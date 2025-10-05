from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately after registration
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

@login_required
def edit_profile(request): 
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})