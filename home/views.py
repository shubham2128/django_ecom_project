from django.shortcuts import render, redirect


def homePage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "homePage.html", context)