from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id',   models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Faculty',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year',           models.CharField(max_length=10)),
                ('semester',       models.CharField(
                    choices=[('I', 'Semester I'), ('II', 'Semester II'), ('III', 'Semester III'), ('IV', 'Semester IV'),
                             ('V', 'Semester V'), ('VI', 'Semester VI'), ('VII', 'Semester VII'), ('VIII', 'Semester VIII'),
                             ('IX', 'Semester IX'), ('X', 'Semester X')],
                    max_length=5
                )),
                ('code',           models.CharField(max_length=50)),
                ('name',           models.CharField(max_length=200)),
                ('hours_per_week', models.PositiveSmallIntegerField(default=4)),
                ('faculty',        models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='subjects',
                    to='core.faculty'
                )),
            ],
            options={
                'ordering': ['year', 'semester', 'name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('year', 'semester', 'code')},
        ),
    ]
