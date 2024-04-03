from django.db import models
from django.utils import timezone

from news.news_models import News


class DetailNewsMedia(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    news_id = models.ForeignKey(News, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    media_uri = models.ImageField(upload_to="uploads/news/media/")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.CharField(null=True, max_length=255)
    updated_by = models.CharField(null=True, max_length=255)

    def __str__(self):
        return str(self.news_id) + ' - ' + self.title

    def save(self, *args, **kwargs):
        self.id = f'DNM-{timezone.now().timestamp()}'
        super(DetailNewsMedia, self).save(*args, **kwargs)