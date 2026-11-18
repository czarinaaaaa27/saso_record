from django.utils import timezone
from rest_framework import serializers

from .models import (
    Activity,
    ActivityParticipation,
)


# =========================================================
# ACTIVITY SERIALIZER
# =========================================================

class ActivitySerializer(serializers.ModelSerializer):

    participation_count = serializers.IntegerField(
        read_only=True
    )

    present_count = serializers.IntegerField(
        read_only=True
    )

    attendance_rate = serializers.SerializerMethodField()

    participations = serializers.SerializerMethodField()

    concept_paper_url = serializers.SerializerMethodField()

    permit_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Activity

        fields = [
            # BASIC
            'id',
            'title',
            'description',

            # DATE / TIME
            'event_date',
            'end_date',
            'start_time',
            'end_time',

            # LOCATION / ORGANIZER
            'location',
            'organizer',

            # EVENT INFORMATION
            'event_type',
            'departments',
            'guest_speaker',
            'participants',

            # DOCUMENTS
            'concept_paper',
            'concept_paper_url',
            'permit_file',
            'permit_file_url',

            # STATUS
            'status',

            # ARCHIVE
            'archived',
            'archived_at',
            'created_at',

            # ATTENDANCE
            'participation_count',
            'present_count',
            'attendance_rate',
            'participations',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'archived_at',
            'participation_count',
            'present_count',
            'attendance_rate',
            'participations',
            'concept_paper_url',
            'permit_file_url',
        ]

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        # New activities should never accidentally be
        # archived unless explicitly requested.
        if 'archived' not in validated_data:
            validated_data['archived'] = False

        if not validated_data.get('archived'):
            validated_data['archived_at'] = None

        return Activity.objects.create(
            **validated_data
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        instance,
        validated_data
    ):

        archived = validated_data.get(
            'archived',
            instance.archived
        )

        if archived and not instance.archived:

            validated_data['archived_at'] = (
                timezone.now()
            )

        elif not archived and instance.archived:

            validated_data['archived_at'] = None

        return super().update(
            instance,
            validated_data
        )

    # =====================================================
    # DEPARTMENTS
    # =====================================================

    def validate_departments(self, value):

        if value is None:
            return []

        # Accept:
        #
        # ["BSIT", "BSCS"]
        #
        # OR:
        #
        # "BSIT, BSCS"

        if isinstance(value, str):

            value = [
                item.strip()
                for item in value.split(',')
                if item.strip()
            ]

        if not isinstance(value, list):

            raise serializers.ValidationError(
                'Departments must be a list or '
                'comma-separated text.'
            )

        cleaned = []

        for department in value:

            if department is None:
                continue

            department = str(
                department
            ).strip()

            if (
                department
                and department not in cleaned
            ):
                cleaned.append(
                    department
                )

        return cleaned

    # =====================================================
    # PARTICIPANTS
    # =====================================================

    def validate_participants(self, value):

        if value is None:
            return None

        try:
            value = int(value)
        except (
            TypeError,
            ValueError
        ):
            raise serializers.ValidationError(
                'Participants must be a valid number.'
            )

        if value < 0:

            raise serializers.ValidationError(
                'Participants cannot be negative.'
            )

        return value

    # =====================================================
    # STATUS
    # =====================================================

    def validate_status(self, value):

        allowed = {
            Activity.STATUS_ACTIVE,
            Activity.STATUS_CANCELLED,
        }

        if value not in allowed:

            raise serializers.ValidationError(
                'Status must be either active or cancelled.'
            )

        return value

    # =====================================================
    # DATE / TIME VALIDATION
    # =====================================================

    def validate(self, attrs):

        event_date = attrs.get(
            'event_date'
        )

        end_date = attrs.get(
            'end_date'
        )

        start_time = attrs.get(
            'start_time'
        )

        end_time = attrs.get(
            'end_time'
        )

        # -------------------------------------------------
        # END DATE
        # -------------------------------------------------

        if (
            event_date
            and end_date
            and end_date < event_date
        ):

            raise serializers.ValidationError({
                'end_date':
                    'End date cannot be earlier '
                    'than event date.'
            })

        # -------------------------------------------------
        # END TIME
        # -------------------------------------------------

        if (
            start_time
            and end_time
            and event_date
            and end_date
            and event_date == end_date
            and end_time < start_time
        ):

            raise serializers.ValidationError({
                'end_time':
                    'End time cannot be earlier '
                    'than start time.'
            })

        return attrs

    # =====================================================
    # CONCEPT PAPER URL
    # =====================================================

    def get_concept_paper_url(self, obj):

        request = self.context.get(
            'request'
        )

        if not obj.concept_paper:
            return None

        try:
            url = obj.concept_paper.url
        except ValueError:
            return None

        if request:
            return request.build_absolute_uri(
                url
            )

        return url

    # =====================================================
    # PERMIT FILE URL
    # =====================================================

    def get_permit_file_url(self, obj):

        request = self.context.get(
            'request'
        )

        if not obj.permit_file:
            return None

        try:
            url = obj.permit_file.url
        except ValueError:
            return None

        if request:
            return request.build_absolute_uri(
                url
            )

        return url

    # =====================================================
    # PARTICIPATIONS
    # =====================================================

    def get_participations(self, obj):

        return ActivityParticipationSerializer(
            obj.participations.select_related(
                'student'
            ).all(),
            many=True,
            context=self.context
        ).data

    # =====================================================
    # ATTENDANCE RATE
    # =====================================================

    def get_attendance_rate(self, obj):

        total = getattr(
            obj,
            'participation_count',
            0
        ) or 0

        present = getattr(
            obj,
            'present_count',
            0
        ) or 0

        if total:

            return round(
                (present / total) * 100,
                1
            )

        return 0


# =========================================================
# ACTIVITY PARTICIPATION SERIALIZER
# =========================================================

class ActivityParticipationSerializer(
    serializers.ModelSerializer
):

    student_detail = serializers.SerializerMethodField(
        read_only=True
    )

    activity_title = serializers.CharField(
        source='activity.title',
        read_only=True
    )

    class Meta:

        model = ActivityParticipation

        fields = [
            'id',
            'student',
            'student_detail',
            'activity',
            'activity_title',
            'role',
            'attendance_status',
            'attendance_note',
            'attendance_marked_at',
            'joined_at',
        ]

        read_only_fields = [
            'attendance_marked_at',
            'joined_at',
        ]

    # =====================================================
    # STUDENT DETAIL
    # =====================================================

    def get_student_detail(self, obj):

        student = obj.student

        return {
            'id': student.id,
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'course': student.course,
            'year_level': student.year_level,
            'email': student.email,
        }

    # =====================================================
    # UPDATE ATTENDANCE
    # =====================================================

    def update(
        self,
        instance,
        validated_data
    ):

        attendance_status = validated_data.get(
            'attendance_status',
            instance.attendance_status
        )

        if (
            attendance_status
            == ActivityParticipation.ATTENDANCE_PRESENT
        ):

            validated_data[
                'attendance_marked_at'
            ] = timezone.now()

        elif attendance_status in {
            ActivityParticipation.ATTENDANCE_ABSENT,
            ActivityParticipation.ATTENDANCE_EXCUSED,
            ActivityParticipation.ATTENDANCE_INVITED,
        }:

            validated_data[
                'attendance_marked_at'
            ] = None

        return super().update(
            instance,
            validated_data
        )