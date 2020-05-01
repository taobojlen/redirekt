from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from ua_parser import user_agent_parser
from ipware import get_client_ip
import logging

from .forms import AdminLoginForm, LinkForm
from .models import Link, Visit
from .utils import is_authenticated, is_bot, get_random_short_id

# TODO
PASSWORD = "mypass"


def index(request):
    return HttpResponse("Hello, world. You're at the links index.")


def redirect_to_destination(request, short_id):
    link = get_object_or_404(Link, short_id=short_id)

    try:
        user_agent = request.META["HTTP_USER_AGENT"]
        client_ip, _is_routable = get_client_ip(request)
        visit = Visit(
            link=link,
            user_agent=user_agent,
            ip=client_ip,
            is_bot=is_bot(user_agent),
            city=request.ipinfo.city,
            country=request.ipinfo.country,
            hostname=request.ipinfo.hostname,
            latitude=float(request.ipinfo.latitude),
            longitude=float(request.ipinfo.longitude)
        )
        visit.save()
    except Exception as e:
        # something went wrong but we don't want to alert the visitor...
        logging.error(
            "Failed to save visit to {}. IP: {}, UA: {}".format(
                link, client_ip, user_agent
            )
        )
        logging.error(e)

    return redirect(link.destination)


def admin(request):
    if not is_authenticated(request):
        return redirect("admin-login")

    # We're authenticated; show admin view.
    links = Link.objects.order_by("-created_at")
    return render(request, "links/admin/index.html", {"links": links})


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

    return render(request, "links/admin/login.html", {"form": form})


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

    return render(request, "links/admin/create_link.html", {"form": form})


def link_detail(request, pk):
    link = get_object_or_404(Link, pk=pk)
    visits = link.visit_set.all()
    return render(
        request, "links/admin/view_link.html", {"link": link, "visits": visits}
    )


class DeleteLink(DeleteView, SuccessMessageMixin):
    model = Link
    success_url = reverse_lazy("links-admin")
    success_message = "Deleted link successfully."
