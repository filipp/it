from django.db import models

from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType


class AbstractGenericItem(models.Model):
    created_by = models.ForeignKey(User, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    content_type = models.ForeignKey(ContentType, editable=False)
    content_object = generic.GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class TaggedItem(AbstractGenericItem):
    "A generic tagged item"
    tag = models.CharField(max_length=128)
    slug = models.SlugField()
    color = models.CharField(max_length=8, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super(TaggedItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.tag

    class Meta:
        ordering = ['tag']
        unique_together = ("content_type", "object_id", "tag",)


class Attachment(AbstractGenericItem):
    attachment = models.FileField(upload_to='attachments')

    def __unicode__(self):
        import os
        path = os.path.basename(self.attachment.name)
        return u'%s ...' % path[0:35]


class Article(AbstractGenericItem):
    note = models.TextField()
    tags = generic.GenericRelation(TaggedItem)
    title = models.CharField(max_length=256, default=_('New Article'))
    


class Issue(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=256, default=_('New Issue'))
    priority = models.PositiveIntegerField(default=0)
    assigned_to = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='issues')
    users = models.ManyToManyField(
        User,
        null=True,
        editable=False,
        related_name='metoo'
    )
    STATES = (
        ('NEW', _('New')),
        ('OPEN', _('Open')),
        ('CLOSED', _('Closed')),
    )
    state = models.CharField(max_length=32, choices=STATES, default=STATES[0][0])
    files = generic.GenericRelation(Attachment)
    tags = generic.GenericRelation(TaggedItem)
    created_by = models.ForeignKey(User, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    progress = models.PositiveIntegerField(default=0, editable=False)

    def __unicode__(self):
        return self.description

    def set_progress(self):
        self.progress = self.get_progress()
        self.save()

    def get_progress(self):
        all = self.task_set.all().count()
        if all < 1:
            return 0
        done = self.task_set.exclude(completed_at=None).count()
        print done/all*100
        return done/all*100

    def get_content_type(self):
        return ContentType.objects.get_for_model(self)

    def get_absolute_url(self):
        return '/issues/%d/' % self.pk

    class Meta:
        ordering = ['-priority', 'created_at']


class Task(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(Issue, null=True, editable=False)
    step = models.PositiveIntegerField(default=0, editable=False)
    created_by = models.ForeignKey(User, editable=False)
    assigned_to = models.ForeignKey(User,
                                    null=True,
                                    blank=True,
                                    related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    files = generic.GenericRelation(Attachment)

    def save(self):
        super(Task, self).save()
        self.issue.set_progress()

    def __unicode__(self):
        return self.description

    class Meta:
        ordering = ['-created_at']


class Asset(models.Model):
    name = models.CharField(max_length=256, default='New Asset')
    description = models.TextField()
    location = models.CharField(max_length=256)
    ip_address = models.IPAddressField(default='')
    product_url = models.URLField(null=True, blank=True)
    issues = models.ManyToManyField(Issue, null=True)
    files = generic.GenericRelation(Attachment)
    KINDS = (
        ('SERVER', _('Server')),
        ('WORKSTATION', _('Workstation')),
        ('NETWORK', _('Networking')),
        ('SOFTWARE', _('Software')),
        ('PRINTER', _('Printer')),
    )
    kind = models.CharField(choices=KINDS, max_length=128, default=KINDS[0][0])
    tags = generic.GenericRelation(TaggedItem)
    contact = models.ForeignKey(User, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/stuff/%d/' % self.pk
