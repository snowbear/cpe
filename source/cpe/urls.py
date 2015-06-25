from django.conf.urls import patterns, url
from cpe import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^solve/(?P<exercise_id>\d+)/$', views.solve, name='solve'),
    url(r'^solve/(?P<exercise_id>\d+)/attempt/(?P<attempt_id>\d+)$', views.solve, name='solve2'),
    url(r'^submit/(?P<exercise_id>\d+)$', views.submit, name='submit'),
    url(r'^status/(?P<submission_id>\d+)$', views.status, name='status'),
    url(r'^update-status/(?P<submission_id>\d+)$', views.update_status, name='update_status'),
)
