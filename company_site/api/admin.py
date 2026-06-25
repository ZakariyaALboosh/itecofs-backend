from django.contrib import admin
from django import forms
from .models import ContactForm, HomepageStats, News, NewsImage, Project, ProjectImage, Service, SupplierRegistration


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_hidden', 'created_at')
    list_filter = ('is_hidden', 'created_at')
    search_fields = ('title', 'author')
    inlines = [NewsImageInline]


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1



class ProjectAdminForm(forms.ModelForm):
    execution = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 8,
            "placeholder": "Enter one execution step per line",
        }),
        help_text="Enter each execution step on a new line.",
        required=False,
        label="Execution steps",
    )

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Convert existing JSON list into one-step-per-line text
        if self.instance and isinstance(self.instance.execution, list):
            self.initial["execution"] = "\n".join(self.instance.execution)

    def clean_execution(self):
        execution_text = self.cleaned_data.get("execution", "")

        # Convert lines into a clean Python list
        steps = [
            line.strip()
            for line in execution_text.splitlines()
            if line.strip()
        ]

        return steps


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

    list_display = ("title", "status", "client")
    list_filter = ("status",)
    search_fields = ("title", "client")
    inlines = [ProjectImageInline]

@admin.register(HomepageStats)
class HomepageStatsAdmin(admin.ModelAdmin):
    list_display = (
        'projects_executed',
        'field_personnel',
        'clients_partners',
        'operational_locations',
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'service', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'service')
    list_filter = ('created_at',)


@admin.register(SupplierRegistration)
class SupplierRegistrationAdmin(admin.ModelAdmin):
    list_display = ('vendor_name', 'country', 'cr_number', 'fp_name', 'fp_email', 'created_at')
    search_fields = ('vendor_name', 'country', 'cr_number', 'fp_name', 'fp_email', 'email')
    list_filter = ('country', 'operates_libya', 'created_at')
    readonly_fields = ('created_at',)
