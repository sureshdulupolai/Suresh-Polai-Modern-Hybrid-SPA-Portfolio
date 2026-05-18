from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from core.models import Project, Skill, Experience, Achievement, Certification, SiteVisit, ContactSubmission, ErrorLog, SiteSettings

# Views for Admin Panel

def is_superuser(user):
    return user.is_superuser

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        else:
            return redirect('index')

    # Check Lockout Status
    lockout_time_str = request.session.get('lockout_until')
    if lockout_time_str:
        lockout_until = timezone.datetime.fromisoformat(lockout_time_str)
        if timezone.now() < lockout_until:
            remaining = lockout_until - timezone.now()
            seconds_remaining = int(remaining.total_seconds())
            return render(request, 'custom_admin/login.html', {
                'locked_out': True, 
                'remaining_seconds': seconds_remaining
            })
        else:
            # Lockout expired
            if 'lockout_until' in request.session:
                del request.session['lockout_until']
            request.session['login_attempts'] = 0

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        security_key = request.POST.get('security_key', '')
        
        # 1. Validate Security Key
        if security_key != 'developer_suresh_hu':
            attempts = request.session.get('login_attempts', 0) + 1
            request.session['login_attempts'] = attempts
            
            if attempts >= 2:
                lockout_until = timezone.now() + timedelta(hours=24)
                request.session['lockout_until'] = lockout_until.isoformat()
                return render(request, 'custom_admin/login.html', {
                    'locked_out': True,
                    'remaining_seconds': 24 * 60 * 60, # 86400
                    'error': "Maximum attempts exceeded. Locked out for 24 hours."
                })
            
            messages.error(request, f"Invalid Security Key. Attempt {attempts}/2.")
            return render(request, 'custom_admin/login.html', {'form': form})

        # 2. Validate User Credentials
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    # Success - Reset counters
                    request.session['login_attempts'] = 0
                    if 'lockout_until' in request.session:
                        del request.session['lockout_until']
                        
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Only admins can access this area.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'custom_admin/login.html', {'form': form})

