from rest_framework.routers import DefaultRouter

from .views import ContactFormViewSet, HomepageStatsViewSet, NewsViewSet, ProjectViewSet, ServiceViewSet

router = DefaultRouter()
router.register('homepage', HomepageStatsViewSet, basename='homepage')
router.register('services', ServiceViewSet, basename='services')
router.register('contact', ContactFormViewSet, basename='contact')
router.register('news', NewsViewSet, basename='news')
router.register('projects', ProjectViewSet, basename='projects')

urlpatterns = router.urls
