from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from listing.models import Region, City, Listing
from users.models import Profile, CustomUser
from contact.models import Contact
from .serializers import RegionSerializer, CitySerializer, ListingSerializer, ContactSerializer, CustomUserSerializer, ProfileSerializer
from django.db.models import F, Count
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny



class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    @action(detail=False, methods=['get'])
    def with_cities(self, request):
        regions = Region.objects.annotate(cities_count=Count('region_city')).filter(cities_count__gt=0)
        serializer = self.get_serializer(regions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_coordinates(self, request, pk=None):
        region = self.get_object()
        return Response({'lat': region.lat, 'long': region.long})

    @action(detail=True, methods=['post'])
    def update_coordinates(self, request, pk=None):
        region = self.get_object()
        region.lat = request.data.get('lat')
        region.long = request.data.get('long')
        region.save()
        return Response({'status': 'Coordinates updated'})

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'region__name']
    ordering_fields = ['name']

    @action(detail=False, methods=['get'])
    def with_listings(self, request):
        cities = City.objects.annotate(listings_count=Count('city_listing')).filter(listings_count__gt=0)
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_coordinates(self, request, pk=None):
        city = self.get_object()
        return Response({'lat': city.lat, 'long': city.long})

    @action(detail=True, methods=['post'])
    def update_coordinates(self, request, pk=None):
        city = self.get_object()
        city.lat = request.data.get('lat')
        city.long = request.data.get('long')
        city.save()
        return Response({'status': 'Coordinates updated'})

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['address', 'city__name']
    ordering_fields = ['created_date']

    @action(detail=True, methods=['get'])
    def increment_views(self, request, pk=None):
        listing = self.get_object()
        listing.views = F('views') + 1
        listing.save()
        return Response({'status': 'Views incremented'})


    @action(detail=True, methods=['get'])
    def get_coordinates(self, request, pk=None):
        listing = self.get_object()
        return Response({'lat': listing.lat, 'long': listing.long})

    @action(detail=True, methods=['post'])
    def update_coordinates(self, request, pk=None):
        listing = self.get_object()
        listing.lat = request.data.get('lat')
        listing.long = request.data.get('long')
        listing.save()
        return Response({'status': 'Coordinates updated'})

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name']

    @action(detail=True, methods=['get'])
    def by_email(self, request, pk=None):
        email = request.query_params.get('email', None)
        if email:
            contact = Contact.objects.filter(email=email)
        else:
            contact = Contact.objects.all()
        serializer = self.get_serializer(contact, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_phone(self, request, pk=None):
        contact = self.get_object()
        return Response({'phone': contact.phone})

    @action(detail=True, methods=['post'])
    def update_phone(self, request, pk=None):
        contact = self.get_object()
        contact.phone = request.data.get('phone')
        contact.save()
        return Response({'status': 'Phone updated'})


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username']

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email']
    ordering_fields = ['user__username']

    @action(detail=True, methods=['get'])
    def get_user_info(self, request, pk=None):
        profile = self.get_object()
        user = profile.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

