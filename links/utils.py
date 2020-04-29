def is_authenticated(request):
  return 'authenticated' in request.session and request.session['authenticated']
