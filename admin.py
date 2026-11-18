from django.contrib import admin
from .models import Activity, ActivityParticipation


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display  = ('title', 'event_date', 'location', 'organizer')
    search_fields = ('title', 'organizer', 'location')
    ordering      = ('event_date',)


@admin.register(ActivityParticipation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display  = ('student', 'activity', 'role')
    list_filter   = ('activity',)
    search_fields = ('student__last_name', 'student__student_id')
