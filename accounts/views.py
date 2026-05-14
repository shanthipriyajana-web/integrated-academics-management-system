from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm, FirstRunForm
from .models import PasswordResetToken

User = get_user_model()


def first_run_setup(request):
    """
    One-time setup view — only accessible when NO users exist at all.
    Creates the very first Main Assistant account, bypassing pre-registration.
    """
    if User.objects.exists():
        # System already has users — this page is no longer available
        return redirect('login')

    form = FirstRunForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(
            request,
            f"Welcome, {user.full_name}! Your Main Assistant account has been created. "
            "You can now pre-register other users from the Manage Users page."
        )
        return redirect('dashboard')

    return render(request, 'accounts/first_run_setup.html', {'form': form})


def _assistant_slot_available(role, department, exclude_pk=None):
    if role != 'assistant':
        return True, None
    dept = (department or '').strip()
    qs = User.objects.filter(role='assistant', department=dept)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    if qs.exists():
        if dept == '':
            return False, (
                "A Main Assistant (system-wide, no department) already exists. "
                "Only ONE main assistant is allowed."
            )
        return False, (
            f"A Department Assistant for '{dept}' already exists. "
            "Each department can only have ONE assistant."
        )
    return True, None


def login_view(request):
    # No users at all? Send to first-run setup instead
    if not User.objects.exists():
        return redirect('first_run_setup')

    login_form    = LoginForm(request)
    register_form = RegisterForm()
    active_tab    = request.GET.get('tab', 'login')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'switch_account' and request.user.is_authenticated:
            current_account = request.user.full_name or request.user.email
            logout(request)
            messages.info(request, f"Signed out from {current_account}. You can now sign in with another account.")
            return redirect('login')

        if request.user.is_authenticated:
            return redirect('dashboard')

        if action == 'login':
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('dashboard')
            active_tab = 'login'

        elif action == 'register':
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Account created successfully! You can now sign in.")
                return redirect('login')
            else:
                active_tab = 'register'

    elif request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, 'accounts/login.html', {
        'login_form':    login_form,
        'register_form': register_form,
        'active_tab':    active_tab,
    })


def signout_page(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/signout.html')


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been signed out successfully.")
    return redirect('login')


# ── Forgot Password ──────────────────────────────────────────────────────────

def forgot_password_view(request):
    form = ForgotPasswordForm()
    reset_link = None  # Shown on-screen in dev (no email server needed)

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user  = User.objects.get(email__iexact=email)

            # Invalidate previous tokens for this user
            PasswordResetToken.objects.filter(user=user, used=False).update(used=True)

            # Create a fresh token
            token_obj  = PasswordResetToken.objects.create(user=user)
            reset_link = request.build_absolute_uri(
                f"/accounts/reset-password/{token_obj.token}/"
            )

            messages.success(
                request,
                "Password reset link generated. Use the link below to reset your password."
            )

    return render(request, 'accounts/forgot_password.html', {
        'form':       form,
        'reset_link': reset_link,
    })


def reset_password_view(request, token):
    token_obj = get_object_or_404(PasswordResetToken, token=token)

    if not token_obj.is_valid():
        messages.error(request, "This password reset link has expired or has already been used.")
        return redirect('forgot_password')

    form = ResetPasswordForm()

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = token_obj.user
            user.set_password(form.cleaned_data['password'])
            user.save()
            token_obj.used = True
            token_obj.save()
            messages.success(request, "Password reset successfully! You can now sign in.")
            return redirect('login')

    return render(request, 'accounts/reset_password.html', {
        'form':      form,
        'token':     token,
        'user_email': token_obj.user.email,
    })


# ── AJAX: check pre-registered role for an email ────────────────────────────
from django.http import JsonResponse

def check_role_view(request):
    email = request.GET.get('email', '').strip().lower()
    try:
        slot = PreRegisteredUser.objects.get(email__iexact=email)
        return JsonResponse({'role': slot.role, 'found': True})
    except PreRegisteredUser.DoesNotExist:
        return JsonResponse({'role': None, 'found': False})
