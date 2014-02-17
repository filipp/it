from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from apps.it.models import Issue, Task, Attachment


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task


def home(request):
    issues = Issue.objects.all()
    return render(request, "list_issues.html", locals())

def search(request):
    query = request.GET['q']
    results = Issue.objects.filter(description__icontains=query)
    return render(request, "default.html", locals())

def view_issue(request, pk):
    issue = Issue.objects.get(pk=pk)
    return render(request, "view_issue.html", locals())

def edit_issue(request, pk=None):
    if pk is None:
        issue = Issue()
    else:
        issue = Issue.objects.get(pk=pk)

    form = IssueForm(instance=issue)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            return redirect(issue)

    return render(request, "edit_issue.html", locals())

def edit_task(request, issue, pk=None):
    if pk is None:
        task = Task()
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

@csrf_exempt
def add_files(request, pk):
    issue = Issue.objects.get(pk=pk)
    att = Attachment(content_object=issue, created_by_id=1)
    form = AttachmentForm(request.POST, request.FILES, instance=att)

    if form.is_valid:
        form.save()
    else:
        print form.errors

    return HttpResponse('Cheerio!')