def signup_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')

    # Check Lockout Status
    lockout_time_str = request.session.get('signup_lockout_until')
    if lockout_time_str:
        lockout_until = timezone.datetime.fromisoformat(lockout_time_str)
        if timezone.now() < lockout_until:
            remaining = lockout_until - timezone.now()
            seconds_remaining = int(remaining.total_seconds())
            return render(request, 'custom_admin/signup.html', {
                'locked_out': True, 
                'remaining_seconds': seconds_remaining
            })
        else:
            # Lockout expired
            if 'signup_lockout_until' in request.session:
                del request.session['signup_lockout_until']
            request.session['signup_attempts'] = 0

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        security_key = request.POST.get('security_key', '')

        # 1. Validate Security Key
        if security_key != 'developer_suresh_hu':
            attempts = request.session.get('signup_attempts', 0) + 1
            request.session['signup_attempts'] = attempts
            
            if attempts >= 2:
                lockout_until = timezone.now() + timedelta(hours=24)
                request.session['signup_lockout_until'] = lockout_until.isoformat()
                return render(request, 'custom_admin/signup.html', {
                    'locked_out': True,
                    'remaining_seconds': 24 * 60 * 60,
                    'error': "Maximum attempts exceeded. Locked out for 24 hours."
                })
            
            messages.error(request, f"Invalid Security Key. Attempt {attempts}/2.")
            return render(request, 'custom_admin/signup.html', {
                'username': username
            })

        # 2. Validate Other Fields
        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, 'custom_admin/signup.html', {'username': username})
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'custom_admin/signup.html', {'username': username})
        
        from django.contrib.auth.models import User
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'custom_admin/signup.html', {'username': username})

        # 3. Create Superuser
        try:
            user = User.objects.create_superuser(username=username, password=password, email="")
            messages.success(request, "Admin account created successfully! Please login.")
            # Clear attempts on success
            request.session['signup_attempts'] = 0
            return redirect('admin_login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'custom_admin/signup.html', {'username': username})
    
    return render(request, 'custom_admin/signup.html')

def logout_view(request):
    logout(request)
    return redirect('admin_login')

@user_passes_test(is_superuser, login_url='admin_login')
def dashboard(request):
    # Analytics Logic
    total_views = SiteVisit.objects.count()
    
    # Views today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    views_today = SiteVisit.objects.filter(timestamp__gte=today_start).count()
    
    # Source Breakdown
    source_stats = SiteVisit.objects.values('source').annotate(count=Count('source')).order_by('-count')

    context = {
        'total_projects': Project.objects.count(),
        'total_skills': Skill.objects.count(),
        'recent_projects': Project.objects.order_by('-created_at')[:5],
        'total_views': total_views,
        'views_today': views_today,
        'source_stats': source_stats,
        'active_tab': 'dashboard'
    }
    return render(request, 'custom_admin/dashboard.html', context)

@user_passes_test(is_superuser, login_url='admin_login')
def project_list(request):
    projects = Project.objects.all().order_by('order', '-created_at')
    return render(request, 'custom_admin/project_list.html', {'projects': projects, 'active_tab': 'projects'})

@user_passes_test(is_superuser, login_url='admin_login')
def projects_reorder(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('order_'):
                try:
                    project_id = int(key.split('_')[1])
                    order_val = int(value)
                    Project.objects.filter(pk=project_id).update(order=order_val)
                except (ValueError, IndexError):
                    pass
        messages.success(request, "Project ordering saved successfully!")
    return redirect('admin_projects')

@user_passes_test(is_superuser, login_url='admin_login')
def project_create(request):
    if request.method == 'POST':
        from django import forms
        class ProjectForm(forms.ModelForm):
            class Meta:
                model = Project
                fields = '__all__'
        
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created successfully!")
            return redirect('admin_projects')
    else:
        from django import forms
        class ProjectForm(forms.ModelForm):
            class Meta:
                model = Project
                fields = '__all__'
        form = ProjectForm()

    return render(request, 'custom_admin/project_form.html', {'form': form, 'title': 'Add Project', 'active_tab': 'projects'})

@user_passes_test(is_superuser, login_url='admin_login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    from django import forms
    class ProjectForm(forms.ModelForm):
        class Meta:
            model = Project
            fields = '__all__'

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('admin_projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'custom_admin/project_form.html', {'form': form, 'title': 'Edit Project', 'active_tab': 'projects'})

@user_passes_test(is_superuser, login_url='admin_login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully!")
        return redirect('admin_projects')
    return render(request, 'custom_admin/project_confirm_delete.html', {'project': project})

# --- Generic CRUD Helpers ---

def handle_generic_form(request, model, form_class, url_name_base, title, pk=None):
    from django.urls import reverse
    instance = None
    if pk:
        instance = get_object_or_404(model, pk=pk)
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{model.__name__} saved successfully!")
            return redirect(f'{url_name_base}_list')
    else:
        form = form_class(instance=instance)
    
    return render(request, 'custom_admin/generic_form.html', {
        'form': form, 
        'title': title, 
        'cancel_url': reverse(f'{url_name_base}_list')
    })

def handle_generic_delete(request, model, url_name_base, pk):
    from django.urls import reverse
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{model.__name__} deleted successfully!")
        return redirect(f'{url_name_base}_list')
    
    return render(request, 'custom_admin/generic_confirm_delete.html', {
        'object': obj,
        'cancel_url': reverse(f'{url_name_base}_list')
    })

class ItemWrapper:
    def __init__(self, item, base_url):
        self.item = item
        self.base_url = base_url
    def __str__(self):
        return str(self.item)
    @property
    def pk(self):
        return self.item.pk
    @property
    def order(self):
        return getattr(self.item, 'order', 0)
    @property
    def edit_url(self):
        from django.urls import reverse
        return reverse(f'{self.base_url}_edit', kwargs={'pk': self.item.pk})
    @property
    def delete_url(self):
        from django.urls import reverse
        return reverse(f'{self.base_url}_delete', kwargs={'pk': self.item.pk})

def render_generic_list(request, items, title, url_name_base, active_tab=None):
    from django.urls import reverse
    wrapped_items = [ItemWrapper(i, url_name_base) for i in items]
    reorder_url = None
    if title in ['Experience', 'Achievements', 'Certifications']:
        reorder_url = reverse(f'{url_name_base}_reorder')
    return render(request, 'custom_admin/generic_list.html', {
        'items': wrapped_items,
        'model_name_plural': title,
        'add_url': reverse(f'{url_name_base}_add'),
        'reorder_url': reorder_url,
        'active_tab': active_tab
    })

# --- SKILLS ---
from django import forms

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'

@user_passes_test(is_superuser, login_url='admin_login')
def skill_list(request):
    items = Skill.objects.all().order_by('category', '-proficiency_percentage')
    return render_generic_list(request, items, 'Skills', 'admin_skill', active_tab='admin_skill')

@user_passes_test(is_superuser, login_url='admin_login')
def skill_add(request):
    return handle_generic_form(request, Skill, SkillForm, 'admin_skill', 'Add Skill')

@user_passes_test(is_superuser, login_url='admin_login')
def skill_edit(request, pk):
    return handle_generic_form(request, Skill, SkillForm, 'admin_skill', 'Edit Skill', pk)

@user_passes_test(is_superuser, login_url='admin_login')
def skill_delete(request, pk):
    return handle_generic_delete(request, Skill, 'admin_skill', pk)

# --- EXPERIENCE ---
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

@user_passes_test(is_superuser, login_url='admin_login')
def experience_list(request):
    items = Experience.objects.all().order_by('order', '-start_date')
    return render_generic_list(request, items, 'Experience', 'admin_experience', active_tab='admin_experience')

@user_passes_test(is_superuser, login_url='admin_login')
def experience_add(request):
    return handle_generic_form(request, Experience, ExperienceForm, 'admin_experience', 'Add Experience')

@user_passes_test(is_superuser, login_url='admin_login')
def experience_edit(request, pk):
    return handle_generic_form(request, Experience, ExperienceForm, 'admin_experience', 'Edit Experience', pk)

@user_passes_test(is_superuser, login_url='admin_login')
def experience_delete(request, pk):
    return handle_generic_delete(request, Experience, 'admin_experience', pk)

# --- ACHIEVEMENT ---
class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

@user_passes_test(is_superuser, login_url='admin_login')
def achievement_list(request):
    items = Achievement.objects.all().order_by('order', '-date')
    return render_generic_list(request, items, 'Achievements', 'admin_achievement', active_tab='admin_achievement')

@user_passes_test(is_superuser, login_url='admin_login')
def achievement_add(request):
    return handle_generic_form(request, Achievement, AchievementForm, 'admin_achievement', 'Add Achievement')

@user_passes_test(is_superuser, login_url='admin_login')
def achievement_edit(request, pk):
    return handle_generic_form(request, Achievement, AchievementForm, 'admin_achievement', 'Edit Achievement', pk)

@user_passes_test(is_superuser, login_url='admin_login')
def achievement_delete(request, pk):
    return handle_generic_delete(request, Achievement, 'admin_achievement', pk)

# --- CERTIFICATION ---
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = '__all__'

@user_passes_test(is_superuser, login_url='admin_login')
def certification_list(request):
    items = Certification.objects.all().order_by('order', '-year')
    return render_generic_list(request, items, 'Certifications', 'admin_certification', active_tab='admin_certification')

@user_passes_test(is_superuser, login_url='admin_login')
def certification_add(request):
    return handle_generic_form(request, Certification, CertificationForm, 'admin_certification', 'Add Certification')

@user_passes_test(is_superuser, login_url='admin_login')
def certification_edit(request, pk):
    return handle_generic_form(request, Certification, CertificationForm, 'admin_certification', 'Edit Certification', pk)

@user_passes_test(is_superuser, login_url='admin_login')
def certification_delete(request, pk):
    return handle_generic_delete(request, Certification, 'admin_certification', pk)

# --- CONTACT MESSAGES ---

@user_passes_test(is_superuser, login_url='admin_login')
def contact_list(request):
    status_filter = request.GET.get('status')
    if status_filter:
        items = ContactSubmission.objects.filter(status=status_filter).order_by('-created_at')
    else:
        items = ContactSubmission.objects.all().order_by('-created_at')
        
    return render(request, 'custom_admin/contact_list.html', {
        'items': items,
        'active_tab': 'contact',
        'current_filter': status_filter
    })

@user_passes_test(is_superuser, login_url='admin_login')
def contact_status_update(request, pk, status):
    submission = get_object_or_404(ContactSubmission, pk=pk)
    if status in ['Resolved', 'Rejected', 'Pending']:
        submission.status = status
        submission.save()
        messages.success(request, f"Submission marked as {status}.")
    return redirect('admin_contact')

@user_passes_test(is_superuser, login_url='admin_login')
def contact_delete(request, pk):
    submission = get_object_or_404(ContactSubmission, pk=pk)
    if request.method == 'POST':
        submission.delete()
        messages.success(request, "Submission deleted.")
    return redirect('admin_contact')

# --- ERROR LOGS ---

@user_passes_test(is_superuser, login_url='admin_login')
def error_log_list(request):
    logs = ErrorLog.objects.all().order_by('-timestamp')
    return render(request, 'custom_admin/error_log_list.html', {
        'items': logs,
        'active_tab': 'error_logs'
    })

@user_passes_test(is_superuser, login_url='admin_login')
def error_log_delete(request, pk):
    log = get_object_or_404(ErrorLog, pk=pk)
    if request.method == 'POST':
        log.delete()
        messages.success(request, "Error log deleted.")
    return redirect('admin_error_logs')

@user_passes_test(is_superuser, login_url='admin_login')
def error_log_clear(request):
    if request.method == 'POST':
        ErrorLog.objects.all().delete()
        messages.success(request, "All error logs cleared.")
    return redirect('admin_error_logs')


@user_passes_test(is_superuser, login_url='admin_login')
def site_settings_edit(request):
    site_settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        experience_years = request.POST.get('experience_years', '')
        projects_count = request.POST.get('projects_count', '')
        
        if experience_years and projects_count:
            site_settings.experience_years = experience_years
            site_settings.projects_count = projects_count
            site_settings.save()
            messages.success(request, "Site settings updated successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "All fields are required.")
            
    return render(request, 'custom_admin/settings_form.html', {
        'site_settings': site_settings,
        'active_tab': 'admin_settings'
    })


@user_passes_test(is_superuser, login_url='admin_login')
def experience_reorder(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('order_'):
                try:
                    item_id = int(key.split('_')[1])
                    order_val = int(value)
                    Experience.objects.filter(pk=item_id).update(order=order_val)
                except (ValueError, IndexError):
                    pass
        messages.success(request, "Experience ordering saved successfully!")
    return redirect('admin_experience_list')


@user_passes_test(is_superuser, login_url='admin_login')
def achievement_reorder(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('order_'):
                try:
                    item_id = int(key.split('_')[1])
                    order_val = int(value)
                    Achievement.objects.filter(pk=item_id).update(order=order_val)
                except (ValueError, IndexError):
                    pass
        messages.success(request, "Achievement ordering saved successfully!")
    return redirect('admin_achievement_list')


@user_passes_test(is_superuser, login_url='admin_login')
def certification_reorder(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('order_'):
                try:
                    item_id = int(key.split('_')[1])
                    order_val = int(value)
                    Certification.objects.filter(pk=item_id).update(order=order_val)
                except (ValueError, IndexError):
                    pass
        messages.success(request, "Certification ordering saved successfully!")
    return redirect('admin_certification_list')
