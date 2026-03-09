from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models


User = get_user_model()


class GroomRequest(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новая"
        PROCESSING = "processing", "Обработка данных"
        COMPLETED = "completed", "Услуга оказана"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groom_requests")
    pet_name = models.CharField(max_length=120)
    pet_photo = models.ImageField(
        upload_to="pets/original/",
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "bmp"])],
    )
    result_photo = models.ImageField(
        upload_to="pets/result/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "bmp"])],
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.pet_name} ({self.get_status_display()})"
