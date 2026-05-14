from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FacultyForm, SubjectForm
from .mixins import assistant_required, dept_assistant_required
from .models import Faculty, Subject, SEMESTER_CHOICES
from .timetable import DAYS, TIME_SLOTS, generate_timetable
from accounts.models import PreRegisteredUser

User = get_user_model()


# ─── Helpers ───────────────────────────────────────────────────────────────

def _user_dept(request):
    return (getattr(request.user, 'department', '') or '').strip()

def _is_super(request):
    """Super-assistant = assistant with NO department → sees ALL departments."""
    return request.user.is_authenticated and request.user.is_assistant and not _user_dept(request)

def _dept_filter(request):
    dept = _user_dept(request)
    return {} if _is_super(request) else {'department': dept}

def _available_years(dept_filter):
    return list(
        Subject.objects.filter(**dept_filter)
        .order_by('-year').values_list('year', flat=True).distinct()
    )

def _all_departments():
    subject_depts = set(
        Subject.objects.exclude(department='')
        .values_list('department', flat=True).distinct()
    )
    user_depts = set(
        User.objects.exclude(department='').filter(role='assistant')
        .values_list('department', flat=True).distinct()
    )
    prereg_depts = set(
        PreRegisteredUser.objects.exclude(department='').filter(role='assistant')
        .values_list('department', flat=True).distinct()
    )
    return sorted(subject_depts | user_depts | prereg_depts)

def _faculty_dept(request):
    """
    Returns the department string for a faculty user.
    Faculty are strictly locked to their own department.
    """
    if request.user.is_authenticated and request.user.is_faculty:
        return _user_dept(request)
    return None


# ─── Dashboard ─────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    dept_filter = _dept_filter(request)
    years       = _available_years(dept_filter)
    user_dept   = _user_dept(request)
    is_super    = _is_super(request)

    dept_stats = []
    if is_super:
        for dept in _all_departments():
            dept_stats.append({
                'name':     dept,
                'subjects': Subject.objects.filter(department=dept).count(),
                'users':    User.objects.filter(department=dept).count(),
                'years':    Subject.objects.filter(department=dept)
                            .values_list('year', flat=True).distinct().count(),
            })

    # Faculty count is always scoped to the user's own department
    fac_dept_filter = {'department': user_dept} if user_dept else {}

    context = {
        'subject_count':   Subject.objects.filter(**dept_filter).count(),
        'faculty_count':   Faculty.objects.filter(**fac_dept_filter).count(),
        'user_count':      User.objects.filter(**fac_dept_filter).count(),
        'years':           years,
        'morning_slots':   TIME_SLOTS[:3],
        'afternoon_slots': TIME_SLOTS[3:],
        'user_dept':       user_dept,
        'is_super':        is_super,
        'dept_stats':      dept_stats,
        'all_depts':       _all_departments(),
    }
    return render(request, 'core/dashboard.html', context)


# ─── Timetable ─────────────────────────────────────────────────────────────

