from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from projects.forms import ProjectForm
from projects.models import Project
from team_finder import constants
from users.service import get_paginated_objects


def _project_queryset():
    return (
        Project.objects.select_related("owner")
        .prefetch_related("participants")
        .all()
    )


@ensure_csrf_cookie
def project_list(request):
    page = get_paginated_objects(request, _project_queryset())
    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page,
            "page_obj": page,
            "query_prefix": "",
        },
    )


@ensure_csrf_cookie
def project_detail(request, project_id):
    project = get_object_or_404(_project_queryset(), id=project_id)
    return render(
        request,
        "projects/project-details.html",
        {"project": project},
    )


@login_required
@ensure_csrf_cookie
def favorite_projects(request):
    projects = request.user.favorites.select_related("owner").prefetch_related(
        "participants"
    )
    return render(
        request,
        "projects/favorite_projects.html",
        {"projects": projects},
    )


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:project_detail", project_id=project.id)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": False},
    )


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:project_detail", project_id=project.id)
    return render(
        request,
        "projects/create-project.html",
        {"form": form, "is_edit": True},
    )


@login_required
@require_POST
def project_complete(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if project.status != constants.STATUS_OPEN:
        return JsonResponse(
            {"status": "error"},
            status=HTTPStatus.BAD_REQUEST,
        )
    project.status = constants.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_POST
def toggle_participate(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner_id == request.user.id:
        return JsonResponse(
            {"status": "error", "message": "Автор уже в проекте"},
            status=HTTPStatus.BAD_REQUEST,
        )

    is_participant = project.participants.filter(id=request.user.id).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": not is_participant})


@login_required
@require_POST
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.favorites.filter(id=project.id).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True
    return JsonResponse({"status": "ok", "favorited": favorited})
