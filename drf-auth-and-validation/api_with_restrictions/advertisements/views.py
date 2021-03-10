from django.db.models import Q
from rest_framework.decorators import action

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


def open_advert_count(viewset, request):
    return viewset.queryset.filter(
        creator=request.user).filter(
        status='OPEN').count()


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        if request.user.id is not None:
            self.queryset = self.queryset.\
                select_related('creator').\
                prefetch_related('favourite_of').\
                exclude(~Q(creator=request.user), status='DRAFT')
        else:
            self.queryset = self.queryset.\
                select_related('creator').\
                prefetch_related('favourite_of').\
                exclude(status='DRAFT')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if request.user.id is not None:
            self.queryset = self.queryset.\
                select_related('creator').\
                prefetch_related('favourite_of').\
                exclude(~Q(creator=request.user), status='DRAFT')
        else:
            self.queryset = self.queryset.\
                select_related('creator').\
                prefetch_related('favourite_of').\
                exclude(status='DRAFT')
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if open_advert_count(self, request) >= MAX_ADVERTS_NUMBER:
            return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if 'status' in request.data and self.queryset.get(id=kwargs['pk']).status != 'OPEN':
            if open_advert_count(self, request) >= MAX_ADVERTS_NUMBER and request.data['status'] == 'OPEN':
                return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if 'status' in request.data and self.queryset.get(id=kwargs['pk']).status != 'OPEN':
            if open_advert_count(self, request) >= MAX_ADVERTS_NUMBER and request.data['status'] == 'OPEN':
                return Response(data='Max advertisements number', status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def add_to_favourites(self, request, pk=None):
        advertisement = self.queryset.select_related('creator').get(id=pk)
        if advertisement.creator_id == request.user.id:
            return Response(data="Can't favourite own advertisement", status=status.HTTP_400_BAD_REQUEST)
        advertisement.favourite_of.add(request.user.id)
        return Response(data='Added to favourites', status=status.HTTP_200_OK)

    @action(detail=True, methods=['put'])
    def remove_from_favourites(self, request, pk=None):
        advertisement = self.queryset.prefetch_related('favourite_of').select_related('creator').get(id=pk)
        if request.user not in advertisement.favourite_of.all():
            return Response(data="Not in your favourites", status=status.HTTP_400_BAD_REQUEST)
        advertisement.favourite_of.remove(request.user.id)
        return Response(data='Removed from favourites', status=status.HTTP_200_OK)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()] or [IsAdmin()]
        elif self.action in ["create", "add_to_favourites", "remove_from_favorites"]:
            return [IsAuthenticated()]
        return []
