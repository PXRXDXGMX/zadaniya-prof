import json
import re
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .models import GroomRequest


USERNAME_RE = re.compile(r"^[A-Za-z-]+$")
MAX_FILE_SIZE = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = ("jpeg", "jpg", "bmp")


def _request_to_dict(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            return json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    return request.POST


def _serve_frontend(relative_path: str):
    file_path = Path(settings.BASE_DIR).parent / "frontend" / relative_path
    return HttpResponse(file_path.read_text(encoding="utf-8"), content_type="text/html; charset=utf-8")


def _serialize_request(item: GroomRequest):
    return {
        "id": item.id,
        "pet_name": item.pet_name,
        "status": item.status,
        "status_label": item.get_status_display(),
        "pet_photo": item.pet_photo.url if item.pet_photo else None,
        "result_photo": item.result_photo.url if item.result_photo else None,
        "created_at": item.created_at.isoformat(),
        "can_delete": item.status == GroomRequest.Status.NEW,
        "owner": item.owner.username,
    }


def _validate_photo(photo):
    errors = []
    if not photo:
        return ["Файл обязателен."]

    if photo.size > MAX_FILE_SIZE:
        errors.append("Размер файла должен быть не больше 2 МБ.")

    ext = photo.name.rsplit(".", 1)[-1].lower() if "." in photo.name else ""
    if ext not in ALLOWED_EXTENSIONS:
        errors.append("Разрешены только форматы jpeg/jpg/bmp.")

    return errors


@require_GET
def home_page(request):
    return _serve_frontend("index.html")


@require_GET
def user_page(request):
    return _serve_frontend("user/index.html")


@require_GET
def groom_page(request):
    return _serve_frontend("groom/index.html")


@require_GET
def completed_requests_view(request):
    items = GroomRequest.objects.filter(status=GroomRequest.Status.COMPLETED).order_by("-created_at")[:4]
    return JsonResponse({"results": [_serialize_request(item) for item in items]})


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    data = _request_to_dict(request)
    errors = {}

    full_name = (data.get("full_name") or "").strip()
    username = (data.get("username") or "").strip()
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    password_repeat = data.get("password_repeat") or ""

    if not full_name:
        errors["full_name"] = "Поле обязательно."

    if not username:
        errors["username"] = "Поле обязательно."
    elif not USERNAME_RE.fullmatch(username):
        errors["username"] = "Только латиница и дефис."

    from django.contrib.auth import get_user_model

    User = get_user_model()
    if username and User.objects.filter(username=username).exists():
        errors["username"] = "Логин уже занят."

    if not email:
        errors["email"] = "Поле обязательно."
    else:
        from django.core.exceptions import ValidationError
        from django.core.validators import validate_email

        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Некорректный email."

    if not password:
        errors["password"] = "Поле обязательно."

    if password_repeat != password:
        errors["password_repeat"] = "Пароли не совпадают."

    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email, first_name=full_name)
    login(request, user)
    return JsonResponse({"ok": True, "role": "admin" if user.is_staff else "user"}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data = _request_to_dict(request)
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({"ok": False, "message": "Неверный логин или пароль."}, status=400)

    login(request, user)
    return JsonResponse({"ok": True, "role": "admin" if user.is_staff else "user"})


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})
    return JsonResponse(
        {
            "authenticated": True,
            "username": request.user.username,
            "full_name": request.user.first_name,
            "role": "admin" if request.user.is_staff else "user",
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def user_requests_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "message": "Требуется авторизация."}, status=401)

    if request.method == "GET":
        items = GroomRequest.objects.filter(owner=request.user).order_by("-created_at")
        return JsonResponse({"results": [_serialize_request(item) for item in items]})

    pet_name = (request.POST.get("pet_name") or "").strip()
    pet_photo = request.FILES.get("pet_photo")
    errors = {}

    if not pet_name:
        errors["pet_name"] = "Кличка обязательна."

    photo_errors = _validate_photo(pet_photo)
    if photo_errors:
        errors["pet_photo"] = " ".join(photo_errors)

    if errors:
        return JsonResponse({"ok": False, "errors": errors}, status=400)

    item = GroomRequest.objects.create(
        owner=request.user,
        pet_name=pet_name,
        pet_photo=pet_photo,
        status=GroomRequest.Status.NEW,
    )

    return JsonResponse({"ok": True, "request": _serialize_request(item)}, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user_request_view(request, request_id: int):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "message": "Требуется авторизация."}, status=401)

    item = get_object_or_404(GroomRequest, id=request_id, owner=request.user)
    if item.status != GroomRequest.Status.NEW:
        return JsonResponse({"ok": False, "message": "Удалять можно только заявки со статусом 'Новая'."}, status=400)

    item.delete()
    return JsonResponse({"ok": True})


def _require_admin(request):
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "message": "Требуется авторизация."}, status=401)
    if not request.user.is_staff:
        return JsonResponse({"ok": False, "message": "Доступ только админу."}, status=403)
    return None


@require_GET
def admin_requests_view(request):
    denial = _require_admin(request)
    if denial:
        return denial

    items = GroomRequest.objects.all().order_by("-created_at")
    return JsonResponse({"results": [_serialize_request(item) for item in items]})


@csrf_exempt
@require_http_methods(["POST"])
def admin_update_status_view(request, request_id: int):
    denial = _require_admin(request)
    if denial:
        return denial

    item = get_object_or_404(GroomRequest, id=request_id)
    target_status = (request.POST.get("status") or "").strip()
    result_photo = request.FILES.get("result_photo")

    if item.status == GroomRequest.Status.NEW and target_status == GroomRequest.Status.PROCESSING:
        item.status = GroomRequest.Status.PROCESSING
        item.save(update_fields=["status"])
        return JsonResponse({"ok": True, "request": _serialize_request(item)})

    if item.status == GroomRequest.Status.PROCESSING and target_status == GroomRequest.Status.COMPLETED:
        photo_errors = _validate_photo(result_photo)
        if photo_errors:
            return JsonResponse({"ok": False, "errors": {"result_photo": " ".join(photo_errors)}}, status=400)

        item.status = GroomRequest.Status.COMPLETED
        item.result_photo = result_photo
        item.save(update_fields=["status", "result_photo"])
        return JsonResponse({"ok": True, "request": _serialize_request(item)})

    return JsonResponse({"ok": False, "message": "Нельзя сменить статус."}, status=400)
