from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import (
    LoginForm,
    PasswordChangeForm,
    ProfileEditForm,
    RegisterForm,
)
from users.service import USER_FILTERS, filter_users, get_paginated_objects

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("users:login")
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect("projects:project_list")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_list(request):
    active_filter = request.GET.get("filter")
    if request.user.is_authenticated and active_filter in USER_FILTERS:
        users_qs = filter_users(request.user, active_filter)
        query_prefix = f"filter={active_filter}&"
    else:
        active_filter = ""
        users_qs = User.objects.all().order_by("-date_joined")
        query_prefix = ""

    page = get_paginated_objects(request, users_qs)
    return render(
        request,
        "users/participants.html",
        {
            "participants": page,
            "page_obj": page,
            "active_filter": active_filter,
            "query_prefix": query_prefix,
        },
    )


def user_detail(request, user_id):
    user_obj = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        id=user_id,
    )
    return render(request, "users/user-details.html", {"user": user_obj})


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", user_id=request.user.id)
    return render(
        request,
        "users/edit_profile.html",
        {"form": form, "user": request.user},
    )


@login_required
def change_password(request):
    form = PasswordChangeForm(request.POST or None)
    if form.is_valid():
        user = request.user
        if user.check_password(form.cleaned_data["old_password"]):
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            update_session_auth_hash(request, user)
            return redirect("users:user_detail", user_id=user.id)
        form.add_error("old_password", "Неверный текущий пароль")
    return render(request, "users/change_password.html", {"form": form})
