from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .decorator import organiser_only,profile_updated
from django.contrib import messages
from django.http import HttpResponseForbidden,HttpResponseNotFound
from queries.models import Query
from user_profile.models import UserProfile
from team_profile.models import Team
from django.db.models import Q
from django.http import JsonResponse
from .forms import AnnouncmentForm
from .models import Announcments
from accounts.models import UserRole
from django.core.paginator import Paginator
@login_required
@organiser_only
@profile_updated
def staff_dashboard(request):
    return render(request, 'staff_home/dashboard.html')

@login_required
@organiser_only
def checkregistration(request):
    query = request.GET.get('q', '')
    filter_status = request.GET.get('filter', '')
    sort = request.GET.get('sort', 'first_name')  # default sorting
    direction = request.GET.get('direction', 'asc')
    year = request.GET.get('event_year', '2025')  # default to 2025

    user_profiles = UserProfile.objects.select_related('user').prefetch_related('user__team')

    if query:
        user_profiles = user_profiles.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(college__icontains=query) |
            Q(branch__icontains=query)
        )

    if filter_status == 'registered':
        user_profiles = user_profiles.filter(user__team__isnull=False, user__team__is_registered=True).distinct()
    elif filter_status == 'not_registered':
        user_profiles = user_profiles.filter(user__team__isnull=False, user__team__is_registered=False).distinct()
    elif filter_status == 'no_team':
        user_profiles = user_profiles.filter(user__team__isnull=True).distinct()

    # Filter by event year
    if year:
        user_profiles = user_profiles.filter(event_year=year)

    # Sorting
    if direction == 'desc':
        sort = f'-{sort}'
    user_profiles = user_profiles.order_by(sort)

    paginator = Paginator(user_profiles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_home/registration.html', {
        'page_obj': page_obj,
        'query': query,
        'filter': filter_status,
        'sort': request.GET.get('sort', ''),
        'direction': direction,
        'event_year': year
    })

@login_required
@organiser_only
def upload_questions(request):
    return render(request,'staff_home/questions.html')

@login_required
@organiser_only
def queries(request):
    # Fetch all queries (or filter if you want)
    queries = Query.objects.all().order_by('-created_at')  # Or filter by some criteria
    total_queries = queries.count()

    context = {
        'queries': queries,
        'total_queries': total_queries,
    }
    return render(request, 'staff_home/check_queries.html', context)
@login_required
@organiser_only
def resolve_query(request, ticket):
    try:
        query = Query.objects.get(ticket=ticket)
    except Query.DoesNotExist:
        return HttpResponseNotFound("Query not found")

    if request.method == 'POST':
        query.response = request.POST.get('response')
        query.resolved = True
        query.save()
        return redirect('respond_queries')

    return render(request, 'staff_home/resolve_query.html', {'query': query})

@login_required
@organiser_only
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncmentForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            print(f"Announcement saved: {announcement}")
            return redirect('make_announcments')  # Replace with your actual redirect
    else:
        form = AnnouncmentForm()
    return render(request, 'staff_home/announcment.html', {'form': form})


@login_required
@organiser_only
def announcement_list(request):
    announcments = Announcments.objects.order_by('-created_at')
    return render(request, 'staff_home/announcement_list.html', {'Announcments': announcments})

@login_required
def announcement_edit(request, pk):
    try:
        announcement = Announcments.objects.get(pk=pk, created_by=request.user)
    except Announcments.DoesNotExist:
        messages.error(request,"This Announcment is not made by you contact its creator.")
        return redirect('announcement_list')

    if request.method == 'POST':
        form = AnnouncmentForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')
    else:
        form = AnnouncmentForm(instance=announcement)

    return render(request, 'staff_home/announcment_edit.html', {'form': form})


