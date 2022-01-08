from django.shortcuts import render


# Create your views here.

def landing_page(request):
    return render(request, "blog/landing_page.html")


def posts(request):
    pass


def post_details(request):
    pass
