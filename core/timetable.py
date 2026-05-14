import random

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

TIME_SLOTS = [
    "10:00–11:00",
    "11:00–12:00",
    "12:00–13:00",
    # 13:00–14:00 = LUNCH (not a slot)
    "14:00–15:00",
    "15:00–16:00",
    "16:00–17:00",
]  # indices 0-2 = morning block, 3-5 = afternoon block


def generate_timetable(year, department=None):
    """
    Returns:
        timetable  : { day: { semester: [cell|None, ...6] } }
        workload   : { faculty_code: { name, theory, practical, total, subjects } }
        semesters  : sorted list of semester strings present
    """
    from .models import Subject

    qs_filter = {'year': year}
    if department:
        qs_filter['department'] = department
    subjects_qs = (
        Subject.objects
        .filter(**qs_filter)
        .select_related('faculty')
    )

    if not subjects_qs.exists():
        return {}, {}, []

    # Group by semester
    sem_map = {}
    for sub in subjects_qs:
        sem_map.setdefault(sub.semester, []).append(sub)

    semesters = sorted(sem_map.keys())
    n_slots   = len(TIME_SLOTS)  # 6

    # Build empty skeleton
    timetable = {
        day: {sem: [None] * n_slots for sem in semesters}
        for day in DAYS
    }

    # Track which (day, start) lab blocks are already taken across ALL semesters
    # so two semesters never share the same lab slot simultaneously.
    occupied_lab_blocks = set()  # set of (day, start_index)

    for sem, subs in sem_map.items():
        lab_subs  = [s for s in subs if s.is_lab]
        theo_subs = [s for s in subs if not s.is_lab]

        # ── Schedule labs first (3 consecutive slots) ──
        random.shuffle(lab_subs)
        used_days = set()

        for lab in lab_subs:
            placed = False
            days_order = DAYS[:]
            random.shuffle(days_order)

            for day in days_order:
                if day in used_days:
                    continue
                # valid 3-slot starting indices: 0 (morning) or 3 (afternoon)
                for start in [0, 3]:
                    # Check this sem's own slots are free
                    if not all(timetable[day][sem][start + i] is None for i in range(3)):
                        continue
                    # Check no other semester already has a lab block at this day+start
                    if (day, start) in occupied_lab_blocks:
                        continue
                    cell = {
                        'code':     lab.code,
                        'name':     lab.name,
                        'faculty':  lab.faculty.code,
                        'fac_name': lab.faculty.name,
                        'type':     'lab',
                    }
                    for i in range(3):
                        timetable[day][sem][start + i] = cell
                    occupied_lab_blocks.add((day, start))
                    used_days.add(day)
                    placed = True
                    break
                if placed:
                    break

        # ── Schedule theory subjects spread across week ──
        slots_to_fill = []
        for sub in theo_subs:
            for _ in range(sub.hours_per_week):
                slots_to_fill.append(sub)
        random.shuffle(slots_to_fill)

        for sub in slots_to_fill:
            placed = False
            days_order = DAYS[:]
            random.shuffle(days_order)

            for day in days_order:
                for slot_i in range(n_slots):
                    if timetable[day][sem][slot_i] is not None:
                        continue

                    # No consecutive same subject
                    prev = timetable[day][sem][slot_i - 1] if slot_i > 0 else None
                    if prev and prev['code'] == sub.code:
                        continue

                    # No same subject more than once per day
                    day_codes = [
                        c['code'] for c in timetable[day][sem] if c is not None
                    ]
                    if sub.code in day_codes:
                        continue

                    timetable[day][sem][slot_i] = {
                        'code':     sub.code,
                        'name':     sub.name,
                        'faculty':  sub.faculty.code,
                        'fac_name': sub.faculty.name,
                        'type':     'theory',
                    }
                    placed = True
                    break
                if placed:
                    break

    # ── Faculty workload ──
    workload = {}
    for day in DAYS:
        for sem in semesters:
            for cell in timetable[day][sem]:
                if not cell:
                    continue
                fac = cell['faculty']
                if fac not in workload:
                    workload[fac] = {
                        'name':      cell['fac_name'],
                        'theory':    0,
                        'practical': 0,
                        'subjects':  set(),
                    }
                if cell['type'] == 'lab':
                    workload[fac]['practical'] += 1
                else:
                    workload[fac]['theory'] += 1
                workload[fac]['subjects'].add(cell['code'])

    for fac in workload:
        workload[fac]['total']    = workload[fac]['theory'] + workload[fac]['practical']
        workload[fac]['subjects'] = sorted(workload[fac]['subjects'])

    return timetable, workload, semesters
