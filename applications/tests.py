import pytest
from rest_framework.test import APIClient

from accounts.models import User
from applications.models import Application


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_a(db):
    return User.objects.create_user(username="user_a", email="a@example.com", password="pw")


@pytest.fixture
def user_b(db):
    return User.objects.create_user(username="user_b", email="b@example.com", password="pw")


@pytest.mark.django_db
def test_create_application_returns_201(api_client, user_a):
    api_client.force_authenticate(user_a)

    response = api_client.post(
        "/api/applications/",
        {"company": "Acme", "job_title": "Backend Engineer", "status": "applied"},
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_application_missing_company_returns_400(api_client, user_a):
    api_client.force_authenticate(user_a)

    response = api_client.post(
        "/api/applications/",
        {"job_title": "Backend Engineer", "status": "applied"},
        format="json",
    )

    assert response.status_code == 400
    assert "company" in response.json()


@pytest.mark.django_db
def test_filter_by_status(api_client, user_a):
    Application.objects.create(owner=user_a, company="Acme", job_title="Engineer", status="applied")
    Application.objects.create(owner=user_a, company="Globex", job_title="Engineer", status="interviewing")
    api_client.force_authenticate(user_a)

    response = api_client.get("/api/applications/?status=applied")

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["company"] == "Acme"


@pytest.mark.django_db
def test_user_cannot_read_another_users_application(api_client, user_a, user_b):
    application = Application.objects.create(owner=user_b, company="Acme", job_title="Engineer")
    api_client.force_authenticate(user_a)

    response = api_client.get(f"/api/applications/{application.id}/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_edit_another_users_application(api_client, user_a, user_b):
    application = Application.objects.create(owner=user_b, company="Acme", job_title="Engineer")
    api_client.force_authenticate(user_a)

    response = api_client.patch(
        f"/api/applications/{application.id}/", {"company": "Hacked"}, format="json"
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_user_cannot_delete_another_users_application(api_client, user_a, user_b):
    application = Application.objects.create(owner=user_b, company="Acme", job_title="Engineer")
    api_client.force_authenticate(user_a)

    response = api_client.delete(f"/api/applications/{application.id}/")

    assert response.status_code == 404
