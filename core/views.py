from django.shortcuts import render, get_object_or_404
from .models import Project, Experience, Skill, SiteVisit, Achievement, Certification
from django.http import Http404

def index(request):
    """
    Renders the main SPA shell. 
    Determines the active section based on the URL path.
    If X-SPA-Request header is present, returns only the section partial.
    Also records site visits for analytics.
    """
    path = request.path.strip('/')
    # Split path to get the first segment, e.g., 'resume' from 'resume/' or 'resume/details'
    path_segments = path.split('/')
    active_section = path_segments[0] if path and path_segments else 'home'
    
    # --- ANALYTICS TRACKING ---
    if not request.headers.get('X-SPA-Request') == 'true' and not request.path.startswith('/custom-admin'):
        # Only track full page loads (initial visits) or maybe specific interactions if desired.
        # We'll track all non-SPA requests to the main index as "Visits"
        
        referer = request.META.get('HTTP_REFERER', '')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        source = 'Direct'
        
        if 'whatsapp' in referer.lower():
            source = 'WhatsApp'
        elif 'linkedin' in referer.lower():
            source = 'LinkedIn'
        elif 'twitter' in referer.lower() or 't.co' in referer.lower():
            source = 'Twitter'
        elif 'facebook' in referer.lower():
            source = 'Facebook'
        elif 'instagram' in referer.lower():
            source = 'Instagram'
        elif 'google' in referer.lower():
            source = 'Google'
        elif referer:
            # Parse domain if possible, or just use 'Other'
            from urllib.parse import urlparse
            try:
                domain = urlparse(referer).netloc
                if domain:
                    source = domain
                else:
                    source = 'Other'
            except:
                source = 'Other'

        # Basic separate of dev/admin (optional, but good for accuracy)
        if not request.user.is_superuser:
            SiteVisit.objects.create(
                source=source,
                path=request.path,
                user_agent=user_agent
            )
    # --------------------------

    # Map paths to template names if they differ, or strict 1-to-1
    # For now, we assume section templates exist for 'about', 'projects', 'contact', 'home'
    # 'projects' view logic needs context, so we might need a mapping function.
    
    if request.headers.get('X-SPA-Request') == 'true':
        if active_section == 'projects':
            projects = Project.objects.filter(is_featured=True).order_by('-created_at')
            if not projects.exists():
                projects = Project.objects.all().order_by('-created_at')
            return render(request, 'sections/projects.html', {'projects': projects})
        elif active_section == 'experience':
            experiences = Experience.objects.all().order_by('-start_date')
            return render(request, 'sections/experience.html', {'experiences': experiences})
        elif active_section == 'skills':
            skills = Skill.objects.all()
            categories = {}
            for skill in skills:
                if skill.category not in categories:
                    categories[skill.category] = []
                categories[skill.category].append(skill)
            return render(request, 'sections/skills.html', {'categories': categories})
        elif active_section == 'resume':
            skills = Skill.objects.all()
            categories = {}
            for skill in skills:
                if skill.category not in categories:
                    categories[skill.category] = []
                categories[skill.category].append(skill)
            return render(request, 'sections/resume.html', {
                'experiences': Experience.objects.all().order_by('-start_date'),
                'categories': categories,
                'achievements': Achievement.objects.all(),
                'certifications': Certification.objects.all().order_by('-year')
            })
        
        # Simple static sections
        try:
            return render(request, f'sections/{active_section}.html')
        except:
            return render(request, 'sections/hero.html') # Fallback
    
    # Context data helpers
    def get_common_context():
        skills = Skill.objects.all()
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
            
        return {
            'projects': Project.objects.filter(is_featured=True).order_by('-created_at') or Project.objects.all().order_by('-created_at'),
            'experiences': Experience.objects.all().order_by('-start_date'),
            'categories': categories,
            'achievements': Achievement.objects.all(),
            'certifications': Certification.objects.all().order_by('-year'),
        }

    # Full page load
    context = {'active_section': active_section}
    context.update(get_common_context())
        
    return render(request, 'index.html', context)

def get_section(request, section_name):
    """
    Returns theHTML partial for a specific section.
    """
    if section_name == 'home':
        # Hero section
        return render(request, 'sections/hero.html')
    
    elif section_name == 'about':
        return render(request, 'sections/about.html', {
            'achievements': Achievement.objects.all(),
            'certifications': Certification.objects.all().order_by('-year')
        })
    
    elif section_name == 'projects':
        projects = Project.objects.filter(is_featured=True).order_by('-created_at')
        if not projects.exists(): 
             # Fallback if no featured, show all or just empty
             projects = Project.objects.all().order_by('-created_at')
        return render(request, 'sections/projects.html', {'projects': projects})
    
    elif section_name == 'experience':
        experiences = Experience.objects.all().order_by('-start_date')
        return render(request, 'sections/experience.html', {'experiences': experiences})
    
    elif section_name == 'skills':
        skills = Skill.objects.all()
        # Grouping by category
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
        return render(request, 'sections/skills.html', {'categories': categories})
    
    elif section_name == 'contact':
        return render(request, 'sections/contact.html')

    elif section_name == 'resume':
        skills = Skill.objects.all()
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
            
        return render(request, 'sections/resume.html', {
            'experiences': Experience.objects.all().order_by('-start_date'),
            'categories': categories,
            'achievements': Achievement.objects.all(),
            'certifications': Certification.objects.all().order_by('-year')
        })
        
    else:
        raise Http404("Section not found")

import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ContactSubmission

@require_POST
def contact_submit(request):
    # 1. Device Check
    device_id = request.COOKIES.get('device_id')
    if not device_id:
        device_id = str(uuid.uuid4())
        set_cookie = True
    else:
        set_cookie = False

    # 2. Check for Pending Submissions from this device
    # If device_id was just created, obviously no pending, but if existed:
    if not set_cookie:
        pending_exists = ContactSubmission.objects.filter(device_id=device_id, status='Pending').exists()
        if pending_exists:
            return JsonResponse({
                'status': 'error',
                'message': 'You have a pending submission. Please wait for it to be processed before submitting again.'
            }, status=403)

    # 3. Process Form Data
    name = request.POST.get('name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    message = request.POST.get('message')

    if not name or not message:
         return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=400)
    
    if not email and not mobile:
         return JsonResponse({'status': 'error', 'message': 'Please provide either Email or Mobile.'}, status=400)

    # 4. Save
    submission = ContactSubmission.objects.create(
        name=name,
        email=email,
        mobile=mobile,
        message=message,
        device_id=device_id
    )

    response = JsonResponse({
        'status': 'success', 
        'message': 'Message sent successfully! We will get back to you soon.'
    })

    # 5. Set Cookie if needed (expires in 1 year)
    if set_cookie:
        response.set_cookie('device_id', device_id, max_age=31536000, httponly=True, samesite='Lax')
    
    return response
