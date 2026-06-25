from rest_framework import viewsets

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


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.prefetch_related('images').all()
    serializer_class = NewsSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.prefetch_related('images').all()
    serializer_class = ProjectSerializer


class SupplierRegistrationViewSet(viewsets.ModelViewSet):
    queryset = SupplierRegistration.objects.all()
    serializer_class = SupplierRegistrationSerializer
