from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import AdminLoginForm, LinkForm
from .models import Link
from .utils import is_authenticated

# TODO
PASSWORD = "mypass"

def index(request):
    return HttpResponse("Hello, world. You're at the links index.")

def admin(request):
  if not is_authenticated(request):
    return redirect('admin_login')

  # We're authenticated; show admin view.
  links = Link.objects.order_by('-created_at')
  return render(request, 'links/admin/index.html', {'links': links})

def admin_login(request):
  if is_authenticated(request):
    return redirect('links_admin')

  if request.method == 'POST':
    # Form was submitted
    form = AdminLoginForm(request.POST)
    if form.is_valid():
      password = form.cleaned_data['password']
      if password == PASSWORD:
        request.session['authenticated'] = True
        return redirect('links_admin')
      else:
        form.add_error(None, "Incorrect password.")
  else:
    # GET request
    form = AdminLoginForm()

  return render(request, 'links/admin/login.html', {'form': form})

def create_link(request):
  if not is_authenticated(request):
    return redirect('admin_login')

  if request.method == 'POST':
    form = LinkForm(request.POST)
    if form.is_valid():
      link = form.save()
      return redirect(link)
  else:
    form = LinkForm()

  return render(request, 'links/admin/create_link.html', {'form': form})

def link_detail(request, pk):
  link = Link.objects.get(pk=pk)
  visits = link.visit_set.all()
  return render(request, 'links/admin/view_link.html', {'link': link, 'visits': visits})

class DeleteLink(DeleteView, SuccessMessageMixin):
  model = Link
  success_url = reverse_lazy('links_admin')
  success_message = "Deleted link successfully."