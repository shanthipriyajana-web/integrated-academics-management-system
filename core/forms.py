from django import forms
from .models import Faculty, Subject


class FacultyForm(forms.ModelForm):
    class Meta:
        model  = Faculty
        fields = ['department', 'code', 'name']
        widgets = {
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Computer Science',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. AP, MU, GVL',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dr. Full Name',
            }),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ['department', 'year', 'semester', 'code', 'name', 'faculty', 'hours_per_week']
        widgets = {
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Computer Science',
            }),
            'year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2024-25',
            }),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. ML, CN Lab',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full subject name',
            }),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
            'hours_per_week': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1, 'max': 6,
            }),
        }

    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Scope the faculty dropdown to the current department only
        if department:
            self.fields['faculty'].queryset = (
                Faculty.objects.filter(department=department).order_by('code')
            )
        else:
            self.fields['faculty'].queryset = Faculty.objects.none()
