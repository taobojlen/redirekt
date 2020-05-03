from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from links.models import Link, Visit
from .utils import is_authenticated
from .forms import AdminLoginForm, LinkForm

# TODO
PASSWORD = "mypass"


def admin(request):
    if not is_authenticated(request):
        return redirect("admin-login")

    # We're authenticated; show admin view.
    links = Link.objects.order_by("-created_at")
    return render(request, "admin/index.html", {"links": links})


def admin_login(request):
    if is_authenticated(request):
        return redirect("links-admin")

    if request.method == "POST":
        # Form was submitted
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            if password == PASSWORD:
                request.session["authenticated"] = True
                return redirect("links-admin")
            else:
                form.add_error(None, "Incorrect password.")
    else:
        # GET request
        form = AdminLoginForm()

    return render(request, "admin/login.html", {"form": form})


def create_link(request):
    if not is_authenticated(request):
        return redirect("admin-login")

    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            return redirect(link)
    else:
        # Generate random short ID as initial value
        form = LinkForm()

    return render(request, "admin/create_link.html", {"form": form})


def link_detail(request, pk):
    link = get_object_or_404(Link, pk=pk)
    visits = link.visit_set.all()
    return render(
        request, "admin/view_link.html", {"link": link, "visits": visits}
    )


class DeleteLink(DeleteView, SuccessMessageMixin):
    model = Link
    success_url = reverse_lazy("links-admin")
    success_message = "Deleted link successfully."