@login_required
def timetable_view(request):
    is_super  = _is_super(request)
    user_dept = _user_dept(request)
    is_faculty = request.user.is_faculty

    # ── Department selection ──────────────────────────────────────────────
    # Students and faculty are HARD-LOCKED to their own department.
    # Dept assistants are hard-locked too.
    # Only the super-assistant can switch departments.
    if is_super:
        selected_dept = request.GET.get('dept', '') or request.POST.get('dept', '')
        if not selected_dept:
            depts = _all_departments()
            selected_dept = depts[0] if depts else ''
        tt_filter = {'department': selected_dept} if selected_dept else {}
    else:
        # Everyone else is locked to their own department — ignore any ?dept= param
        selected_dept = user_dept
        tt_filter     = {'department': user_dept} if user_dept else {}

    years = list(
        Subject.objects.filter(**tt_filter)
        .order_by('-year').values_list('year', flat=True).distinct()
    )
    selected_year = (
        request.POST.get('year') or request.GET.get('year') or (years[0] if years else '')
    )

    timetable, workload, semesters = {}, {}, []
    if selected_year:
        timetable, workload, semesters = generate_timetable(
            selected_year, selected_dept or None
        )

    # Identify the logged-in faculty member's code — searched within their dept only
    faculty_code = None
    if is_faculty and user_dept:
        try:
            faculty_code = Faculty.objects.get(
                department=user_dept,
                name__iexact=request.user.full_name
            ).code
        except Faculty.DoesNotExist:
            try:
                faculty_code = Faculty.objects.get(
                    department=user_dept,
                    code__iexact=request.user.email.split('@', 1)[0].upper()
                ).code
            except Faculty.DoesNotExist:
                pass

    context = {
        'days':            DAYS,
        'year':            selected_year,
        'years':           years,
        'semesters':       semesters,
        'timetable':       timetable,
        'workload':        workload,
        'faculty_code':    faculty_code,
        'morning_slots':   TIME_SLOTS[:3],
        'afternoon_slots': TIME_SLOTS[3:],
        'current_dept':    selected_dept,
        'all_depts':       _all_departments() if is_super else [],
        'is_super':        is_super,
        'user_dept':       user_dept,
    }
    return render(request, 'core/timetable.html', context)


# ─── Manage Subjects ───────────────────────────────────────────────────────

@dept_assistant_required
def manage_subjects(request):
    user_dept   = _user_dept(request)
    dept_filter = {'department': user_dept}

    years = list(
        Subject.objects.filter(**dept_filter)
        .order_by('-year').values_list('year', flat=True).distinct()
    )
    selected_year = request.GET.get('year') or (years[0] if years else '')

    form = SubjectForm(initial={'year': selected_year, 'department': user_dept},
                       department=user_dept)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_year':
            new_year = request.POST.get('new_year', '').strip()
            if not new_year:
                messages.error(request, 'Please enter an academic year.')
            else:
                return redirect(reverse('manage_subjects') + f'?year={new_year}')
            return redirect('manage_subjects')

        if action == 'add':
            selected_year = request.POST.get('year', '').strip() or selected_year
            data = request.POST.copy()
            data['department'] = user_dept          # always lock to own dept
            form = SubjectForm(data, department=user_dept)
            if form.is_valid():
                form.save()
                messages.success(request, f"Subject '{form.cleaned_data['name']}' added.")
                return redirect(reverse('manage_subjects') + f'?year={selected_year}')
            messages.error(request, 'Please correct the errors below.')

        elif action == 'edit':
            subject = get_object_or_404(Subject, pk=request.POST.get('subject_id'),
                                        department=user_dept)   # 404 if wrong dept
            data = request.POST.copy()
            data['year']       = subject.year
            data['department'] = user_dept
            form_e = SubjectForm(data, instance=subject, department=user_dept)
            if form_e.is_valid():
                form_e.save()
                messages.success(request, 'Subject updated.')
            else:
                messages.error(request, 'Error updating subject.')
            return redirect(reverse('manage_subjects') + f'?year={subject.year}')

        elif action == 'delete':
            subject = get_object_or_404(Subject, pk=request.POST.get('subject_id'),
                                        department=user_dept)   # 404 if wrong dept
            yr = subject.year
            messages.warning(request, f"Subject '{subject.name}' removed.")
            subject.delete()
            return redirect(reverse('manage_subjects') + f'?year={yr}')

    if selected_year and selected_year not in years:
        years.insert(0, selected_year)

    subjects = (
        Subject.objects.filter(**dept_filter, year=selected_year)
        .select_related('faculty').order_by('semester', 'name')
    )
    context = {
        'years':         years,
        'selected_year': selected_year,
        'selected_dept': user_dept,
        'subjects':      subjects,
        'faculty_list':  Faculty.objects.filter(department=user_dept).order_by('code'),
        'form':          form,
        'user_dept':     user_dept,
        'is_super':      False,
        'all_depts':     [],
    }
    return render(request, 'core/manage_subjects.html', context)


