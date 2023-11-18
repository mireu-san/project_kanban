from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트용 사용자 생성
        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Testpassword123",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("Testpassword123"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), "testuser")

    def test_custom_user_manager_create_user(self):
        user2 = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="Testpassword123",
        )
        self.assertFalse(user2.is_staff)
        self.assertFalse(user2.is_superuser)

    def test_custom_user_manager_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="Adminpassword123",
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_password_validation(self):
        with self.assertRaises(ValidationError):
            # 비밀번호에 영문과 숫자가 포함되지 않은 경우
            User.objects.create_user(
                username="invaliduser",
                email="invaliduser@example.com",
                password="password",
            )

        with self.assertRaises(ValidationError):
            # 비밀번호 길이가 짧은 경우
            User.objects.create_user(
                username="shortpassuser",
                email="shortpassuser@example.com",
                password="Shrt1",
            )
