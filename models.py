from django.db import models
from apps.students.models import Student


class Activity(models.Model):

    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    # =====================================================
    # DATE AND TIME
    # =====================================================

    event_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    start_time = models.TimeField(
        null=True,
        blank=True
    )

    end_time = models.TimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # LOCATION / ORGANIZER
    # =====================================================

    location = models.CharField(
        max_length=200,
        blank=True
    )

    organizer = models.CharField(
        max_length=200,
        blank=True
    )

    # =====================================================
    # EVENT INFORMATION
    # =====================================================

    event_type = models.CharField(
        max_length=200,
        blank=True
    )

    departments = models.JSONField(
        default=list,
        blank=True
    )

    guest_speaker = models.CharField(
        max_length=200,
        blank=True
    )

    participants = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # =====================================================
    # DOCUMENTS
    # =====================================================

    concept_paper = models.FileField(
        upload_to='activities/concept_papers/',
        null=True,
        blank=True
    )

    permit_file = models.FileField(
        upload_to='activities/permits/',
        null=True,
        blank=True
    )

    # =====================================================
    # ACTIVITY STATUS
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    # =====================================================
    # ARCHIVE
    # =====================================================

    archived = models.BooleanField(
        default=False
    )

    archived_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # CREATED
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            'event_date',
            'start_time',
            'id'
        ]

    def __str__(self):
        return self.title


class ActivityParticipation(models.Model):

    ATTENDANCE_INVITED = 'invited'
    ATTENDANCE_PRESENT = 'present'
    ATTENDANCE_ABSENT = 'absent'
    ATTENDANCE_EXCUSED = 'excused'

    ATTENDANCE_CHOICES = [
        (
            ATTENDANCE_INVITED,
            'Invited'
        ),
        (
            ATTENDANCE_PRESENT,
            'Present'
        ),
        (
            ATTENDANCE_ABSENT,
            'Absent'
        ),
        (
            ATTENDANCE_EXCUSED,
            'Excused'
        ),
    ]

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='activity_participations'
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='participations'
    )

    # =====================================================
    # PARTICIPATION INFORMATION
    # =====================================================

    role = models.CharField(
        max_length=100,
        blank=True
    )

    attendance_status = models.CharField(
        max_length=20,
        choices=ATTENDANCE_CHOICES,
        default=ATTENDANCE_INVITED
    )

    attendance_note = models.CharField(
        max_length=255,
        blank=True
    )

    attendance_marked_at = models.DateTimeField(
        null=True,
        blank=True
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'student',
            'activity'
        )

    def __str__(self):
        return f"{self.student} - {self.activity}"