from django.urls import path
from . import views

urlpatterns = [
    path('robots.txt', views.robots_view, name='robots'),
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('google5c65749617527eda.html', views.google_verification_view, name='google_verification'),
    path('', views.index, name='index'),
    path('section/<str:section_name>/', views.get_section, name='get_section'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('resume/download/', views.download_resume, name='download_resume'),

    path('about/', views.index, name='about'),
    path('projects/', views.index, name='projects'),
    # path('experience/', views.index, name='experience'), # Not in main nav but good to have
    path('resume/', views.index, name='resume'),
    path('contact/', views.index, name='contact'),
]
