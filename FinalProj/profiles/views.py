from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from .forms import ItemForm
from django.contrib.auth.decorators import user_passes_test

@login_required
def view_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profiles/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)  # Pass existing profile instance to the form

    return render(request, 'profiles/edit_profile.html', {'form': form, 'profile': profile})



@user_passes_test(lambda u: u.is_superuser)
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to your desired page after saving the item
    else:
        form = ItemForm()
    return render(request, 'your_template.html', {'form': form})