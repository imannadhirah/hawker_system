from django.urls import path
from .import views

urlpatterns = [
    
    path("signup/", views.signupManager, name="signupManager"),
    path("login/", views.login, name="login"),
    path("signup/login", views.login, name="login"),
    path('profile/<str:manager_id>/', views.manager_profile, name='manager_profile'),
    path('main_manager_schedule/', views.main_manager_schedule, name='main_manager_schedule'),
    path('schedule/', views.manager_Schedule, name='manager_Schedule'),
    path('mainApproval/', views.mainApproval, name='mainApproval'),

    path('insSignup/', views.inspector_signup, name='inspector_signup'),
    path('insLogin/', views.inspector_login, name='inspector_login'),
    path('mainpage/', views.inspector_mainpage, name='mainpage'),
    path('profile/', views.profile, name='profile'),
    path('inspectlist/', views.inspectlist, name='inspectlist'),
    path('doinspect/', views.doinspect, name='doinspect'),
    path('pastinspect/', views.pastinspect, name='pastinspect'),
    path('emginspect/', views.emginspect, name='emginspect'),
    
    path('approval/<str:hawker_id>', views.Approval, name='approval'),
    path('mainFines/', views.mainFines, name='mainFines'),
    path('fines/<str:inspection_id>', views.manage_fines, name='fines'),
    path('license/', views.license, name='license'),
    path('signupHawker/', views.signupHawker, name='signupHawker'),
    path('loginHawker/', views.loginHawker, name='loginHawker'),
    path('licenseApplied/', views.licenseApplied, name='licenseApplied'),
    path('application_status/', views.application_status, name='application_status'),
    path('digitalLicense/', views.digitalLicense, name='digitalLicense'),
    path('renewal/', views.renewalLicense, name='renewal'),
    path('Hawkerfines/', views.finesRecord, name='finesHawker'),
    path('logout/', views.logout_view, name='logout'),  # Add this URL pattern for logout
    path('renewalApplied/', views.renewalApplied, name='renewalApplied'),
    path('', views.mainscreen, name='mainscreen'),

















]

