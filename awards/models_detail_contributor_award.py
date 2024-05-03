from django.db import models

from awards.models_awards import Award
from users.models_users import User

class DetailContributorAward(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    member_nim = models.ForeignKey(User, related_name='awards', on_delete=models.PROTECT)
    award_id = models.ForeignKey(Award, related_name='contributors', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")
    
    def __str__(self):
        return str(self.project_id) + ' - ' + str(self.member_nim)