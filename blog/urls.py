from django.urls import path

from blog import views

urlpatterns = [
    path("", views.landing_page, name="landing-page"),
    path("posts", views.posts, name="posts"),
    path("posts/<slug:slug>", views.post_details, name="post-details"),
]
