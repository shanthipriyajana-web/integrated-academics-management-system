"""
Migration: enforce assistant uniqueness rules.

No schema changes — uniqueness is enforced via model-level clean() / save().
This migration records the policy change in the migration history.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_department'),
    ]

    operations = [
        # No DB schema change; uniqueness enforced in model.clean() / model.save()
    ]
