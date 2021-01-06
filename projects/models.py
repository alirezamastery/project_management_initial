from django.contrib.auth.models import User
from django.db import models, transaction


class Project(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class ProjectMembership(models.Model):
    ROLE_GUEST = 'RG'
    ROLE_REPORTER = 'RR'
    ROLE_DEVELOPER = 'RD'
    ROLE_MASTER = 'RM'
    ROLE_OWNER = 'RO'

    ROLE_CHOICES = (
        (ROLE_GUEST, 'Guest'),
        (ROLE_REPORTER, 'Reporter'),
        (ROLE_DEVELOPER, 'Developer'),
        (ROLE_MASTER, 'Master'),
        (ROLE_OWNER, 'Owner'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=4, choices=ROLE_CHOICES, default=ROLE_GUEST, verbose_name='Role')
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user.username} in {self.project.name} is {self.get_role}'

    @property
    def get_role(self):
        for r in self.ROLE_CHOICES:
            if r[0] == self.role:
                return r[1]

    def has_permission(self, action):
        permissions = {
            self.ROLE_GUEST:     ('create_new_issue',
                                  'leave_comments'),
            self.ROLE_REPORTER:  ('create_new_issue',
                                  'leave_comments',
                                  'pull_project_code',
                                  'assign_issues_and_merge_requests',
                                  'see_a_list_of_merge_requests'
                                  ),
            self.ROLE_DEVELOPER: ('create_new_issue',
                                  'leave_comments',
                                  'pull_project_code',
                                  'assign_issues_and_merge_requests',
                                  'see_a_list_of_merge_requests',
                                  'manage_merge_requests',
                                  'create_new_branches'
                                  ),
            self.ROLE_MASTER:    ('create_new_issue',
                                  'leave_comments',
                                  'pull_project_code',
                                  'assign_issues_and_merge_requests',
                                  'see_a_list_of_merge_requests',
                                  'manage_merge_requests',
                                  'create_new_branches',
                                  'add_new_team_members',
                                  'push_to_protected_branches'
                                  ),
            self.ROLE_OWNER:     ('create_new_issue',
                                  'leave_comments',
                                  'pull_project_code',
                                  'assign_issues_and_merge_requests',
                                  'see_a_list_of_merge_requests',
                                  'manage_merge_requests',
                                  'create_new_branches',
                                  'add_new_team_members',
                                  'push_to_protected_branches',
                                  'switch_visibility_level',
                                  'remove_project'
                                  ),
        }

        return action in permissions[self.role]
