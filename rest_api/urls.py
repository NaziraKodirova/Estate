from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_api .views import RegionViewSet, CityViewSet, ListingViewSet, ContactViewSet, CustomUserViewSet, ProfileViewSet
from django.urls import path


schema_view = get_schema_view(
   openapi.Info(
      title="ESTATE API",
      default_version='v1',
      description="Demo ESTATE API",
      terms_of_service="demo.com",
      contact=openapi.Contact(email="nazira.kodirova@mail.ru"),
      license=openapi.License(name="demo service")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register('regions', viewset= RegionViewSet)
router.register('cities', viewset=CityViewSet)
router.register('listings', viewset=ListingViewSet)
router.register('contacts', viewset=ContactViewSet)
router.register('customusers',viewset=CustomUserViewSet)
router.register('profile', viewset=ProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', views.obtain_auth_token),
    path('docs-swagger/', schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path('docs-redoc/', schema_view.with_ui("redoc", cache_timeout=0), name='redoc'),
]
