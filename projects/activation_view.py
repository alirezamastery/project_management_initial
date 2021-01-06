from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from projects.models import Project, ProjectMembership

User = get_user_model()


def active_project(request, project_id):
    user = request.user
    user_obj = User.objects.get(username=user)

    project_membership_qs = user_obj.projectmembership_set.all()
    for project_membership in project_membership_qs:
        project_membership.is_current = False
        project_membership.save()

    project_obj = get_object_or_404(Project, pk=project_id)
    activated_project_obj = project_obj.projectmembership_set.filter(user=user).first()
    activated_project_obj.is_current = True
    activated_project_obj.save()

    return redirect('index')
