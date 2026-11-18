from django.db.models import Count, Q

from rest_framework import (
    viewsets,
    filters,
    status
)

from rest_framework.decorators import action

from rest_framework.response import Response

from .models import (
    Activity,
    ActivityParticipation
)

from apps.students.models import Student

from .serializers import (
    ActivitySerializer,
    ActivityParticipationSerializer
)


# =========================================================
# ACTIVITY VIEWSET
# =========================================================

class ActivityViewSet(
    viewsets.ModelViewSet
):

    queryset = Activity.objects.all().prefetch_related(
        'participations__student'
    )

    serializer_class = ActivitySerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = [
        'title',
        'organizer',
        'location'
    ]

    ordering_fields = [
        'event_date',
        'created_at'
    ]

    def get_queryset(self):

        return (
            super()
            .get_queryset()
            .annotate(
                participation_count=Count(
                    'participations',
                    distinct=True
                ),

                present_count=Count(
                    'participations',
                    filter=Q(
                        participations__attendance_status='present'
                    ),
                    distinct=True
                ),
            )
        )

    # =====================================================
    # ARCHIVE ACTIVITY
    # =====================================================

    @action(
        detail=True,
        methods=['patch'],
        url_path='archive'
    )
    def archive(
        self,
        request,
        pk=None
    ):

        activity = self.get_object()

        activity.archived = True

        activity.save(
            update_fields=['archived']
        )

        return Response(
            {
                'message':
                    'Activity archived successfully.',

                'archived': True
            },
            status=status.HTTP_200_OK
        )

    # =====================================================
    # RESTORE ARCHIVED ACTIVITY
    # =====================================================

    @action(
        detail=True,
        methods=['patch'],
        url_path='restore'
    )
    def restore(
        self,
        request,
        pk=None
    ):

        activity = self.get_object()

        activity.archived = False

        activity.save(
            update_fields=['archived']
        )

        return Response(
            {
                'message':
                    'Activity restored successfully.',

                'archived': False
            },
            status=status.HTTP_200_OK
        )

    # =====================================================
    # CANCEL ACTIVITY
    # =====================================================

    @action(
        detail=True,
        methods=['patch'],
        url_path='cancel'
    )
    def cancel(
        self,
        request,
        pk=None
    ):

        activity = self.get_object()

        activity.status = (
            Activity.STATUS_CANCELLED
        )

        activity.save(
            update_fields=['status']
        )

        return Response(
            {
                'message':
                    'Activity cancelled successfully.',

                'status':
                    Activity.STATUS_CANCELLED
            },
            status=status.HTTP_200_OK
        )

    # =====================================================
    # REACTIVATE ACTIVITY
    # =====================================================

    @action(
        detail=True,
        methods=['patch'],
        url_path='reactivate'
    )
    def reactivate(
        self,
        request,
        pk=None
    ):

        activity = self.get_object()

        activity.status = (
            Activity.STATUS_ACTIVE
        )

        activity.save(
            update_fields=['status']
        )

        return Response(
            {
                'message':
                    'Activity reactivated successfully.',

                'status':
                    Activity.STATUS_ACTIVE
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# ACTIVITY PARTICIPATION VIEWSET
# =========================================================

class ActivityParticipationViewSet(
    viewsets.ModelViewSet
):

    queryset = (
        ActivityParticipation.objects
        .select_related(
            'student',
            'activity'
        )
        .all()
    )

    serializer_class = (
        ActivityParticipationSerializer
    )

    # =====================================================
    # BULK ADD STUDENTS
    # =====================================================

    @action(
        detail=False,
        methods=['post'],
        url_path='bulk-add'
    )
    def bulk_add(
        self,
        request
    ):

        activity_id = request.data.get(
            'activity'
        )

        if not activity_id:

            return Response(
                {
                    'detail':
                        'Activity is required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            activity = Activity.objects.get(
                pk=activity_id
            )

        except Activity.DoesNotExist:

            return Response(
                {
                    'detail':
                        'Activity not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # =================================================
        # DO NOT ADD TO ARCHIVED ACTIVITIES
        # =================================================

        if activity.archived:

            return Response(
                {
                    'detail':
                        'Cannot add students to an archived activity.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # =================================================
        # DO NOT ADD TO CANCELLED ACTIVITIES
        # =================================================

        if (
            activity.status
            == Activity.STATUS_CANCELLED
        ):

            return Response(
                {
                    'detail':
                        'Cannot add students to a cancelled activity.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        student_ids = (
            request.data.get('student_ids')
            or []
        )

        if isinstance(
            student_ids,
            str
        ):
            student_ids = [
                student_ids
            ]

        students = Student.objects.all()

        if student_ids:

            students = students.filter(
                id__in=student_ids
            )

        course = str(
            request.data.get(
                'course'
            )
            or ''
        ).strip()

        year_level = str(
            request.data.get(
                'year_level'
            )
            or ''
        ).strip()

        if course:

            students = students.filter(
                course__iexact=course
            )

        if year_level:

            try:

                students = students.filter(
                    year_level=int(
                        year_level
                    )
                )

            except ValueError:

                return Response(
                    {
                        'detail':
                            'Year level must be a number.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        students = list(
            students
        )

        if not students:

            return Response(
                {
                    'detail':
                        'No students matched the selected filters.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created_count = 0
        skipped_count = 0

        for student in students:

            participation, created = (
                ActivityParticipation.objects
                .get_or_create(
                    student=student,
                    activity=activity,
                    defaults={
                        'attendance_status':
                            ActivityParticipation.ATTENDANCE_INVITED,

                        'role': '',

                        'attendance_note': '',
                    }
                )
            )

            if created:

                created_count += 1

            else:

                skipped_count += 1

        return Response(
            {
                'created':
                    created_count,

                'skipped':
                    skipped_count,

                'total_matched':
                    len(students),
            },
            status=status.HTTP_200_OK
        )