from rest_framework import viewsets

from .emails import notify_contact_submission, notify_supplier_registration

from .models import ContactForm, HomepageStats, News, Project, Service, SupplierRegistration
from .serializers import (
    ContactFormSerializer,
    HomepageStatsSerializer,
    NewsSerializer,
    ProjectSerializer,
    ServiceSerializer,
    SupplierRegistrationSerializer,
)


class HomepageStatsViewSet(viewsets.ModelViewSet):
    queryset = HomepageStats.objects.all()
    serializer_class = HomepageStatsSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer




class ContactFormViewSet(viewsets.ModelViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer

    def perform_create(self, serializer):
        contact_form = serializer.save()
        notify_contact_submission(contact_form)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.prefetch_related('images').all()
    serializer_class = NewsSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('images').all()
    serializer_class = ProjectSerializer


class SupplierRegistrationViewSet(viewsets.ModelViewSet):
    queryset = SupplierRegistration.objects.all()
    serializer_class = SupplierRegistrationSerializer

    def perform_create(self, serializer):
        registration = serializer.save()
        notify_supplier_registration(registration)
