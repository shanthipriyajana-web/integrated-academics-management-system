from django.contrib import admin
from .models import Faculty, Subject


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display  = ('code', 'name')
    search_fields = ('code', 'name')
    ordering      = ('code',)


class IsLabFilter(admin.SimpleListFilter):
    title        = 'type'
    parameter_name = 'is_lab'

    def lookups(self, request, model_admin):
        return [('lab', 'Lab'), ('theory', 'Theory')]

    def queryset(self, request, queryset):
        if self.value() == 'lab':
            return queryset.filter(code__icontains='lab') | queryset.filter(name__icontains='lab')
        if self.value() == 'theory':
            return queryset.exclude(code__icontains='lab').exclude(name__icontains='lab')
        return queryset


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display   = ('year', 'semester', 'code', 'name', 'faculty', 'hours_per_week', 'display_type')
    list_filter    = ('year', 'semester', 'faculty', IsLabFilter)
    search_fields  = ('code', 'name')
    ordering       = ('year', 'semester', 'name')
    list_per_page  = 25

    fieldsets = (
        ('Academic Info', {'fields': ('year', 'semester')}),
        ('Subject',       {'fields': ('code', 'name', 'faculty', 'hours_per_week')}),
    )

    def display_type(self, obj):
        return obj.display_type
    display_type.short_description = 'Type'

from .models import Syllabus, OldQuestionPaper

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('department', 'academic_year', 'semester', 'title', 'uploaded_by', 'uploaded_at')
    list_filter  = ('department', 'semester', 'academic_year')
    search_fields = ('title', 'department')

@admin.register(OldQuestionPaper)
class OldQuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('department', 'academic_year', 'semester', 'subject_name', 'subject_code', 'exam_type', 'uploaded_by', 'uploaded_at')
    list_filter  = ('department', 'semester', 'academic_year', 'exam_type')
    search_fields = ('subject_name', 'subject_code', 'department')
