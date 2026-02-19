from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('section/<str:section_name>/', views.get_section, name='get_section'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    
    # We also need to handle direct access to "pages" so they render the shell + content
    # For a true SPA without React Router, we often use a catch-all or specific paths pointing to index
    # and then let JS handle the fetch, OR render specific content server-side.
    # To keep it simple: we will point all main nav URLs to index, and let client-side JS/History API handle it? 
    # NO, that causes full reload unless we intercept.
    # But if user Hits Refresh on /about, server must render 'About'.
    # For this iteration, let's just make the server redirection simple:
    # Any of these paths returns the index view, but with context to render the correct initial section.
    
    path('about/', views.index, name='about'),
    path('projects/', views.index, name='projects'),
    # path('experience/', views.index, name='experience'), # Not in main nav but good to have
    path('resume/', views.index, name='resume'),
    path('contact/', views.index, name='contact'),
]
