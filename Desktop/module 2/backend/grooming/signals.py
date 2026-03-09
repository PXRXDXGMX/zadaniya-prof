from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_admin_user(sender, **kwargs):
    if sender.name != "grooming":
        return

    User = get_user_model()
    username = "admin"
    password = "grooming"
    admin_email = "admin@groomroom"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": admin_email,
            "is_staff": True,
            "is_superuser": True,
        },
    )

    changed = False
    if user.email != admin_email:
        user.email = admin_email
        changed = True
    if not user.is_staff:
        user.is_staff = True
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True

    if created or changed or not user.check_password(password):
        user.set_password(password)
        user.save()
