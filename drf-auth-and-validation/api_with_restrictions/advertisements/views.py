from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

MAX_ADVERTS_NUMBER = 10


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def create(self, request, *args, **kwargs):
        open_advert_count = Advertisement.objects.filter(
            creator=request.user).filter(
            status='OPEN').count()
        if open_advert_count >= MAX_ADVERTS_NUMBER:
            return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if "status" in request.data and Advertisement.objects.get(id=kwargs['pk']).status != 'OPEN':
            open_advert_count = Advertisement.objects.filter(
                creator=request.user).filter(
                status='OPEN').count()
            if open_advert_count >= MAX_ADVERTS_NUMBER and request.data['status'] == 'OPEN':
                return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if "status" in request.data and Advertisement.objects.get(id=kwargs['pk']).status != 'OPEN':
            open_advert_count = Advertisement.objects.filter(
                creator=request.user).filter(
                status='OPEN').count()
            if open_advert_count >= MAX_ADVERTS_NUMBER and request.data['status'] == 'OPEN':
                return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()] or [IsAdmin()]
        elif self.action == "create":
            return [IsAuthenticated()] or [IsAdmin()]
        return []
