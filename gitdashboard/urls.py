from django.conf.urls import url
from . import views

urlpatterns = [
  #url(r'^$', views.repo_list, name='repo_list'),
  url(r'^repo1-branch.*$', views.repo_detail, name='repo_detail'),
  url(r'^add_list/$', views.add_list, name='repo-add_list'),
  url(r'^list_repo/$', views.list_repo),
  url(r'^list_submit/', views.list_submit, name='repo-list_submit'),
  url(r'^list_submit', views.list_submit, name='repo-list_submit'),
  url(r'^list_submit/detail/(?P<repo>.*)/(?P<branch>.*)/(?P<day>.*)$', views.repo_detail, name='repo_detail'),
  url(r'^details/(?P<repo>.*)/(?P<branch>.*)$', views.details),
  url(r'^$', views.list_lists, name="repo_lists"),
]
