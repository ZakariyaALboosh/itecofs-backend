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



class SupplierRegistration(models.Model):
    vendor_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    cr_number = models.CharField(max_length=100)
    est_year = models.CharField(max_length=20)
    supplier_type = models.JSONField(default=list, help_text='Selected supplier types as a JSON list')
    hq_address = models.TextField()
    operates_libya = models.CharField(max_length=10)
    cr_certificate = models.FileField(upload_to='supplier_registrations/cr_certificates/')
    organisation_chart = models.FileField(upload_to='supplier_registrations/organisation_charts/')
    company_profile = models.FileField(upload_to='supplier_registrations/company_profiles/')

    fp_name = models.CharField(max_length=255)
    fp_position = models.CharField(max_length=255)
    fp_phone = models.CharField(max_length=50)
    fp_email = models.EmailField()

    tax_registration_certificate = models.FileField(upload_to='supplier_registrations/tax_certificates/')
    vat_registration_certificate = models.FileField(upload_to='supplier_registrations/vat_certificates/', blank=True, null=True)

    bank_name = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    iban = models.CharField(max_length=100)
    swift = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    branch_address = models.CharField(max_length=255)
    currency = models.CharField(max_length=50)

    registration_type = models.JSONField(default=list, help_text='Selected registration types as a JSON list')
    product_types = models.TextField()
    warranty_terms = models.TextField()
    support_info = models.TextField()

    certs = models.JSONField(default=dict, help_text='Certification yes/no values keyed by certification name')
    iso9001_certificate = models.FileField(upload_to='supplier_registrations/certifications/', blank=True, null=True)
    iso14001_certificate = models.FileField(upload_to='supplier_registrations/certifications/', blank=True, null=True)
    iso45001_certificate = models.FileField(upload_to='supplier_registrations/certifications/', blank=True, null=True)
    apiq1_certificate = models.FileField(upload_to='supplier_registrations/certifications/', blank=True, null=True)
    apiq2_certificate = models.FileField(upload_to='supplier_registrations/certifications/', blank=True, null=True)

    lead_time = models.CharField(max_length=255)
    export_ports = models.CharField(max_length=255)
    logistics_address = models.TextField()

    accepted = models.BooleanField(default=False)
    representative = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Supplier Registration'
        verbose_name_plural = 'Supplier Registration Management'

    def __str__(self):
        return f'SupplierRegistration #{self.pk} - {self.vendor_name}'
