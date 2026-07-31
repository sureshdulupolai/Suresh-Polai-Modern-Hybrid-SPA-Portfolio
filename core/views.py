from django.shortcuts import render, get_object_or_404
from .models import Project, Experience, Skill, SiteVisit, Achievement, Certification, SiteSettings, UniqueVisitor
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
    
    # 1. Bot & Monitoring Filter
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    user_agent_lower = user_agent.lower()
    
    bot_keywords = [
        'uptimerobot', 'googlebot', 'bingbot', 'yandexbot', 'baiduspider', 
        'crawler', 'spider', 'robot', 'bot', 'pingdom', 'betteruptime', 
        'statuscake', 'uptime', 'monitoring', 'curl', 'wget', 'python-requests',
        'node-superagent', 'axios', 'go-http-client', 'java/', 'http-client',
        'postman', 'lighthouse', 'gtmetrix', 'semrushbot', 'ahrefsbot', 'siteaudit'
    ]
    is_bot = not user_agent_lower or any(keyword in user_agent_lower for keyword in bot_keywords)

    # 2. Device check / generation (skip for bots to optimize CPU)
    import uuid
    device_id = request.COOKIES.get('device_id')
    set_cookie = False
    if not is_bot and not device_id:
        device_id = str(uuid.uuid4())
        set_cookie = True

    # --- ANALYTICS TRACKING ---
    if not is_bot and not request.headers.get('X-SPA-Request') == 'true' and not request.path.startswith('/custom-admin'):
        
        referer = request.META.get('HTTP_REFERER', '')
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
                user_agent=user_agent,
                device_id=device_id
            )
            
            # Record/Update UniqueVisitor
            visitor, created = UniqueVisitor.objects.get_or_create(
                device_id=device_id,
                defaults={'visit_count': 1}
            )
            if not created:
                visitor.visit_count += 1
                visitor.save()
    # --------------------------

    # Map paths to template names if they differ, or strict 1-to-1
    # For now, we assume section templates exist for 'about', 'projects', 'contact', 'home'
    # 'projects' view logic needs context, so we might need a mapping function.
    
    if request.headers.get('X-SPA-Request') == 'true':
        if active_section == 'projects':
            projects = Project.objects.all().order_by('order', '-created_at')
            response = render(request, 'sections/projects.html', {'projects': projects})
        elif active_section == 'about':
            response = render(request, 'sections/about.html', {
                'site_settings': SiteSettings.get_settings(),
                'achievements': Achievement.objects.all().order_by('order', '-date'),
                'certifications': Certification.objects.all().order_by('order', '-year'),
            })
        elif active_section == 'experience':
            experiences = Experience.objects.all().order_by('order', '-start_date')
            response = render(request, 'sections/experience.html', {'experiences': experiences})
        elif active_section == 'skills':
            skills = Skill.objects.all()
            categories = {}
            for skill in skills:
                if skill.category not in categories:
                    categories[skill.category] = []
                categories[skill.category].append(skill)
            response = render(request, 'sections/skills.html', {'categories': categories})
        elif active_section == 'resume':
            skills = Skill.objects.all()
            categories = {}
            for skill in skills:
                if skill.category not in categories:
                    categories[skill.category] = []
                categories[skill.category].append(skill)
            response = render(request, 'sections/resume.html', {
                'experiences': Experience.objects.all().order_by('order', '-start_date'),
                'categories': categories,
                'achievements': Achievement.objects.all().order_by('order', '-date'),
                'certifications': Certification.objects.all().order_by('order', '-year')
            })
        else:
            # Simple static sections
            if active_section == 'home':
                response = render(request, 'sections/hero.html', {
                    'site_settings': SiteSettings.get_settings()
                })
            else:
                try:
                    response = render(request, f'sections/{active_section}.html')
                except:
                    response = render(request, 'sections/hero.html', {
                        'site_settings': SiteSettings.get_settings()
                    }) # Fallback
        
        if set_cookie:
            response.set_cookie('device_id', device_id, max_age=31536000, httponly=True, samesite='Lax')
        return response
    
    # Context data helpers
    def get_common_context():
        skills = Skill.objects.all()
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
            
        return {
            'projects': Project.objects.all().order_by('order', '-created_at'),
            'experiences': Experience.objects.all().order_by('order', '-start_date'),
            'categories': categories,
            'achievements': Achievement.objects.all().order_by('order', '-date'),
            'certifications': Certification.objects.all().order_by('order', '-year'),
            'site_settings': SiteSettings.get_settings(),
            'resume': Resume.objects.order_by('-updated_at').first(),
        }

    # Full page load
    context = {'active_section': active_section}
    context.update(get_common_context())
        
    response = render(request, 'index.html', context)
    if set_cookie:
        response.set_cookie('device_id', device_id, max_age=31536000, httponly=True, samesite='Lax')
    return response

