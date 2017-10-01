from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.NotebookCreateView.as_view(), name="home"),

    url(r"^notebooks/(?P<pk>[\w-]+)/notes/$", views.NotebookNotesView.as_view(), name="notebook_notes"),

    url(r"^ajax/notebooks/(?P<notebook_pk>\d+)/notes/create/$", views.ajax_notes_create, name="ajax_notes_create"),
    url(r"^ajax/notebooks/(?P<notebook_pk>\d+)/notes/(?P<pk>\d+)/update/$", views.ajax_notes_update, name="ajax_notes_update"),
    url(r"^ajax/notebooks/(?P<notebook_pk>\d+)/notes/update-order/$", views.ajax_notes_update_order, name="ajax_notes_update_order"),
]
