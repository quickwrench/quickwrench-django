import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from quickwrench_api.apps.users.models import User


class TestRegister:
    @pytest.mark.django_db
    def test_register_success_201(self, client, user_data, load_data):
        response = client.post("/users/register/", user_data, format="json")
        assert response.data["account"]["username"] == user_data["account"]["username"]
        assert response.data["account"]["email"] == user_data["account"]["email"]
        assert (
            response.data["account"]["phone_number"]
            == user_data["account"]["phone_number"]
        )
        assert response.data["first_name"] == user_data["first_name"]
        assert response.data["last_name"] == user_data["last_name"]
        assert response.data["car_make"] == user_data["car_make"]
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_register_with_existing_email(self, client, user_with_existing_email):

        payload = {
            "account": {
                "email": user_with_existing_email.account.email,
                "username": "newuser",
                "password": "newpassword",
                "phone_number": "+20110124567",
            },
            "first_name": "Jane",
            "last_name": "Doe",
            "car_make": 1,
        }

        response = client.post("/users/register/", payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["account"]
        assert response.data["account"]["email"] == [
            "account with this email already exists."
        ]

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "invalid_email",
        [
            "invalidemail.com",
            "@missingusername.com",
            "test@.com",
        ],
    )
    def test_register_with_invalid_email(self, client, user_data, invalid_email):
        user_data["account"]["email"] = invalid_email
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data["account"]

    @pytest.mark.django_db
    def test_register_missing_username(self, client, user_data):
        user_data["account"]["username"] = ""
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in response.data["account"]
        assert response.data["account"]["username"] == ["This field may not be blank."]

    @pytest.mark.django_db
    def test_register_missing_password(self, client, user_data):
        user_data["account"]["password"] = ""
        response = client.post("/users/register/", user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data["account"]
        assert response.data["account"]["password"] == ["This field may not be blank."]

    @pytest.mark.django_db
    def test_filter_user_by_account__username(
        self, client: APIClient, user_with_existing_email: User
    ):

        response: Response = client.get(
            "/users/search/",
            {"account__username": user_with_existing_email.account.username},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["account"]["username"]
            == user_with_existing_email.account.username
        )

    @pytest.mark.django_db
    def test_filter_user_by_account__phone_number(
        self, client: APIClient, user_with_existing_email: User
    ):
        response: Response = client.get(
            "/users/search/",
            {"account__phone_number": user_with_existing_email.account.phone_number},
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert (
            response.data[0]["account"]["phone_number"]
            == user_with_existing_email.account.phone_number
        )

    @pytest.mark.django_db
    def test_filter_by_first_name(
        self, client: APIClient, user_with_existing_email: User
    ):
        response: Response = client.get(
            "/users/search/", {"first_name": user_with_existing_email.first_name}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["first_name"] == user_with_existing_email.first_name

    @pytest.mark.django_db
    def test_filter_by_last_name(
        self, client: APIClient, user_with_existing_email: User
    ):
        response: Response = client.get(
            "/users/search/", {"last_name": user_with_existing_email.last_name}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["last_name"] == user_with_existing_email.last_name