def get_section(request, section_name):
    """
    Returns theHTML partial for a specific section.
    """
    if section_name == 'home':
        # Hero section
        return render(request, 'sections/hero.html', {
            'site_settings': SiteSettings.get_settings()
        })
    
    elif section_name == 'about':
        return render(request, 'sections/about.html', {
            'achievements': Achievement.objects.all().order_by('order', '-date'),
            'certifications': Certification.objects.all().order_by('order', '-year'),
            'site_settings': SiteSettings.get_settings(),
        })
    
    elif section_name == 'projects':
        projects = Project.objects.all().order_by('order', '-created_at')
        return render(request, 'sections/projects.html', {'projects': projects})
    
    elif section_name == 'experience':
        experiences = Experience.objects.all().order_by('order', '-start_date')
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
            
        resume_obj = Resume.objects.order_by('-updated_at').first()
            
        return render(request, 'sections/resume.html', {
            'experiences': Experience.objects.all().order_by('order', '-start_date'),
            'categories': categories,
            'achievements': Achievement.objects.all().order_by('order', '-date'),
            'certifications': Certification.objects.all().order_by('order', '-year'),
            'resume': resume_obj
        })
    else:
        raise Http404("Section not found")

import os
from django.http import FileResponse
from .models import Resume, ResumeDownload

def download_resume(request):
    resume = Resume.objects.order_by('-updated_at').first()
    if not resume or not resume.file:
        raise Http404("Resume not found.")
        
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
        
    download_record, created = ResumeDownload.objects.get_or_create(
        ip_address=ip,
        defaults={'download_count': 1}
    )
    if not created:
        download_record.download_count += 1
        download_record.save()
        
    filename = f"{resume.title}.pdf" if not resume.title.lower().endswith('.pdf') else resume.title
    return FileResponse(open(resume.file.path, 'rb'), as_attachment=True, filename=filename)

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

from django.views.decorators.http import require_GET
from django.http import HttpResponse

@require_GET
def robots_view(request):
    """
    Renders a standard-compliant robots.txt.
    Bypasses security protections for friendly bots and directs crawlers to sitemap.xml.
    """
    domain = request.build_absolute_uri('/')
    content = f"""User-agent: *
Allow: /
Disallow: /custom-admin/

Sitemap: {domain}sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain")

@require_GET
def sitemap_view(request):
    """
    Generates a clean, fully-dynamic sitemap.xml at runtime.
    Lists key SPA section pages and updates their relative crawler weights.
    """
    domain = request.build_absolute_uri('/')
    urls = [
        {'loc': f"{domain}", 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{domain}about/", 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': f"{domain}projects/", 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{domain}resume/", 'changefreq': 'weekly', 'priority': '0.7'},
        {'loc': f"{domain}contact/", 'changefreq': 'weekly', 'priority': '0.8'},
    ]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml_content += '  <url>\n'
        xml_content += f"    <loc>{url['loc']}</loc>\n"
        xml_content += f"    <changefreq>{url['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{url['priority']}</priority>\n"
        xml_content += '  </url>\n'
    xml_content += '</urlset>'
    return HttpResponse(xml_content, content_type="application/xml")

@require_GET
def google_verification_view(request):
    """
    Serves the Google Search Console HTML verification file dynamic content.
    """
    content = "google-site-verification: google5c65749617527eda.html"
    return HttpResponse(content, content_type="text/html")
