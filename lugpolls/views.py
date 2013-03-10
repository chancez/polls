from django.shortcuts import render


def home(request):
    return render(request, 'index.html', {})


#@login_required()
def profile(request):
    return render(request, 'users/profile.html', {})
