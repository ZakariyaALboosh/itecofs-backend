from django.db import models


class HomepageStats(models.Model):
    projects_executed = models.PositiveIntegerField()
    field_personnel = models.PositiveIntegerField()
    clients_partners = models.PositiveIntegerField()
    operational_locations = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Homepage data"
        verbose_name_plural = "Homepage data"  # prevents incorrect plural
    def __str__(self):
        return f"HomepageStats #{self.pk}"


class Service(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    first_image = models.ImageField(upload_to='services/', blank=True, null=True)
    second_image = models.ImageField(upload_to='services/', blank=True, null=True)
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services Management" 
    def __str__(self):
        return self.name


class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    service = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Form Submission"
        verbose_name_plural = "Form Submissions"
    def __str__(self):
        return f"ContactForm #{self.pk} - {self.name}"


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_hidden = models.BooleanField(default=False)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "News"
        verbose_name_plural = "News management"   # prevents "Newses"
    def __str__(self):
        return self.title


class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "News Image"
        verbose_name_plural = "News Images"

    def __str__(self):
        return f"{self.news.title} - {self.order}"


class Project(models.Model):
    STATUS_PLANNED = 'planned'
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PLANNED, 'Planned'),
        (STATUS_ACTIVE, 'Active'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    client = models.CharField(max_length=255)
    scope = models.TextField()
    execution = models.JSONField(default=list, help_text='Execution steps as a JSON list')
    outcome = models.TextField()
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Project management"
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
    def __str__(self):
        return f"{self.project.title} - {self.order}"