# ─── Manage Faculty ────────────────────────────────────────────────────────

@dept_assistant_required
def manage_faculty(request):
    user_dept    = _user_dept(request)
    faculty_list = (
        Faculty.objects
        .filter(department=user_dept)          # ONLY this department's faculty
        .annotate(subject_count=Count('subjects'))
        .order_by('code')
    )
    form = FacultyForm(initial={'department': user_dept})

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            data = request.POST.copy()
            data['code']       = data.get('code', '').strip().upper()
            data['department'] = user_dept          # lock to own dept — never trust POST
            form = FacultyForm(data)
            if form.is_valid():
                form.save()
                messages.success(request, f"Faculty '{form.cleaned_data['name']}' added.")
                return redirect('manage_faculty')
            messages.error(request, 'Please correct the errors below.')

        elif action == 'edit':
            # get_object_or_404 with department=user_dept → 404 if faculty belongs to another dept
            faculty = get_object_or_404(Faculty, pk=request.POST.get('faculty_id'),
                                        department=user_dept)
            data = request.POST.copy()
            data['code']       = data.get('code', '').strip().upper()
            data['department'] = user_dept          # keep locked
            form_e = FacultyForm(data, instance=faculty)
            if form_e.is_valid():
                form_e.save()
                messages.success(request, 'Faculty updated.')
            else:
                messages.error(request, 'Error updating faculty.')
            return redirect('manage_faculty')

        elif action == 'delete':
            faculty = get_object_or_404(Faculty, pk=request.POST.get('faculty_id'),
                                        department=user_dept)
            try:
                faculty.delete()
                messages.warning(request, f"Faculty '{faculty.name}' removed.")
            except ProtectedError:
                messages.error(request, 'Cannot delete: faculty has assigned subjects.')
            return redirect('manage_faculty')

    return render(request, 'core/manage_faculty.html', {
        'faculty_list': faculty_list,
        'form':         form,
        'user_dept':    user_dept,
    })


# ─── Manage Users ──────────────────────────────────────────────────────────

