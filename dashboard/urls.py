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
from .views import SchoolApplicationCountryListView, SchoolApplicationCountryCreationView, SchoolApplicationCountryUpdateView, SchoolApplicationCountryDeleteView
from .views import SchoolApplicationSchoolListView, SchoolApplicationSchoolCreationView, SchoolApplicationSchoolUpdateView, SchoolApplicationSchoolDeleteView
from .views import SchoolApplicationCollegeListView, SchoolApplicationCollegeCreationView, SchoolApplicationCollegeUpdateView, SchoolApplicationCollegeDeleteView
from .views import SchoolApplicationMajorListView, SchoolApplicationMajorCreationView, SchoolApplicationMajorUpdateView, SchoolApplicationMajorDeleteView
from .views import SchoolApplicationDegreeListView, SchoolApplicationDegreeCreationView, SchoolApplicationDegreeUpdateView, SchoolApplicationDegreeDeleteView
from .views import SchoolApplicationDegreeDetailView

app_name = 'dashboard'
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.overview, name='overview'),

    url(r'administrator/$', 
        login_required(permission_required('dashboard.view_administrator')(
            AdministratorListView.as_view())), 
        name='AdministratorListView'),
    url(r'administrator/creation/$', 
        login_required(permission_required('dashboard.add_administrator')(
            AdministratorCreationView.as_view())), 
        name='AdministratorCreationView'),
    url(r'administrator/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_administrator')(
            AdministratorUpdateView.as_view())), 
        name='AdministratorUpdateView'),
    url(r'administrator/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_administrator')(
            AdministratorDeleteView.as_view())), 
        name='AdministratorDeleteView'),

    url(r'teacher/$', 
        login_required(permission_required('dashboard.view_teacher')(
            TeacherListView.as_view())), 
        name='TeacherListView'),
    url(r'teacher/creation/$', 
        login_required(permission_required('dashboard.add_teacher')(
            TeacherCreationView.as_view())), 
        name='TeacherCreationView'),
    url(r'teacher/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_teacher')(
            TeacherUpdateView.as_view())), 
        name='TeacherUpdateView'),
    url(r'teacher/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_teacher')(
            TeacherDeleteView.as_view())), 
        name='TeacherDeleteView'),

    url(r'student/$', 
        login_required(permission_required('dashboard.view_student')(
            StudentListView.as_view())), 
        name='StudentListView'),
    url(r'student/(?P<pk>[0-9]+)/detail/$', 
        login_required(permission_required('dashboard.view_student')(
            StudentDetailView.as_view())), 
        name='StudentDetailView'),
    url(r'student/creation/$', 
        login_required(permission_required('dashboard.add_student')(
            StudentCreationView.as_view())), 
        name='StudentCreationView'),
    url(r'student/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_student')(
            StudentUpdateView.as_view())), 
        name='StudentUpdateView'),
    url(r'student/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_student')(
            StudentDeleteView.as_view())), 
        name='StudentDeleteView'),

    url(r'mentoring/relationship/$', 
        login_required(permission_required('dashboard.view_mentoringrelationship')(
            MentoringRelationshipListView.as_view())), 
        name='MentoringRelationshipListView'),
    url(r'mentoring/relationship/creation/$', 
        login_required(permission_required('dashboard.add_mentoringrelationship')(
            MentoringRelationshipCreationView.as_view())), 
        name='MentoringRelationshipCreationView'),
    url(r'mentoring/relationship/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_mentoringrelationship')(
            MentoringRelationshipUpdateView.as_view())), 
        name='MentoringRelationshipUpdateView'),
    url(r'mentoring/relationship/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_mentoringrelationship')(
            MentoringRelationshipDeleteView.as_view())), 
        name='MentoringRelationshipDeleteView'),

    url(r'mentoring/record/$', 
        login_required(permission_required('dashboard.view_mentoringrecord')(
            MentoringRecordListView.as_view())), 
        name='MentoringRecordListView'),
    url(r'mentoring/record/creation/$', 
        login_required(permission_required('dashboard.add_mentoringrecord')(
            MentoringRecordCreationView.as_view())), 
        name='MentoringRecordCreationView'),
    url(r'mentoring/record/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_mentoringrecord')(
            MentoringRecordUpdateView.as_view())), 
        name='MentoringRecordUpdateView'),
    url(r'mentoring/record/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_mentoringrecord')(
            MentoringRecordDeleteView.as_view())), 
        name='MentoringRecordDeleteView'),

    url(r'mission/$', 
        login_required(permission_required('dashboard.view_mission')(
            MissionListView.as_view())), 
        name='MissionListView'),
    url(r'mission/creation/$', 
        login_required(permission_required('dashboard.add_mission')(
            MissionCreationView.as_view())), 
        name='MissionCreationView'),
    url(r'mission/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_mission')(
            MissionUpdateView.as_view())), 
        name='MissionUpdateView'),
    url(r'mission/(?P<pk>[0-9]+)/detail/$', 
        login_required(permission_required('dashboard.view_mission')(
            MissionDetailView.as_view())), 
        name='MissionDetailView'),
    url(r'mission/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_mission')(
            MissionDeleteView.as_view())), 
        name='MissionDeleteView'),

    url(r'school_application/country/$', 
        login_required(permission_required('dashboard.view_applycountry')(
            SchoolApplicationCountryListView.as_view())), 
        name='SchoolApplicationCountryListView'),
    url(r'school_application/country/creation/$', 
        login_required(permission_required('dashboard.add_applycountry')(
            SchoolApplicationCountryCreationView.as_view())), 
        name='SchoolApplicationCountryCreationView'),
    url(r'school_application/country/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_applycountry')(
            SchoolApplicationCountryUpdateView.as_view())), 
        name='SchoolApplicationCountryUpdateView'),
    url(r'school_application/country/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_applycountry')(
            SchoolApplicationCountryDeleteView.as_view())), 
        name='SchoolApplicationCountryDeleteView'),

    url(r'school_application/school/$', 
        login_required(permission_required('dashboard.view_applyschool')(
            SchoolApplicationSchoolListView.as_view())), 
        name='SchoolApplicationSchoolListView'),
    url(r'school_application/school/creation/$', 
        login_required(permission_required('dashboard.add_applyschool')(
            SchoolApplicationSchoolCreationView.as_view())), 
        name='SchoolApplicationSchoolCreationView'),
    url(r'school_application/school/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_applyschool')(
            SchoolApplicationSchoolUpdateView.as_view())), 
        name='SchoolApplicationSchoolUpdateView'),
    url(r'school_application/school/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_applyschool')(
            SchoolApplicationSchoolDeleteView.as_view())), 
        name='SchoolApplicationSchoolDeleteView'),

    url(r'school_application/college/$', 
        login_required(permission_required('dashboard.view_applycollege')(
            SchoolApplicationCollegeListView.as_view())), 
        name='SchoolApplicationCollegeListView'),
    url(r'school_application/college/creation/$', 
        login_required(permission_required('dashboard.add_applycollege')(
            SchoolApplicationCollegeCreationView.as_view())), 
        name='SchoolApplicationCollegeCreationView'),
    url(r'school_application/college/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_applycollege')(
            SchoolApplicationCollegeUpdateView.as_view())), 
        name='SchoolApplicationCollegeUpdateView'),
    url(r'school_application/college/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_applycollege')(
            SchoolApplicationCollegeDeleteView.as_view())), 
        name='ApplyCollegeDeleteView'),
    
    url(r'school_application/major/$', 
        login_required(permission_required('dashboard.view_applymajor')(
            SchoolApplicationMajorListView.as_view())), 
        name='SchoolApplicationMajorListView'),
    url(r'school_application/major/creation/$', 
        login_required(permission_required('dashboard.add_applymajor')(
            SchoolApplicationMajorCreationView.as_view())), 
        name='SchoolApplicationMajorCreationView'),
    url(r'school_application/major/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_applymajor')(
            SchoolApplicationMajorUpdateView.as_view())), 
        name='SchoolApplicationMajorUpdateView'),
    url(r'school_application/major/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_applymajor')(
            SchoolApplicationMajorDeleteView.as_view())), 
        name='SchoolApplicationMajorDeleteView'),
    
    url(r'school_application/degree/$', 
        login_required(permission_required('dashboard.view_applydegree')(
            SchoolApplicationDegreeListView.as_view())), 
        name='SchoolApplicationDegreeListView'),
    url(r'school_application/degree/(?P<pk>[0-9]+)/detail/$', 
        login_required(permission_required('dashboard.view_applydegree')(
            SchoolApplicationDegreeDetailView.as_view())), 
        name='SchoolApplicationDegreeDetailView'),
    url(r'school_application/degree/creation/$', 
        login_required(permission_required('dashboard.add_applydegree')(
            SchoolApplicationDegreeCreationView.as_view())), 
        name='SchoolApplicationDegreeCreationView'),
    url(r'school_application/degree/(?P<pk>[0-9]+)/update/$', 
        login_required(permission_required('dashboard.change_applydegree')(
            SchoolApplicationDegreeUpdateView.as_view())), 
        name='SchoolApplicationDegreeUpdateView'),
    url(r'school_application/degree/(?P<pk>[0-9]+)/delete/$', 
        login_required(permission_required('dashboard.delete_applydegree')(
            SchoolApplicationDegreeDeleteView.as_view())), 
        name='SchoolApplicationDegreeDeleteView'),

    url(r'settings/$', 
        login_required(SelfUpdateView.as_view()), 
        name='SelfUpdateView'),
]
