from django.urls import path

from blog import views

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="landing-page"),
    path("posts", views.AllPostsView.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PostDetails.as_view(), name="post-details"),
    path("read-later", views.ReadLater.as_view(), name="read-later"),
]
