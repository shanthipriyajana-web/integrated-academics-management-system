from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_enforce_assistant_uniqueness'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreRegisteredUser',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email',      models.EmailField(max_length=254, unique=True)),
                ('role',       models.CharField(
                    choices=[('assistant', 'Assistant'), ('faculty', 'Faculty'), ('student', 'Student')],
                    default='student', max_length=20
                )),
                ('department', models.CharField(
                    blank=True, default='', max_length=200,
                    help_text='Leave blank for Main/Super Assistant'
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('registered', models.BooleanField(
                    default=False,
                    help_text='True once the user has completed registration'
                )),
            ],
            options={
                'verbose_name': 'Pre-registered User',
                'verbose_name_plural': 'Pre-registered Users',
                'ordering': ['role', 'email'],
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token',      models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('used',       models.BooleanField(default=False)),
                ('user',       models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reset_tokens',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
