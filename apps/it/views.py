from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import *
from .models import (Issue, Task, Attachment, User, Asset, TaggedItem)

def home(request):
    state = request.GET.get('state')
    issues = Issue.objects.all()

    if state:
        issues = issues.filter(state=state)

    form = SimpleIssueForm()
    states = Issue.STATES
    issue = Issue(created_by_id=1)

    if request.method == 'POST':
        form = SimpleIssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            messages.success(request, 'Issue saved')
            return redirect(issue)
    return render(request, "list_issues.html", locals())

def search(request):
    query = request.GET['q']
    form = IssueForm()
    issues = Issue.objects.filter(description__icontains=query)
    return render(request, "list_issues.html", locals())

def view_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    task = Task(issue=issue, created_by_id=1)
    form = SimpleTaskForm(instance=task)

    return render(request, "view_issue.html", locals())

def edit_issue(request, pk=None):
    if pk is None:
        issue = Issue(created_by_id=1)
    else:
        issue = Issue.objects.get(pk=pk)

    form = IssueForm(instance=issue)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            messages.success(request, 'Issue saved')
            return redirect(issue)

    return render(request, "edit_issue.html", locals())

def edit_task(request, issue, pk=None):
    if pk is None:
        task = Task()
        task.created_by_id = 1
        task.issue = Issue.objects.get(pk=issue)
    else:
        task = Task.objects.get(pk=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(task.issue)
        else:
            print form.errors

    return render(request, "edit_task.html", locals())

def metoo(request, issue, user):
    issue = Issue.objects.get(pk=issue)
    user = User.objects.get(pk=user)

    if user in issue.users.all():
        issue.users.remove(user)
    else:
        issue.users.add(user)
    
    messages.success(request, 'Issue updated')
    return redirect(issue)

def add_files(request, pk):
    issue = Issue.objects.get(pk=pk)
    att = Attachment(content_object=issue, created_by_id=1)
    form = AttachmentForm(request.POST, request.FILES, instance=att)

    if form.is_valid():
        form.save()
    else:
        print form.errors

    return HttpResponse('Cheerio!')

def delete_issue(request, pk):
    Issue.objects.filter(pk=pk).delete()
    messages.success(request, 'Issue deleted')
    return redirect(home)

def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    messages.info(request, 'Task deleted')
    return redirect(task.issue)

def list_assets(request):
    pass

def list_stuff(request):
    if request.method == 'POST':
        form = SimpleAssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            return redirect(asset)

    categories = Asset.KINDS
    object_list = Asset.objects.all()
    kind = request.GET.get('kind')

    if kind:
        object_list = object_list.filter(kind=kind)

    form = SimpleAssetForm(initial={'kind': kind})
    return render(request, "list_stuff.html", locals())

def view_asset(request, pk):
    return render(request, "view_asset.html", locals())

def delete_file(request, pk):
    file = Attachment.objects.get(pk=pk)
    file.delete()
    messages.success(request, 'File deleted')
    return redirect(file.content_object)

def remove_user(request, issue, user):
    issue = Issue.objects.get(pk=issue)
    user = User.objects.get(pk=user)
    issue.users.remove(user)
    messages.success(request, 'User removed from issue')
    return redirect(issue)

def tags(request):
    import json
    if request.method == 'POST':
        name = request.POST.get('tag')
        object_id = request.POST.get('object_id')
        content_type_id = request.POST.get('content_type_id')
        tag = TaggedItem(tag=name, object_id=object_id)
        tag.content_type_id = content_type_id
        tag.created_by_id = 1
        tag.save()
        messages.success(request, 'Tag %s added' % name)
        return redirect(request.META['HTTP_REFERER'])

    query = TaggedItem.objects.all()
    oid = request.GET.get('oid')
    ctype = request.GET.get('ctype')

    if oid and ctype :
        query = query.exclude(object_id=oid, content_type=ctype)

    tags = query.values_list('tag', flat=True)
    return HttpResponse(json.dumps(list(tags)), content_type="application/javascript")

def delete_tag(request, pk):
    TaggedItem.objects.filter(pk=pk).delete()
    return HttpResponse('OK')
