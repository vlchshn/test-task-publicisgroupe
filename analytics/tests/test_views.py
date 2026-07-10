import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from analytics.models import FileUploadLog, FactData


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="tester", password="testpassword123")


@pytest.fixture
def auth_client(client, test_user):
    client.login(username="tester", password="testpassword123")
    return client


@pytest.mark.django_db
def test_dashboard_requires_login(client):
    response = client.get(reverse("dashboard"))
    assert response.status_code == 302
    assert "/login/" in response.url


@pytest.mark.django_db
def test_successful_file_upload(auth_client):
    csv_content = b"advertiser,brand,start,end,format,platform,impr\nAdv1,Brand1,28.03.2021,31.03.2021,banner,web,1000\nAdv2,Brand2,01.04.2021,10.04.2021,video,app,2000"
    valid_file = SimpleUploadedFile(
        "test_valid.csv", csv_content, content_type="text/csv"
    )

    response = auth_client.post(reverse("dashboard"), {"file": valid_file})

    assert response.status_code == 302
    assert FileUploadLog.objects.filter(status="SUCCESS").count() == 1
    assert FactData.objects.count() == 2


@pytest.mark.django_db
def test_invalid_file_upload_missing_data(auth_client):
    csv_content = b"advertiser,brand,start,end,format,platform,impr\nAdv1,Brand1,28.03.2021,31.03.2021,banner,web,1000\nAdv2,Brand2,,,video,app,2000"
    invalid_file = SimpleUploadedFile(
        "test_invalid.csv", csv_content, content_type="text/csv"
    )

    response = auth_client.post(reverse("dashboard"), {"file": invalid_file})

    assert response.status_code == 302
    assert FileUploadLog.objects.filter(status="FAILED").count() == 1
    assert FactData.objects.count() == 0


@pytest.mark.django_db
def test_dashboard_get_request(auth_client):
    response = auth_client.get(reverse("dashboard"))
    assert response.status_code == 200
    assert "form" in response.context


@pytest.mark.django_db
def test_invalid_file_extension(auth_client):
    txt_content = b"Just some plain text"
    invalid_file = SimpleUploadedFile(
        "test.txt", txt_content, content_type="text/plain"
    )

    auth_client.post(reverse("dashboard"), {"file": invalid_file})
    assert FileUploadLog.objects.filter(
        error_type__contains="Unsupported file format"
    ).exists()


@pytest.mark.django_db
def test_missing_required_columns(auth_client):
    csv_content = b"advertiser,brand\nAdv1,Brand1"
    invalid_file = SimpleUploadedFile(
        "test_cols.csv", csv_content, content_type="text/csv"
    )

    auth_client.post(reverse("dashboard"), {"file": invalid_file})
    assert FileUploadLog.objects.filter(
        error_type__contains="Missing required columns"
    ).exists()


@pytest.mark.django_db
def test_models_str_methods(test_user):
    log = FileUploadLog.objects.create(
        user=test_user, file_name="file.csv", status="SUCCESS"
    )
    assert str(log) == "file.csv - SUCCESS"

    fact = FactData.objects.create(
        upload_log=log,
        advertiser="Adv",
        brand="Brand",
        ad_format="Ban",
        platform="Web",
        impressions=10,
    )
    assert str(fact) == "Adv - Brand"
