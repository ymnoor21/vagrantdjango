from django.conf.urls import url

from . import views

app_name = 'polls'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(),
        name='index'),

    url(r'^(?P<pk>[0-9]+)/details/$',
        views.DetailsView.as_view(), name='details'),

    url(r'^(?P<pk>[0-9]+)/results/$',
        views.ResultsView.as_view(), name='results'),

    url(r'^(?P<question_id>[0-9]+)/vote/$',
        views.vote, name='vote'),
]
