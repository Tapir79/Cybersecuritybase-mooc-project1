from django.db import migrations
from django.contrib.auth.models import User
from django.utils import timezone


def create_test_user(apps, schema_editor):
    # Check if the test user already exists to avoid duplicates
    if not User.objects.filter(username="testuser").exists():
        User.objects.create_user(
            username="testuser",
            password="testpassword1",
            email="testuser@example.com",
            is_staff=True,  # Modify this based on your needs
            is_superuser=False,  # Modify this based on your needs
            date_joined=timezone.now(),
        )


def remove_test_user(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(username="testuser").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_add_data'),
    ]

    operations = [
        migrations.RunPython(create_test_user, remove_test_user),
    ]
