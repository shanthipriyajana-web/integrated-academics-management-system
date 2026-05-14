from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def assistant_required(view_func):
    """Allows any assistant (main or dept)."""
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_assistant:
            messages.error(request, "Access denied. Assistant role required.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def dept_assistant_required(view_func):
    """
    Restricts access to Department Assistants only.
    Main Assistant (no department) is a monitor — they cannot enter or edit data.
    Only Dept Assistants handle data entry (subjects, faculty, resources).
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_assistant:
            messages.error(request, "Access denied. Assistant role required.")
            return redirect('dashboard')
        # Main assistant (no dept) is monitor-only — block data-entry views
        if request.user.is_main_assistant:
            messages.error(
                request,
                "Access denied. The Main Assistant is a monitor only and cannot "
                "enter or edit data. Data entry is handled by Department Assistants."
            )
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


class AssistantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_assistant

    def handle_no_permission(self):
        messages.error(self.request, "Access denied. Assistant role required.")
        return redirect('dashboard')


class DeptAssistantRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """CBV mixin — dept assistants only, main assistant is blocked (monitor role)."""
    def test_func(self):
        return self.request.user.is_assistant and self.request.user.is_dept_assistant

    def handle_no_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_main_assistant:
            messages.error(
                self.request,
                "Access denied. The Main Assistant is a monitor only and cannot "
                "enter or edit data."
            )
        else:
            messages.error(self.request, "Access denied. Department Assistant role required.")
        return redirect('dashboard')
