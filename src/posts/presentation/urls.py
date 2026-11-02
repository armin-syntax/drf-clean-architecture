from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("create/", views.PostCreateView.as_view(), name="post-create"),
    path("<uuid:public_id>/", views.PostDetailView.as_view(), name="post-detail"),
    path("<uuid:public_id>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("<uuid:public_id>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
]