@assistant_required
def manage_users(request):
    user_dept = _user_dept(request)
    is_super  = _is_super(request)

    dept_wise_users = []

    if is_super:
        all_depts_list = _all_departments()
        for dept in all_depts_list:
            dept_assistant    = User.objects.filter(role='assistant', department=dept).first()
            dept_pending_asst = PreRegisteredUser.objects.filter(
                role='assistant', department=dept, registered=False
            ).first()
            dept_users = User.objects.filter(
                department=dept, role__in=['faculty', 'student']
            ).order_by('role', 'full_name')
            dept_pending_users = PreRegisteredUser.objects.filter(
                department=dept, role__in=['faculty', 'student'], registered=False
            ).order_by('role', 'email')
            dept_wise_users.append({
                'dept':             dept,
                'assistant':        dept_assistant,
                'pending_assistant': dept_pending_asst,
                'users':            dept_users,
                'pending_users':    dept_pending_users,
            })
        users   = User.objects.filter(role='assistant').order_by('department', 'full_name')
        pending = PreRegisteredUser.objects.filter(
            registered=False, role='assistant'
        ).order_by('department', 'email')
    else:
        users   = User.objects.filter(department=user_dept, role__in=['student', 'faculty']).order_by('role', 'full_name')
        pending = PreRegisteredUser.objects.filter(
            registered=False, department=user_dept, role__in=['student', 'faculty']
        ).order_by('role', 'email')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            email = request.POST.get('email', '').strip().lower()
            role  = request.POST.get('role', 'student')
            dept  = user_dept if user_dept else request.POST.get('department', '').strip()

            if is_super and role != 'assistant':
                messages.error(request,
                    "The Main Assistant can only pre-register Department Assistants. "
                    "Faculty and students are registered by the respective Department Assistant.")
                return redirect('manage_users')

            def _assistant_slot_ok(r, d):
                if r != 'assistant':
                    return True, None
                d = (d or '').strip()
                if User.objects.filter(role='assistant', department=d).exists():
                    label = 'Main Assistant (system-wide)' if d == '' else f"Department Assistant for '{d}'"
                    return False, f"A {label} already exists. Only ONE is allowed."
                if PreRegisteredUser.objects.filter(role='assistant', department=d, registered=False).exists():
                    label = 'Main Assistant' if d == '' else f"Assistant for '{d}'"
                    return False, f"A pending pre-registration for {label} already exists."
                return True, None

            if not email:
                messages.error(request, 'Email is required.')
            elif User.objects.filter(email__iexact=email).exists():
                messages.error(request, f"'{email}' already has a registered account.")
            elif PreRegisteredUser.objects.filter(email__iexact=email).exists():
                slot = PreRegisteredUser.objects.get(email__iexact=email)
                if slot.registered:
                    messages.error(request, f"'{email}' has already completed registration.")
                else:
                    messages.warning(request, f"'{email}' is already pre-registered and waiting to register.")
            else:
                ok, err = _assistant_slot_ok(role, dept)
                if not ok:
                    messages.error(request, err)
                else:
                    academic_year = ''
                    if role == 'student':
                        academic_year = request.POST.get('academic_year', '').strip()
                        if not academic_year:
                            messages.error(request, 'Programme year is required for students (e.g. 2025-27).')
                            return redirect('manage_users')
                    PreRegisteredUser.objects.create(
                        email=email, role=role, department=dept,
                        academic_year=academic_year,
                    )
                    messages.success(request,
                        f"✓ '{email}' has been pre-registered as {role.title()}. "
                        "They can now complete registration on the login page.")
                    return redirect('manage_users')

        elif action == 'revoke_pending':
            slot = get_object_or_404(PreRegisteredUser, pk=request.POST.get('slot_id'), registered=False)
            if not is_super and slot.department != user_dept:
                messages.error(request, 'Access denied.')
            else:
                email = slot.email
                slot.delete()
                messages.warning(request, f"Pre-registration for '{email}' revoked.")
            return redirect('manage_users')

        elif action == 'delete':
            target = get_object_or_404(User, pk=request.POST.get('user_id'))
            if not is_super and target.department != user_dept:
                messages.error(request, 'Access denied.')
            elif target.pk == request.user.pk:
                messages.error(request, 'You cannot delete your own account.')
            else:
                email = target.email
                PreRegisteredUser.objects.filter(email__iexact=email).delete()
                target.delete()
                messages.warning(request, f"User '{email}' removed.")
                return redirect('manage_users')

    return render(request, 'core/manage_users.html', {
        'users':           users,
        'pending':         pending,
        'user_dept':       user_dept,
        'is_super':        is_super,
        'all_depts':       _all_departments(),
        'dept_wise_users': dept_wise_users,
    })


# ─── Resources: Syllabus & Old Question Papers ─────────────────────────────

from .models import Syllabus, OldQuestionPaper

@login_required
def resources_view(request):
    """
    Every user sees ONLY their own department's resources.
    No ?dept= switching is allowed for faculty/students/dept-assistants.
    """
    is_super   = _is_super(request)
    user_dept  = _user_dept(request)
    is_student = request.user.is_student

    # Determine the department to show — locked for everyone except super-assistant
    if is_super:
        all_depts     = _all_departments()
        selected_dept = request.GET.get('dept', all_depts[0] if all_depts else '')
    else:
        selected_dept = user_dept    # LOCKED — ignore any ?dept= param

    all_years = sorted(set(
        list(Syllabus.objects.filter(department=selected_dept)
             .values_list('academic_year', flat=True).distinct()) +
        list(OldQuestionPaper.objects.filter(department=selected_dept)
             .values_list('academic_year', flat=True).distinct())
    ), reverse=True)

    selected_year = request.GET.get('year', '')
    selected_sem  = request.GET.get('semester', '')

    f = {'department': selected_dept}
    if selected_year:
        f['academic_year'] = selected_year
    if selected_sem:
        f['semester'] = selected_sem

    syllabi = Syllabus.objects.filter(**f).order_by('semester')
    papers  = OldQuestionPaper.objects.filter(**f).order_by('semester', 'subject_name')

    context = {
        'is_student':       is_student,
        'syllabi':          syllabi,
        'papers':           papers,
        'all_depts':        _all_departments() if is_super else [],
        'selected_dept':    selected_dept,
        'user_dept':        user_dept,
        'is_super':         is_super,
        'all_years':        all_years,
        'selected_year':    selected_year,
        'selected_sem':     selected_sem,
        'semester_choices': SEMESTER_CHOICES,
    }
    return render(request, 'core/resources.html', context)


