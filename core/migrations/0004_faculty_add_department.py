from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_syllabus_oldquestionpaper'),
    ]

    operations = [
        # 1. Add the department column (blank allowed temporarily so existing rows survive)
        migrations.AddField(
            model_name='faculty',
            name='department',
            field=models.CharField(
                max_length=200, default='', blank=True,
                help_text='Department this faculty member belongs to.',
            ),
        ),
        # 2. Drop the old global unique constraint on code alone
        migrations.AlterField(
            model_name='faculty',
            name='code',
            field=models.CharField(max_length=20),
        ),
        # 3. Apply the new per-department unique constraint
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together={('department', 'code')},
        ),
        # 4. Update ordering
        migrations.AlterModelOptions(
            name='faculty',
            options={
                'ordering': ['department', 'code'],
                'verbose_name_plural': 'Faculty',
            },
        ),
    ]
