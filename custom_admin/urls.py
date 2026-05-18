from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='admin_login'),
    path('signup/', views.signup_view, name='admin_signup'),
    path('logout/', views.logout_view, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Project CRUD
    path('projects/', views.project_list, name='admin_projects'),
    path('projects/add/', views.project_create, name='admin_project_add'),
    path('projects/<int:pk>/edit/', views.project_edit, name='admin_project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='admin_project_delete'),
    path('projects/reorder/', views.projects_reorder, name='admin_projects_reorder'),

    # Skill CRUD
    path('skills/', views.skill_list, name='admin_skill_list'),
    path('skills/add/', views.skill_add, name='admin_skill_add'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='admin_skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='admin_skill_delete'),

    # Experience CRUD
    path('experience/', views.experience_list, name='admin_experience_list'),
    path('experience/add/', views.experience_add, name='admin_experience_add'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='admin_experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='admin_experience_delete'),
    path('experience/reorder/', views.experience_reorder, name='admin_experience_reorder'),

    # Achievement CRUD
    path('achievements/', views.achievement_list, name='admin_achievement_list'),
    path('achievements/add/', views.achievement_add, name='admin_achievement_add'),
    path('achievements/<int:pk>/edit/', views.achievement_edit, name='admin_achievement_edit'),
    path('achievements/<int:pk>/delete/', views.achievement_delete, name='admin_achievement_delete'),
    path('achievements/reorder/', views.achievement_reorder, name='admin_achievement_reorder'),

    # Certification CRUD
    path('certifications/', views.certification_list, name='admin_certification_list'),
    path('certifications/add/', views.certification_add, name='admin_certification_add'),
    path('certifications/<int:pk>/edit/', views.certification_edit, name='admin_certification_edit'),
    path('certifications/<int:pk>/delete/', views.certification_delete, name='admin_certification_delete'),
    path('certifications/reorder/', views.certification_reorder, name='admin_certification_reorder'),

    # Contact Messages
    path('contact/', views.contact_list, name='admin_contact'),
    path('contact/<int:pk>/status/<str:status>/', views.contact_status_update, name='admin_contact_status'),
    path('contact/<int:pk>/delete/', views.contact_delete, name='admin_contact_delete'),

    # Error Logs
    path('errors/', views.error_log_list, name='admin_error_logs'),
    path('errors/<int:pk>/delete/', views.error_log_delete, name='admin_error_log_delete'),
    path('errors/clear/', views.error_log_clear, name='admin_error_log_clear'),

    # Site Settings
    path('settings/', views.site_settings_edit, name='admin_settings'),
]
