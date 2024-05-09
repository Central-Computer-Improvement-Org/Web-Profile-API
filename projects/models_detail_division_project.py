from django.db import models

from projects.models_projects import Project
from users.models import Division

class DetailDivisionProject(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    division_id = models.ForeignKey(Division, related_name='projects', on_delete=models.PROTECT)
    project_id = models.ForeignKey(Project, related_name='divisions', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")
    
    def __str__(self):
        return str(self.project_id) + ' - ' + str(self.member_nim)