from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


SEMESTER_CHOICES = [
    ('I',    'Semester I'),
    ('II',   'Semester II'),
    ('III',  'Semester III'),
    ('IV',   'Semester IV'),
    ('V',    'Semester V'),
    ('VI',   'Semester VI'),
    ('VII',  'Semester VII'),
    ('VIII', 'Semester VIII'),
    ('IX',   'Semester IX'),
    ('X',    'Semester X'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user  = self.model(email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault('role', 'assistant')
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('assistant', 'Assistant'),
        ('faculty',   'Faculty'),
        ('student',   'Student'),
    ]

    email         = models.EmailField(unique=True)
    full_name     = models.CharField(max_length=150)
    department    = models.CharField(max_length=200, blank=True, default='')
    role          = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    # Student-specific fields
    semester      = models.CharField(max_length=5, choices=SEMESTER_CHOICES, blank=True, default='')
    academic_year = models.CharField(max_length=10, blank=True, default='', help_text='e.g. 2024-25')
    is_active     = models.BooleanField(default=True)
    is_staff      = models.BooleanField(default=False)
    date_joined   = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name        = 'User'
        verbose_name_plural = 'Users'
        ordering            = ['role', 'email']

    def __str__(self):
        return f"{self.full_name} <{self.email}> [{self.role}]"

    def clean(self):
        super().clean()
        if self.role == 'assistant':
            dept = (self.department or '').strip()
            qs = User.objects.filter(role='assistant', department=dept)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if dept == '':
                if qs.exists():
                    raise ValidationError(
                        "There can only be ONE Main Assistant (system-wide) with no department assigned. "
                        "A Main Assistant already exists."
                    )
            else:
                if qs.exists():
                    raise ValidationError(
                        f"A Department Assistant for '{dept}' already exists. "
                        "Each department can have only one assistant."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_assistant(self):
        return self.role == 'assistant'

    @property
    def is_faculty(self):
        return self.role == 'faculty'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_main_assistant(self):
        return self.role == 'assistant' and not (self.department or '').strip()

    @property
    def is_dept_assistant(self):
        return self.role == 'assistant' and bool((self.department or '').strip())


# ── Pre-registered users (admin creates these before users can register) ────
class PreRegisteredUser(models.Model):
    ROLE_CHOICES = [
        ('assistant', 'Assistant'),
        ('faculty',   'Faculty'),
        ('student',   'Student'),
    ]

    email         = models.EmailField(unique=True)
    role          = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    department    = models.CharField(max_length=200, blank=True, default='',
                                     help_text='Leave blank for Main/Super Assistant')
    # Student fills these during self-registration (not set by assistant)
    semester      = models.CharField(max_length=5, choices=SEMESTER_CHOICES, blank=True, default='')
    academic_year = models.CharField(max_length=10, blank=True, default='',
                                     help_text='Programme span e.g. 2025-27 (set by student at registration)')
    created_at    = models.DateTimeField(auto_now_add=True)
    registered    = models.BooleanField(default=False,
                                        help_text='True once the user has completed registration')

    class Meta:
        verbose_name        = 'Pre-registered User'
        verbose_name_plural = 'Pre-registered Users'
        ordering            = ['role', 'email']

    def __str__(self):
        status = '✓ Registered' if self.registered else '⏳ Pending'
        return f"{self.email} [{self.role}] — {status}"


# ── Password reset tokens ───────────────────────────────────────────────────
class PasswordResetToken(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token      = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used       = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def is_valid(self):
        if self.used:
            return False
        expiry = self.created_at + timedelta(hours=1)
        return timezone.now() < expiry

    def __str__(self):
        return f"Reset token for {self.user.email}"
