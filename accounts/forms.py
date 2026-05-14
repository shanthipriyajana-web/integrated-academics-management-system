from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import PreRegisteredUser, SEMESTER_CHOICES

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class':       'form-control',
            'placeholder': 'you@vsu.edu',
            'autofocus':   True,
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Enter your password',
        })
    )

    error_messages = {
        'invalid_login': (
            "Invalid email or password. Please check your credentials and try again."
        ),
        'inactive': "This account has been disabled. Please contact the administrator.",
    }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Min 6 characters',
            'id':          'reg-pw',
            'oninput':     'checkStrength(this.value)',
        })
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Re-enter password',
            'id':          'reg-cfm',
            'oninput':     'checkMatch()',
        })
    )
    class Meta:
        model  = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr. / Mr. / Ms. Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@vsu.edu',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        try:
            slot = PreRegisteredUser.objects.get(email__iexact=email)
        except PreRegisteredUser.DoesNotExist:
            raise forms.ValidationError(
                "This email is not registered in our system. "
                "Please contact your administrator to be added."
            )
        if slot.registered:
            raise forms.ValidationError(
                "An account with this email already exists. Please sign in instead."
            )
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists. Please sign in instead."
            )
        return email

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cfm = cleaned.get('confirm_password')
        if pw and cfm and pw != cfm:
            raise forms.ValidationError("Passwords do not match.")

        email = cleaned.get('email', '').strip().lower()
        try:
            slot = PreRegisteredUser.objects.get(email__iexact=email)
            role = slot.role
            dept = (slot.department or '').strip()
        except PreRegisteredUser.DoesNotExist:
            return cleaned

        # academic_year is set by the assistant at pre-registration — nothing to validate here

        if role == 'assistant':
            qs = User.objects.filter(role='assistant', department=dept)
            if qs.exists():
                if dept == '':
                    raise forms.ValidationError(
                        "A Main Assistant (no department) already exists. "
                        "Only ONE main assistant is allowed system-wide."
                    )
                raise forms.ValidationError(
                    f"A Department Assistant for '{dept}' already exists. "
                    "Each department can only have ONE assistant."
                )
        return cleaned

    def save(self, commit=True):
        email = self.cleaned_data['email'].strip().lower()
        slot  = PreRegisteredUser.objects.get(email__iexact=email)

        user = super().save(commit=False)
        user.email         = email
        user.role          = slot.role
        user.department    = slot.department or ''
        user.semester      = ''
        # academic_year was set by the assistant at pre-registration time
        user.academic_year = slot.academic_year or ''
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            slot.registered = True
            slot.save()
        return user


class FirstRunForm(forms.ModelForm):
    """
    Used ONLY when no users exist yet (fresh install).
    Creates the Main Assistant account without requiring pre-registration.
    """
    password = forms.CharField(
        label='Password',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Min 6 characters',
            'id':          'reg-pw',
            'oninput':     'checkStrength(this.value)',
        })
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Re-enter password',
            'id':          'reg-cfm',
            'oninput':     'checkMatch()',
        })
    )

    class Meta:
        model  = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class':       'form-control',
                'placeholder': 'admin@vsu.edu',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cfm = cleaned.get('confirm_password')
        if pw and cfm and pw != cfm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email        = self.cleaned_data['email'].strip().lower()
        user.role         = 'assistant'
        user.department   = ''
        user.is_staff     = True
        user.is_superuser = True
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Registered Email Address',
        widget=forms.EmailInput(attrs={
            'class':       'form-control',
            'placeholder': 'you@vsu.edu',
            'autofocus':   True,
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "No account found with this email address."
            )
        return email


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='New Password',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Min 6 characters',
            'id':          'new-pw',
            'oninput':     'checkStrength(this.value)',
        })
    )
    confirm_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class':       'form-control',
            'placeholder': 'Re-enter new password',
            'id':          'new-cfm',
            'oninput':     'checkMatch()',
        })
    )

    def clean(self):
        cleaned = super().clean()
        pw  = cleaned.get('password')
        cfm = cleaned.get('confirm_password')
        if pw and cfm and pw != cfm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned
