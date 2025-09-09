from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile as up
from django.contrib import messages

# Create your views here.
@login_required
def userprofile_view(request):
    user= request.user
    #email=user.email
    #context={
    #    'user_email':email,
    #}
    #return render(request,'user_profile/profile.html',context)
    user_role = getattr(request.user, 'userrole', None)
    try:
        profile=up.objects.get(user=user)
    except up.DoesNotExist:
        profile=None

    is_nitk = user.email.endswith(".nitk.edu.in")
    if is_nitk:
        college_value = "National Institute of Technology Karnataka" 
    else:
        college_value = profile.college if profile else ""

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        branch = request.POST.get('branch')
        college = request.POST.get('college')
        year = request.POST.get('year')
        dob = request.POST.get('dob')
        photo = request.FILES.get('photo')
        if is_nitk:
            college = "National Institute of Technology Karnataka"


        if profile:
            # Update existing profile
            profile.first_name = first_name
            profile.last_name = last_name
            profile.contact = contact
            profile.branch = branch
            profile.college = college
            profile.year = year
            profile.dob = dob
            if photo:
                profile.photo = photo
            profile.save()
            
                # After saving:
            messages.success(request, 'Profile updated successfully.')
            if not user_role.is_organiser:
                messages.success(request,'Visit Team Profile to to Create or Join a Team')
        else:
            # Create new profile
            up.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                contact=contact,
                branch=branch,
                college=college,
                year=year,
                dob=dob,
                photo=photo
            )
            messages.success(request,'Profile Saved Successfully')
            if not user_role.is_organiser:
                return redirect('dashboard')

    return render(request, 'user_profile/profile.html', {
        'user_email': user.email,
        'profile': profile,
        'user_role':user_role,
        'is_nitk': is_nitk,
    'college_value': college_value
    })