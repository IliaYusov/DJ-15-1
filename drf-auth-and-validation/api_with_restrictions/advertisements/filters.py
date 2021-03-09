from django_filters import rest_framework as filters
from rest_framework.authtoken.admin import User

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    creator = filters.NumberFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    favourites = filters.ModelMultipleChoiceFilter(
        field_name='favourite_of',
        to_field_name='id',
        queryset=User.objects.all()
    )
    fav = filters.BooleanFilter(method='my_method')

    def my_method(self, queryset, value, *args, **kwargs):
        queryset = queryset.filter(self.request.user.id__in=favourite_of)
        return queryset

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status', 'favourites']
