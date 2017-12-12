from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required, permission_required

from . import views
from .user_views import AdministratorListView, AdministratorCreationView, AdministratorUpdateView, AdministratorDeleteView
from .user_views import TeacherListView, TeacherCreationView, TeacherUpdateView, TeacherDeleteView
from .user_views import StudentListView, StudentCreationView, StudentUpdateView, StudentDeleteView
from .user_views import StudentDetailView
from .user_views import SelfUpdateView
from .views import MentoringRelationshipListView, MentoringRelationshipCreationView, MentoringRelationshipUpdateView, MentoringRelationshipDeleteView
from .views import MentoringRecordListView, MentoringRecordCreationView, MentoringRecordUpdateView, MentoringRecordDeleteView
from .views import MissionListView, MissionCreationView, MissionUpdateView, MissionDetailView, MissionDeleteView

app_name = 'dashboard'
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.overview, name='overview'),

    url(r'administrator/$', 
        permission_required('dashboard.view_administrator')(AdministratorListView.as_view()), 
        name='AdministratorListView'),
    url(r'administrator/creation/$', 
        permission_required('dashboard.add_administrator')(AdministratorCreationView.as_view()), 
        name='AdministratorCreationView'),
    url(r'administrator/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_administrator')(AdministratorUpdateView.as_view()), 
        name='AdministratorUpdateView'),
    url(r'administrator/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_administrator')(AdministratorDeleteView.as_view()), 
        name='AdministratorDeleteView'),

    url(r'teacher/$', 
        permission_required('dashboard.view_teacher')(TeacherListView.as_view()), 
        name='TeacherListView'),
    url(r'teacher/creation/$', 
        permission_required('dashboard.add_teacher')(TeacherCreationView.as_view()), 
        name='TeacherCreationView'),
    url(r'teacher/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_teacher')(TeacherUpdateView.as_view()), 
        name='TeacherUpdateView'),
    url(r'teacher/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_teacher')(TeacherDeleteView.as_view()), 
        name='TeacherDeleteView'),

    url(r'student/$', 
        permission_required('dashboard.view_student')(StudentListView.as_view()), 
        name='StudentListView'),
    url(r'student/(?P<pk>[0-9]+)/detail/$', 
        permission_required('dashboard.view_student')(StudentDetailView.as_view()), 
        name='StudentDetailView'),
    url(r'student/creation/$', 
        permission_required('dashboard.add_student')(StudentCreationView.as_view()), 
        name='StudentCreationView'),
    url(r'student/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_student')(StudentUpdateView.as_view()), 
        name='StudentUpdateView'),
    url(r'student/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_student')(StudentDeleteView.as_view()), 
        name='StudentDeleteView'),

    url(r'mentoring/relationship/$', 
        permission_required('dashboard.view_mentoringrelationship')(MentoringRelationshipListView.as_view()), 
        name='MentoringRelationshipListView'),
    url(r'mentoring/relationship/creation/$', 
        permission_required('dashboard.add_mentoringrelationship')(MentoringRelationshipCreationView.as_view()), 
        name='MentoringRelationshipCreationView'),
    url(r'mentoring/relationship/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_mentoringrelationship')(MentoringRelationshipUpdateView.as_view()), 
        name='MentoringRelationshipUpdateView'),
    url(r'mentoring/relationship/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_mentoringrelationship')(MentoringRelationshipDeleteView.as_view()), 
        name='MentoringRelationshipDeleteView'),

    url(r'mentoring/record/$', 
        permission_required('dashboard.view_mentoringrecord')(MentoringRecordListView.as_view()), 
        name='MentoringRecordListView'),
    url(r'mentoring/record/creation/$', 
        permission_required('dashboard.add_mentoringrecord')(MentoringRecordCreationView.as_view()), 
        name='MentoringRecordCreationView'),
    url(r'mentoring/record/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_mentoringrecord')(MentoringRecordUpdateView.as_view()), 
        name='MentoringRecordUpdateView'),
    url(r'mentoring/record/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_mentoringrecord')(MentoringRecordDeleteView.as_view()), 
        name='MentoringRecordDeleteView'),

    url(r'mission/$', 
        permission_required('dashboard.view_mission')(MissionListView.as_view()), 
        name='MissionListView'),
    url(r'mission/creation/$', 
        permission_required('dashboard.add_mission')(MissionCreationView.as_view()), 
        name='MissionCreationView'),
    url(r'mission/(?P<pk>[0-9]+)/update/$', 
        permission_required('dashboard.change_mission')(MissionUpdateView.as_view()), 
        name='MissionUpdateView'),
    url(r'mission/(?P<pk>[0-9]+)/detail/$', 
        permission_required('dashboard.view_mission')(MissionDetailView.as_view()), 
        name='MissionDetailView'),
    url(r'mission/(?P<pk>[0-9]+)/delete/$', 
        permission_required('dashboard.delete_mission')(MissionDeleteView.as_view()), 
        name='MissionDeleteView'),

    url(r'settings/$', 
        SelfUpdateView.as_view(), 
        name='SelfUpdateView'),
]
