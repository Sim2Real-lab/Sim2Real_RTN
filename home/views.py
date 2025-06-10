from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden
from .decorator import user_view,organiser_only,profile_updated
from user_profile.models import UserProfile
from team_profile.models import Team

@login_required
@user_view
@profile_updated
def home_view(request):
    team = request.user.team.first()  # Gets the team user is a member of
    registered = team.is_registered() if team else False
    nitk=UserProfile.is_nitk_user
    context={
        'registered':registered,
    }
    return render(request,'home/index.html',context)


@login_required
@user_view
def schedule_view(request):
    return render(request,'home/schedule.html')

@login_required
@user_view
def registration_view(request):
    return render(request,'home/register.html')

@login_required
@user_view
def prize_view(request):
    return render(request,'home/prize.html')

@login_required
@user_view
def brochure_view(request):
    return render(request,'home/brochure.html')

@login_required
@user_view
def resources_view(request):
    return render(request,'home/resources.html')

@login_required
@user_view
def announce_view(request):
    return render(request,'home/announcements.html')

@login_required
@user_view
def faq_view(request):
    return render(request,'home/faq_pre_registration.html')