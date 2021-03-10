from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    creator = filters.NumberFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    fav = filters.BooleanFilter(method='fav_method')

    def fav_method(self, queryset, value, *args, **kwargs):
        if args[0] is True:
            queryset = queryset.filter(favourite_of__in=[self.request.user.id])
        elif args[0] is False:
            queryset = queryset.exclude(favourite_of__in=[self.request.user.id])
        return queryset

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']
