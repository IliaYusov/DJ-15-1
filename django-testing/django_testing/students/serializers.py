from django.conf import settings
from rest_framework import serializers

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if 'students' in data and len(data['students']) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('Too many students for a course')
        return data


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ("id", "name", "birth_date")
