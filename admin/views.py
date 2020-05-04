from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy

from links.models import Link, Visit
from .forms import AdminLoginForm, LinkForm


@login_required
def admin(request):
    links = Link.objects.order_by("-created_at")
    return render(request, "admin/index.html", {"links": links})


@login_required
def create_link(request):
    if request.method == "POST":
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            return redirect(link)
    else:
        # Generate random short ID as initial value
        form = LinkForm()

    return render(request, "admin/create_link.html", {"form": form})


@login_required
def link_detail(request, pk):
    link = get_object_or_404(Link, pk=pk)
    visits = link.visit_set.order_by('-pk')
    return render(request, "admin/view_link.html", {"link": link, "visits": visits})


class DeleteLink(LoginRequiredMixin, DeleteView, SuccessMessageMixin):
    model = Link
    success_url = reverse_lazy("links-admin")
    success_message = "Deleted link successfully."


def logout_view(request):
    logout(request)
    return redirect("/admin")