from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('apps.it',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    url(r'^search/$', 'views.search', name='search'),
    url(r'^issues/add/$', 'views.edit_issue', name='add_issue'),
    url(r'^issues/(\d+)/$', 'views.view_issue', name='view_issue'),
    url(r'^issues/(\d+)/edit/$', 'views.edit_issue', name='edit_issue'),
    url(r'^issues/(\d+)/delete/$', 'views.delete_issue', name='delete_issue'),
    url(r'^issues/(\d+)/tasks/add/$', 'views.edit_task', name='add_task'),
    url(r'^issues/(\d+)/tasks/(\d+)/$', 'views.edit_task', name='edit_task'),
    url(r'^tasks/(\d+)/delete/$', 'views.delete_task', name='delete_task'),
    url(r'^issues/(\d+)/users/(\d+)/add/$', 'views.metoo', name='metoo'),
    url(r'^issues/(\d+)/users/(\d+)/remove/$', 'views.remove_user', name='remove_user'),
    url(r'^issues/(\d+)/files/add/$', 'views.add_files', name='add_files'),

    url(r'^stuff/$', 'views.list_stuff', name='list_stuff'),
    url(r'^stuff/(\d+)/$', 'views.view_asset', name='view_asset'),

    url(r'^files/(\d+)/delete/$', 'views.delete_file', name='delete_file'),

    url(r'^tags/$', 'views.tags', name='tags'),
    url(r'^tags/(\d+)/delete/$', 'views.delete_tag', name='delete_tag'),

    url(r'^users/$', 'views.users', name='users'),

    url(r'^docs/$', 'views.docs', name='docs'),

    url(r'^login/$', 'views.login', name='login'),
    url(r'^logout/$', 'views.logout', name='logout'),
)
