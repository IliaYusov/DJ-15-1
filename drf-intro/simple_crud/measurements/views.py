from measurements.models import Measurement, Project
from measurements.serializers import ProjectSerializer, MeasurementSerializer
from rest_framework.viewsets import ModelViewSet


class ProjectViewSet(ModelViewSet):
    """ViewSet для проекта."""
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


class MeasurementViewSet(ModelViewSet):
    """ViewSet для измерения."""
    serializer_class = MeasurementSerializer
    queryset = Measurement.objects.all()