@dept_assistant_required
def manage_resources(request):
    """Upload / delete syllabus and question papers — scoped to own dept only."""
    user_dept = _user_dept(request)
    all_depts = _all_departments()

    from .models import SEMESTER_CHOICES

    if request.method == 'POST':
        action = request.POST.get('action')
        dept   = user_dept          # always use own dept — never trust POST dept field

        if action == 'upload_syllabus':
            f = request.FILES.get('file')
            if not f:
                messages.error(request, 'Please select a file to upload.')
            else:
                try:
                    Syllabus.objects.update_or_create(
                        department=dept,
                        academic_year=request.POST.get('academic_year', '').strip(),
                        semester=request.POST.get('semester', '').strip(),
                        defaults={
                            'title':       request.POST.get('title', '').strip(),
                            'file':        f,
                            'uploaded_by': request.user.full_name,
                        }
                    )
                    messages.success(request, 'Syllabus uploaded successfully.')
                except Exception as e:
                    messages.error(request, f'Upload failed: {e}')

        elif action == 'delete_syllabus':
            obj = get_object_or_404(Syllabus, pk=request.POST.get('item_id'),
                                    department=user_dept)   # 404 if wrong dept
            obj.file.delete(save=False)
            obj.delete()
            messages.warning(request, 'Syllabus deleted.')

        elif action == 'upload_paper':
            f = request.FILES.get('file')
            if not f:
                messages.error(request, 'Please select a file to upload.')
            else:
                OldQuestionPaper.objects.create(
                    department   = dept,
                    academic_year= request.POST.get('academic_year', '').strip(),
                    semester     = request.POST.get('semester', '').strip(),
                    subject_name = request.POST.get('subject_name', '').strip(),
                    subject_code = request.POST.get('subject_code', '').strip(),
                    exam_type    = request.POST.get('exam_type', '').strip(),
                    file         = f,
                    uploaded_by  = request.user.full_name,
                )
                messages.success(request, 'Question paper uploaded successfully.')

        elif action == 'delete_paper':
            obj = get_object_or_404(OldQuestionPaper, pk=request.POST.get('item_id'),
                                    department=user_dept)   # 404 if wrong dept
            obj.file.delete(save=False)
            obj.delete()
            messages.warning(request, 'Question paper deleted.')

        return redirect('manage_resources')

    # GET
    f        = {'department': user_dept}
    syllabi  = Syllabus.objects.filter(**f).order_by('-academic_year', 'semester')
    papers   = OldQuestionPaper.objects.filter(**f).order_by('-academic_year', 'semester', 'subject_name')

    all_academic_years = sorted(set(
        list(Syllabus.objects.filter(department=user_dept).values_list('academic_year', flat=True).distinct()) +
        list(OldQuestionPaper.objects.filter(department=user_dept).values_list('academic_year', flat=True).distinct())
    ), reverse=True)
    if not all_academic_years:
        from datetime import date
        yr = date.today().year
        all_academic_years = [f"{yr}-{str(yr+1)[2:]}"]

    context = {
        'syllabi':            syllabi,
        'papers':             papers,
        'all_depts':          all_depts,
        'selected_dept':      user_dept,
        'semester_choices':   SEMESTER_CHOICES,
        'user_dept':          user_dept,
        'is_super':           False,
        'all_academic_years': all_academic_years,
    }
    return render(request, 'core/manage_resources.html', context)
