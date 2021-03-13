import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_course_detail(api_client, course_factory):
    course = course_factory(name='test_course')
    url = reverse('courses-detail', args=(course.id,))
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == course.id


@pytest.mark.django_db
def test_course_list(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    resp = api_client.get(url)
    resp_json = resp.json()
    courses_ids = {_.id for _ in courses}
    resp_ids = {_['id'] for _ in resp_json}
    assert resp.status_code == HTTP_200_OK
    assert courses_ids == resp_ids


@pytest.mark.django_db
def test_course_list_id_filter(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    courses_ids = [_.id for _ in courses]
    filter_ids = courses_ids[1:4]
    resp = api_client.get(url, {'id': filter_ids})
    resp_json = resp.json()
    resp_ids = {_['id'] for _ in resp_json}
    assert resp.status_code == HTTP_200_OK
    assert set(filter_ids) == resp_ids


@pytest.mark.django_db
def test_course_list_name_filter(api_client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    courses_names = [_.name for _ in courses]
    filter_name = courses_names[2]
    resp = api_client.get(url, {'name': filter_name})
    resp_json = resp.json()
    resp_names = {_['name'] for _ in resp_json}
    assert resp.status_code == HTTP_200_OK
    assert {filter_name} == resp_names


@pytest.mark.django_db
def test_course_create(api_client):
    url = reverse('courses-list')
    course_name = 'test_course98732497'
    payload = {'name': course_name}
    resp = api_client.post(url, payload, format='json')
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['name'] == course_name


@pytest.mark.django_db
def test_course_update(api_client):
    url = reverse('courses-list')
    course_name = 'test_course98732497'
    course_new_name = 'test_new_course3472891374'
    payload = {'name': course_name}
    resp_create = api_client.post(url, payload, format='json')
    resp_create_json = resp_create.json()

    url_update = reverse('courses-detail', args=(resp_create_json['id'],))
    payload_update = {'name': course_new_name}
    resp_update = api_client.patch(url_update, payload_update)
    resp_update_json = resp_update.json()

    assert resp_update.status_code == HTTP_200_OK
    assert resp_update_json['name'] == course_new_name
    assert resp_update_json['name'] != course_name


@pytest.mark.parametrize(
    ['students_num', 'expected_status'],
    (
            (1, HTTP_201_CREATED),
            (2, HTTP_201_CREATED),
            (3, HTTP_400_BAD_REQUEST)
    )
)
@pytest.mark.django_db
def test_max_students_per_course(api_client, settings, student_factory, students_num, expected_status):
    settings.MAX_STUDENTS_PER_COURSE = 2
    students = student_factory(_quantity=3)
    students_ids = [_.id for _ in students]
    url = reverse('courses-list')
    payload = {'name': 'test_course', 'students': students_ids[:students_num]}
    resp = api_client.post(url, payload, format='json')
    assert resp.status_code == expected_status
