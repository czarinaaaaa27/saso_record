"""Run with: python manage.py shell < apps/seed.py"""
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.students.models import Student
from apps.discipline.models import DisciplinaryCase
from apps.activities.models import Activity
from datetime import date, timedelta
import random

User = get_user_model()

# Super admin account
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@oct.edu.ph', 'admin1234', role='super_admin',
first_name='System', last_name='Administrator')
    print("Created super admin: admin / admin1234")

sample_users = [
    ('assistant', 'assistant1234', 'assistant', 'Maria', 'Santos', 'assistant@oct.edu.ph'),
    ('staff', 'staff1234', 'staff', 'Liza', 'Cruz', 'staff@oct.edu.ph'),
]

for username, password, role, first_name, last_name, email in sample_users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username,
            email,
            password,
            role=role,
            first_name=first_name,
            last_name=last_name,
        )
        print(f"Created user: {username} / {password}")

# Sample students
courses = ['BSIT', 'BSCS', 'BSBA', 'BSED', 'BSN', 'BSA', 'BSCRIM']
statuses = ['completed', 'pending']
first_names = ['Maria', 'Jose', 'Juan', 'Ana', 'Carlo', 'Liza', 'Mark', 'Grace', 'Ryan', 'Carla',
               'Miguel', 'Diana', 'Luis', 'Sofia', 'Aaron', 'Nina', 'Kevin', 'Ella', 'Jared', 'Bianca']
last_names = ['Santos', 'Reyes', 'Cruz', 'Garcia', 'Torres', 'Flores', 'Lopez', 'Ramos',
              'Mendoza', 'Bautista', 'Dela Cruz', 'Aquino', 'Villanueva', 'Castillo', 'Gonzales']

students = []
for i in range(1, 31):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    sid = f"OCT-2024-{i:04d}"
    if not Student.objects.filter(student_id=sid).exists():
        s = Student.objects.create(
            student_id=sid,
            first_name=fn,
            last_name=ln,
            course=random.choice(courses),
            year_level=random.randint(1, 4),
            address=f"{random.randint(1, 999)} Sample St., Tagaytay City",
            email=f"{fn.lower()}.{ln.lower().replace(' ', '')}@student.oct.edu.ph",
            status=random.choice(statuses),
        )
        students.append(s)
        print(f"Created student: {s}")

all_students = list(Student.objects.all())

# Sample disciplinary cases
violations = [
    ('Tardiness', 'minor'),
    ('Dress Code Violation', 'minor'),
    ('Cheating', 'major'),
    ('Bullying', 'major'),
    ('Disrespect to Faculty', 'moderate'),
    ('Vandalism', 'moderate'),
    ('Possession of Prohibited Items', 'major'),
    ('Cutting Classes', 'minor'),
    ('Fighting', 'major'),
    ('Smoking on Campus', 'moderate'),
]
case_statuses = ['pending', 'under_review', 'resolved']

for i, s in enumerate(all_students[:15]):
    v, sev = random.choice(violations)
    DisciplinaryCase.objects.create(
        student=s,
        incident_date=date.today() - timedelta(days=random.randint(0, 180)),
        violation=v,
        description=f"Student was found to have committed {v.lower()} on campus.",
        severity=sev,
        status=random.choice(case_statuses),
        sanction='Warning letter issued.' if sev == 'minor' else 'Suspension pending review.',
    )

print(f"Created {DisciplinaryCase.objects.count()} disciplinary cases")

# Sample activities
activity_titles = [
    ('Leadership Training Seminar', 30),
    ('SASO Orientation', 14),
    ('Sports Fest', 7),
    ('Community Service Day', 3),
    ('Cultural Night', -5),
    ('College Foundation Week', -20),
    ('Mental Health Awareness Week', 45),
]

for title, days_from_now in activity_titles:
    if not Activity.objects.filter(title=title).exists():
        Activity.objects.create(
            title=title,
            description=f"{title} organized by SASO.",
            event_date=date.today() + timedelta(days=days_from_now),
            location='Olivarez College Tagaytay',
            organizer='SASO',
        )

print(f"Created {Activity.objects.count()} activities")
print("\nDone seeding!")
