from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, help_text="Comma-separated technologies")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0, help_text="Ordering index (lower numbers show first)")

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    order = models.IntegerField(default=0, help_text="Ordering index (lower numbers show first)")
    
    class Meta:
        ordering = ['order', '-start_date']
        
    def __str__(self):
        return f"{self.role} at {self.company}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Tools', 'Tools'),
        ('Database', 'Database'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency_percentage = models.IntegerField()

    def __str__(self):
        return self.name

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    order = models.IntegerField(default=0, help_text="Ordering index (lower numbers show first)")

    class Meta:
        ordering = ['order', '-date']

    def __str__(self):
        return self.title

class Certification(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    year = models.IntegerField()
    image = models.ImageField(upload_to='certifications/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Ordering index (lower numbers show first)")

    class Meta:
        ordering = ['order', '-year']

    def __str__(self):
        return self.title

class SiteVisit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=50, default='Direct')
    path = models.CharField(max_length=200)
    user_agent = models.TextField(blank=True, null=True)
    device_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Visit from {self.source} at {self.timestamp}"


class UniqueVisitor(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    first_visited = models.DateTimeField(auto_now_add=True)
    last_visited = models.DateTimeField(auto_now=True)
    visit_count = models.IntegerField(default=1)

    def __str__(self):
        return f"Visitor {self.device_id[:8]} ({self.visit_count} visits)"

class ContactSubmission(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    device_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.status}"

class ErrorLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    error_message = models.TextField()
    traceback = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.method} {self.path} - {self.timestamp}"


class SiteSettings(models.Model):
    experience_years = models.CharField(max_length=50, default="2+")
    projects_count = models.CharField(max_length=50, default="15+")
    satisfaction_rate = models.CharField(max_length=50, default="100%")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Global Site Settings"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
