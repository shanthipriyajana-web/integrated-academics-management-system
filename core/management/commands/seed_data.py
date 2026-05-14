from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import PreRegisteredUser
from core.models import Faculty, Subject

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with default faculty, subjects, and an admin user'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # ── Default admin user ──
        if not User.objects.filter(email='admin@vsu.edu').exists():
            User.objects.create_superuser(
                email='admin@vsu.edu',
                password='Admin@123',
                full_name='Administrator',
                role='assistant',
            )
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created: admin@vsu.edu / Admin@123'))
            PreRegisteredUser.objects.get_or_create(email='admin@vsu.edu', defaults={'role':'assistant','registered':True})
        else:
            self.stdout.write('  – Admin user already exists')

        # ── Default faculty ──
        faculty_data = [
            ('AP',  'Dr. A. Prasad'),
            ('MU',  'Prof. M. Uma'),
            ('GVL', 'Dr. G.V. Lakshmi'),
            ('PS',  'Prof. P. Sharma'),
            ('SKS', 'Dr. S.K. Singh'),
            ('VS',  'Prof. V. Srinivas'),
        ]
        for code, name in faculty_data:
            obj, created = Faculty.objects.get_or_create(code=code, defaults={'name': name})
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Faculty: {code} – {name}'))

        # ── Default subjects ──
        ap  = Faculty.objects.get(code='AP')
        mu  = Faculty.objects.get(code='MU')
        gvl = Faculty.objects.get(code='GVL')
        ps  = Faculty.objects.get(code='PS')
        sks = Faculty.objects.get(code='SKS')
        vs  = Faculty.objects.get(code='VS')

        subjects_data = [
            # (year, semester, code, name, faculty, hours)
            ('2024-25', 'I',   'ML',      'Machine Learning',             ap,  4),
            ('2024-25', 'I',   'CN',      'Computer Networks',            mu,  4),
            ('2024-25', 'I',   'OS',      'Operating Systems',            gvl, 4),
            ('2024-25', 'I',   'ML Lab',  'Machine Learning Lab',         ap,  3),
            ('2024-25', 'I',   'CN Lab',  'Computer Networks Lab',        mu,  3),
            ('2024-25', 'III', 'SPM',     'Software Project Management',  gvl, 4),
            ('2024-25', 'III', 'NSMDB',   'NoSQL & Modern DB',            ps,  4),
            ('2024-25', 'III', 'MSD',     'Micro Services Design',        sks, 4),
            ('2024-25', 'III', 'ITA',     'IT Audit',                     vs,  4),
            ('2024-25', 'III', 'MSD Lab', 'MSD Lab',                      sks, 3),
        ]

        for year, sem, code, name, fac, hrs in subjects_data:
            obj, created = Subject.objects.get_or_create(
                year=year, semester=sem, code=code,
                defaults={'name': name, 'faculty': fac, 'hours_per_week': hrs}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Subject: [{year} Sem {sem}] {code}'))

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('  Login: admin@vsu.edu  /  Admin@123')
