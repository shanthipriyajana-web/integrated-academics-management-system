from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_preregistereduser_passwordresettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='semester',
            field=models.CharField(
                blank=True, default='',
                choices=[
                    ('I','Semester I'),('II','Semester II'),('III','Semester III'),
                    ('IV','Semester IV'),('V','Semester V'),('VI','Semester VI'),
                    ('VII','Semester VII'),('VIII','Semester VIII'),('IX','Semester IX'),
                    ('X','Semester X'),
                ],
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='academic_year',
            field=models.CharField(blank=True, default='', max_length=10,
                                   help_text='e.g. 2024-25'),
        ),
        migrations.AddField(
            model_name='preregistereduser',
            name='semester',
            field=models.CharField(
                blank=True, default='',
                choices=[
                    ('I','Semester I'),('II','Semester II'),('III','Semester III'),
                    ('IV','Semester IV'),('V','Semester V'),('VI','Semester VI'),
                    ('VII','Semester VII'),('VIII','Semester VIII'),('IX','Semester IX'),
                    ('X','Semester X'),
                ],
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name='preregistereduser',
            name='academic_year',
            field=models.CharField(blank=True, default='', max_length=10,
                                   help_text='e.g. 2024-25'),
        ),
    ]
