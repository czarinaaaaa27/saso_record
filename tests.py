from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from apps.activities.models import Activity, ActivityParticipation
from apps.students.models import Student

User = get_user_model()


class ActivityAttendanceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin1234',
            role='super_admin',
            first_name='System',
            last_name='Administrator',
        )
        self.student = Student.objects.create(
            student_id='S-2001',
            first_name='Ana',
            last_name='Cruz',
            course='BSIT',
            year_level=1,
            address='Tagaytay City',
            email='ana@example.com',
            status='pending',
        )
        self.activity = Activity.objects.create(
            title='Orientation',
            event_date='2026-06-30',
            location='Auditorium',
            organizer='SASO',
        )

    def test_create_participation(self):
        self.client.login(username='admin', password='admin1234')

        response = self.client.post('/api/activities/participations/', {
            'student': self.student.id,
            'activity': self.activity.id,
            'attendance_status': 'invited',
            'role': 'participant',
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ActivityParticipation.objects.count(), 1)
        self.assertEqual(ActivityParticipation.objects.first().attendance_status, 'invited')

    def test_mark_present_sets_marked_time(self):
        self.client.login(username='admin', password='admin1234')
        participation = ActivityParticipation.objects.create(
            student=self.student,
            activity=self.activity,
            attendance_status='invited',
        )

        response = self.client.patch(f'/api/activities/participations/{participation.id}/', {
            'attendance_status': 'present',
        }, format='json')

        self.assertEqual(response.status_code, 200)
        participation.refresh_from_db()
        self.assertEqual(participation.attendance_status, 'present')
        self.assertIsNotNone(participation.attendance_marked_at)

    def test_bulk_add_by_course_and_year(self):
        self.client.login(username='admin', password='admin1234')
        other_student = Student.objects.create(
            student_id='S-2002',
            first_name='Mark',
            last_name='Reyes',
            course='BSIT',
            year_level=1,
            address='Tagaytay City',
            email='mark@example.com',
            status='pending',
        )
        Student.objects.create(
            student_id='S-2003',
            first_name='Luis',
            last_name='Garcia',
            course='BSCS',
            year_level=1,
            address='Tagaytay City',
            email='luis@example.com',
            status='pending',
        )
        ActivityParticipation.objects.create(
            student=self.student,
            activity=self.activity,
            attendance_status='invited',
        )

        response = self.client.post('/api/activities/participations/bulk-add/', {
            'activity': self.activity.id,
            'course': 'BSIT',
            'year_level': '1',
        }, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['created'], 1)
        self.assertEqual(response.data['skipped'], 1)
        self.assertEqual(response.data['total_matched'], 2)
        self.assertTrue(
            ActivityParticipation.objects.filter(student=other_student, activity=self.activity).exists()
        )
