from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .forms import CommentForm
from .models import Post


# Create your views here.

# def landing_page(request):
#     latest_post = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/landing_page.html", {
#         "posts": latest_post
#     })
#

class LandingPageView(ListView):
    template_name = "blog/landing_page.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = "-date"
    context_object_name = "all_posts"


# def posts(request):
#     posts_data = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {
#         "all_posts": posts_data
#     })
#

class PostDetails(View):
    template_name = "blog/post-detail.html"
    model = Post
    context_object_name = "post"

    def is_stored(self, request, post):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved = post.id in stored_posts
        else:
            is_saved = False
        return is_saved

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "is_saved": self.is_stored(request, post)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details", args=[slug]))

        context = {
            "post": post,
            "tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "is_saved": self.is_stored(request, post)

        }
        return render(request, "blog/post-detail.html", context)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #
    #     context["tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context


# def post_details(request, slug):
#     found_post = get_object_or_404(Post, slug=slug)
#
#     return render(request, "blog/post-detail.html", {
#         "post": found_post,
#         "tags": found_post.tags.all()
#     })
class ReadLater(View):

    def get(self, request):
        stored_post = request.session.get("stored_posts")
        context = {}
        if stored_post is None or len(stored_post) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_post)
            context["posts"] = posts
            context["has_posts"] = True
        print(len(stored_post))
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_post = request.session.get("stored_posts")
        if stored_post is None:
            stored_post = []
        post_id = int(request.POST["post_id"])
        if post_id not in stored_post:
            stored_post.append(post_id)
        else:
            stored_post.remove(post_id)
        request.session["stored_posts"] = stored_post

        return HttpResponseRedirect(reverse("landing-page"))
