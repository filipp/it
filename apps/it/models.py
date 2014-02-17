from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType


class Attachment(models.Model):
    attachment = models.FileField(upload_to='attachments')
    created_by = models.ForeignKey(User)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey("content_type", "object_id")

    @classmethod
    def get_content_type(self, model):
        return ContentType.objects.get(app_label='it', model=model)


class Issue(models.Model):
    description = models.TextField()
    priority = models.PositiveIntegerField(default=0)
    users = models.ManyToManyField(
        User,
        null=True,
        blank=True,
        related_name='metoo'
    )

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return '/issues/%d/' % self.pk


class Task(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(Issue, null=True)
    step = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, null=True)
    assigned_to = models.ForeignKey(User, null=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.description


class Asset(models.Model):
    name = models.CharField(max_length=256, default='New Asset')
    description = models.TextField()
    location = models.CharField(max_length=256)
    ip_address = models.IPAddressField(default='')
    issues = models.ManyToManyField(Issue, null=True)

    def __unicode__(self):
        return self.name
