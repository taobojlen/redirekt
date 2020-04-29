from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import AdminLoginForm

# TODO
PASSWORD = "mypass"

def index(request):
    return HttpResponse("Hello, world. You're at the links index.")

def admin(request):
  if not 'authenticated' in request.session or not request.session['authenticated']:
    return redirect('admin_login')
  

  # handle admin view

def admin_login(request):
  if request.method == 'POST':
    # Form was submitted
    form = AdminLoginForm(request)
    if form.is_valid():
      password = form.cleaned_data['password']
      if password == PASSWORD:
        request.session['authenticated'] = True
        return redirect('admin')
      else:
        form.add_error(None, "Incorrect password.")
  else:
    # GET request
    form = AdminLoginForm()

  return render(request, 'links/admin/login.html', {'form': form})
