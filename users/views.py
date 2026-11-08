from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder import constants
from users.forms import (
    LoginForm,
    PasswordChangeForm,
    ProfileEditForm,
    RegisterForm,
)
from users.services import USER_FILTERS, filter_users, get_paginated_objects

User = get_user_model()


def register_view(request):
    form = RegisterForm(request.POST or None)
    if not form.is_valid():
        return render(request, "users/register.html", {"form": form})
    form.save()
    return redirect("users:login")


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if not form.is_valid():
        return render(request, "users/login.html", {"form": form})
    login(request, form.get_user())
    return redirect("projects:project_list")


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_list(request):
    active_filter = request.GET.get("filter", constants.DEFAULT_USER_FILTER)
    if request.user.is_authenticated and active_filter in USER_FILTERS:
        users = filter_users(request.user, active_filter)
        query_prefix = f"filter={active_filter}&"
    else:
        active_filter = constants.DEFAULT_USER_FILTER
        users = User.objects.all()
        query_prefix = ""

    page = get_paginated_objects(request, users)
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
    user = get_object_or_404(
        User.objects.prefetch_related("owned_projects"),
        id=user_id,
    )
    return render(request, "users/user-details.html", {"user": user})


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if not form.is_valid():
        return render(
            request,
            "users/edit_profile.html",
            {"form": form, "user": request.user},
        )
    form.save()
    return redirect("users:user_detail", user_id=request.user.id)


@login_required
def change_password(request):
    form = PasswordChangeForm(request.POST or None)
    if not form.is_valid():
        return render(request, "users/change_password.html", {"form": form})
    user = request.user
    if not user.check_password(form.cleaned_data["old_password"]):
        form.add_error("old_password", "Неверный текущий пароль")
        return render(request, "users/change_password.html", {"form": form})
    user.set_password(form.cleaned_data["new_password1"])
    user.save()
    update_session_auth_hash(request, user)
    return redirect("users:user_detail", user_id=user.id)
