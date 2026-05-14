from django.db import models


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


class Faculty(models.Model):
    department = models.CharField(
        max_length=200, default='', blank=False,
        help_text='Department this faculty member belongs to.'
    )
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'Faculty'
        ordering            = ['department', 'code']
        unique_together     = ('department', 'code')   # code unique per dept, not globally

    def __str__(self):
        return f"[{self.department}] {self.code} – {self.name}"


class Subject(models.Model):
    department     = models.CharField(max_length=200, default='', blank=True)
    year           = models.CharField(max_length=10)
    semester       = models.CharField(max_length=5, choices=SEMESTER_CHOICES)
    code           = models.CharField(max_length=50)
    name           = models.CharField(max_length=200)
    faculty        = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name='subjects')
    hours_per_week = models.PositiveSmallIntegerField(default=4)

    class Meta:
        unique_together = ('department', 'year', 'semester', 'code')
        ordering = ['year', 'semester', 'name']

    def __str__(self):
        return f"[{self.year} Sem {self.semester}] {self.code} – {self.name}"

    @property
    def is_lab(self):
        return 'lab' in self.code.lower() or 'lab' in self.name.lower()

    @property
    def display_type(self):
        return 'Lab ×3' if self.is_lab else 'Theory'


class Syllabus(models.Model):
    department   = models.CharField(max_length=200)
    academic_year = models.CharField(max_length=10, help_text='e.g. 2024-25')
    semester     = models.CharField(max_length=5, choices=SEMESTER_CHOICES)
    title        = models.CharField(max_length=300, help_text='Short description, e.g. B.Tech CSE Semester III Syllabus')
    file         = models.FileField(upload_to='syllabus/')
    uploaded_at  = models.DateTimeField(auto_now_add=True)
    uploaded_by  = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = 'Syllabi'
        ordering = ['department', 'academic_year', 'semester']
        unique_together = ('department', 'academic_year', 'semester')

    def __str__(self):
        return f"[{self.department}] {self.academic_year} Sem {self.semester} — {self.title}"


class OldQuestionPaper(models.Model):
    department   = models.CharField(max_length=200)
    academic_year = models.CharField(max_length=10, help_text='e.g. 2023-24')
    semester     = models.CharField(max_length=5, choices=SEMESTER_CHOICES)
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=50, blank=True)
    exam_type    = models.CharField(max_length=100, blank=True, help_text='e.g. Mid-1, Mid-2, End-Sem')
    file         = models.FileField(upload_to='question_papers/')
    uploaded_at  = models.DateTimeField(auto_now_add=True)
    uploaded_by  = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['department', 'academic_year', 'semester', 'subject_name']

    def __str__(self):
        return f"[{self.department}] {self.academic_year} Sem {self.semester} — {self.subject_name}"
