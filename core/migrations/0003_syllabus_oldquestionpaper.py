from django.db import migrations, models


SEMESTER_CHOICES = [
    ('I','Semester I'),('II','Semester II'),('III','Semester III'),
    ('IV','Semester IV'),('V','Semester V'),('VI','Semester VI'),
    ('VII','Semester VII'),('VIII','Semester VIII'),('IX','Semester IX'),
    ('X','Semester X'),
]


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_department_to_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department',   models.CharField(max_length=200)),
                ('academic_year',models.CharField(max_length=10, help_text='e.g. 2024-25')),
                ('semester',     models.CharField(max_length=5, choices=SEMESTER_CHOICES)),
                ('title',        models.CharField(max_length=300)),
                ('file',         models.FileField(upload_to='syllabus/')),
                ('uploaded_at',  models.DateTimeField(auto_now_add=True)),
                ('uploaded_by',  models.CharField(max_length=150, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Syllabi',
                'ordering': ['department', 'academic_year', 'semester'],
            },
        ),
        migrations.AddConstraint(
            model_name='syllabus',
            constraint=models.UniqueConstraint(
                fields=['department', 'academic_year', 'semester'],
                name='unique_syllabus_per_dept_year_sem'
            ),
        ),
        migrations.CreateModel(
            name='OldQuestionPaper',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department',   models.CharField(max_length=200)),
                ('academic_year',models.CharField(max_length=10, help_text='e.g. 2023-24')),
                ('semester',     models.CharField(max_length=5, choices=SEMESTER_CHOICES)),
                ('subject_name', models.CharField(max_length=200)),
                ('subject_code', models.CharField(max_length=50, blank=True)),
                ('exam_type',    models.CharField(max_length=100, blank=True, help_text='e.g. Mid-1, Mid-2, End-Sem')),
                ('file',         models.FileField(upload_to='question_papers/')),
                ('uploaded_at',  models.DateTimeField(auto_now_add=True)),
                ('uploaded_by',  models.CharField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['department', 'academic_year', 'semester', 'subject_name'],
            },
        ),
    ]
