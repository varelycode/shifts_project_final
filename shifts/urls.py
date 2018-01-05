from django.conf.urls import url

from boards import views


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.GroupDetailView.as_view(), name='group_detail'),
    url(r'^(?P<pk>\d+)/new_shift/$', views.create_shift_view, name='create_shift'),
    url(r'^(?P<pk>\d+)/shift/(?P<shift_pk>\d+)/$', views.ShiftDetailView.as_view(), name='shift_detail'),
    url(r'^(?P<pk>\d+)/shift/(?P<shift_pk>\d+)/new_run/$', views.create_run_view, name='create_run'),
    # url(r'^(?P<pk>\d+)/shift/(?P<shift_pk>\d+)/new_run/(?P<shift_pk>\d+)/$', views.create_run_view, name='run_detail'),
    # url(r'^(?P<pk>\d+)/topics/(?P<run_pk>\d+)/add_shift/$', views.add_shift, name='add_shift'),
    # url(r'^(?P<pk>\d+)/shift/(?P<shift_pk>\d+)/runs/(?P<run_pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='edit_run'),

]
