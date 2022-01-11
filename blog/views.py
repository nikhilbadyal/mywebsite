from django.shortcuts import render, get_object_or_404

from .models import Post


# Create your views here.

def landing_page(request):
    latest_post = Post.objects.all().order_by("-date")[:3]
    return render(request, "blog/landing_page.html", {
        "posts": latest_post
    })


def posts(request):
    posts_data = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html", {
        "all_posts": posts_data
    })


def post_details(request, slug):
    found_post = get_object_or_404(Post, slug=slug)

    return render(request, "blog/post-detail.html", {
        "post": found_post,
        "tags": found_post.tags.all()
    })
