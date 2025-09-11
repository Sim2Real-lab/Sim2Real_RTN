from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponseForbidden,FileResponse, Http404
from .decorator import user_view,organiser_only,profile_updated
from user_profile.models import UserProfile
from team_profile.models import Team
from staff_home.models import Announcments,ProblemStatementConfig,Resource,Brochure
from itertools import chain
from django.contrib import messages
from operator import attrgetter

@login_required
@user_view
@profile_updated
def home_view(request):
    team = request.user.team.first()
    registered = team.is_registered() if team else False
    paid = team.is_paid if team else False

    if registered:
        queryset1 = Announcments.objects.filter(category="GENERAL")
        queryset2 = Announcments.objects.filter(category="REGISTERED")
    else:
        queryset1 = Announcments.objects.filter(category="GENERAL")
        queryset2 = Announcments.objects.filter(category="NOT_REGISTERED")

    # Combine and sort in Python
    combined = sorted(
        chain(queryset1, queryset2),
        key=attrgetter('created_at'),
        reverse=True
    )[:3]  # Limit to the latest 3
    show_welcome = not request.session.get('welcome_shown', False)
    request.session['welcome_shown'] = True  # Set flag to avoid showing again
    context = {
    'registered': registered,
    'announcements': combined,
    'show_welcome': show_welcome,
    'paid':paid,
}
    return render(request, 'home/index.html', context)


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
    announcments = Announcments.objects.order_by('-created_at')
    team = request.user.team.first()  # Gets the team user is a member of
    registered = team.is_registered() if team else False
    if registered:
        announcments = Announcments.objects.filter(category='REGISTERED').order_by('-created_at')|Announcments.objects.filter(category='GENERAL').order_by('-created_at')
        return render(request,'home/announcements.html',{'Announcments':announcments})
    if not registered:
        announcments = Announcments.objects.filter(category='NOT_REGISTERED').order_by('-created_at')|Announcments.objects.filter(category='GENERAL').order_by('-created_at')
        return render(request,'home/announcements.html',{'Announcments':announcments})
    return redirect('home')
@login_required
@user_view
def faq_view(request):
    return render(request,'home/faq_pre_registration.html')

@login_required
@user_view
def problem_statement_view(request):
    team = request.user.team.first()
    registered = team.is_registered() if team else False

    config = ProblemStatementConfig.objects.first()  # Single row config

    if not registered or not (config and config.enabled):
        return render(request, "home/problem_statement.html", {"visible": False})

    return render(request, "home/problem_statement.html", {
        "visible": True,
        "file": config.file if config else None,
        "sections": config.sections.all().order_by("order") if config else []
    })

@login_required
@user_view
def view_resources(request):
    resources = Resource.objects.all()
    return render(request, "home/resources.html", {"resources": resources})




@login_required
@user_view
def download_brochure(request):
    brochure = Brochure.objects.first()
    if not brochure or not brochure.file:
        # Show a side toast message instead of 404
        messages.error(request, "Brochure download failed. File not available.")
        return redirect("problem_statement")  # Redirect to a participant page

    # Return the file as a download
    response = FileResponse(
        brochure.file.open('rb'),
        as_attachment=True,
        filename=brochure.file.name
    )
    return response
