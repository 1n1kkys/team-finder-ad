from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from team_finder import constants

FILTER_OWNERS_OF_FAVORITES = "owners-of-favorite-projects"
FILTER_OWNERS_OF_PARTICIPATING = "owners-of-participating-projects"
FILTER_INTERESTED_IN_MY_PROJECTS = "interested-in-my-projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS = "participants-of-my-projects"

USER_FILTERS = (
    FILTER_OWNERS_OF_FAVORITES,
    FILTER_OWNERS_OF_PARTICIPATING,
    FILTER_INTERESTED_IN_MY_PROJECTS,
    FILTER_PARTICIPANTS_OF_MY_PROJECTS,
)


def get_paginated_objects(
    request, queryset, page_size=constants.PAGINATION_PAGE_SIZE
):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def filter_users(user, filter_name):
    user_model = get_user_model()
    queryset = user_model.objects.all()
    if filter_name == FILTER_OWNERS_OF_FAVORITES:
        queryset = queryset.filter(owned_projects__interested_users=user)
    elif filter_name == FILTER_OWNERS_OF_PARTICIPATING:
        queryset = queryset.filter(owned_projects__participants=user)
    elif filter_name == FILTER_INTERESTED_IN_MY_PROJECTS:
        queryset = queryset.filter(favorites__owner=user)
    elif filter_name == FILTER_PARTICIPANTS_OF_MY_PROJECTS:
        queryset = queryset.filter(participated_projects__owner=user)
    else:
        return user_model.objects.none()
    return queryset.distinct().order_by("-date_joined")
