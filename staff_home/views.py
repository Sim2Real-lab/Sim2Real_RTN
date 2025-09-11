from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .decorators import organiser_only,profile_updated
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
from django.db.models.functions import ExtractYear
from collections import defaultdict
@login_required
@organiser_only
@profile_updated
def staff_dashboard(request):
    return render(request, 'staff_home/dashboard.html')
@login_required
@organiser_only
def checkregistration(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'user__first_name')
    direction = request.GET.get('direction', 'asc')
    year = request.GET.get('event_year', '')

    user_profiles = UserProfile.objects.select_related('user').prefetch_related('user__team')

    # Search
    if query:
        user_profiles = user_profiles.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(college__icontains=query) |
            Q(branch__icontains=query)
        )

    # Filter by registration year
    if year:
        try:
            year_int = int(year)
            user_profiles = user_profiles.annotate(
                reg_year=ExtractYear('user__date_joined')
            ).filter(reg_year=year_int)
        except ValueError:
            pass

    # Sorting
    if direction == 'desc':
        sort = f'-{sort}'
    user_profiles = user_profiles.order_by(sort)

    # Group by team (no pagination)
    grouped_users = defaultdict(list)
    for profile in user_profiles:
        teams = profile.user.team.all()
        if teams.exists():
            for team in teams:
                grouped_users[team.name].append(profile)
        else:
            grouped_users['No Team'].append(profile)

    # Available years for dropdown
    available_years = (
        UserProfile.objects
        .annotate(reg_year=ExtractYear('user__date_joined'))
        .values_list('reg_year', flat=True)
        .distinct()
        .order_by('-reg_year')
    )

    return render(request, 'staff_home/registration.html', {
        'grouped_users': grouped_users,
        'query': query,
        'sort': request.GET.get('sort', ''),
        'direction': direction,
        'event_year': year,
        'available_years': available_years,
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
@login_required
@organiser_only
def verify_payments(request, team_id=None):
    """
    Handles both:
    - POST: verify a specific team
    - GET: list all teams with optional search/status filters
    """
    # POST: verify a specific team
    if request.method == "POST" and team_id:
        team = get_object_or_404(Team, id=team_id)
        team.is_verified = True
        team.save()
        messages.success(request, f"Team '{team.name}' payment verified.")
        return redirect('verify_payments')  # redirect to the list view

    # GET: list all teams
    teams = Team.objects.all().order_by('-id')

    # Search filter
    query = request.GET.get("q", "").strip()
    if query:
        teams = teams.filter(
            Q(name__icontains=query) |
            Q(leader__first_name__icontains=query) |
            Q(leader__last_name__icontains=query) |
            Q(leader__email__icontains=query)
        )

    # Status filter
    status = request.GET.get("status", "").lower()
    if status == "pending":
        teams = teams.filter(is_paid=True, is_verified=False)
    elif status == "verified":
        teams = teams.filter(is_paid=True, is_verified=True)
    elif status == "unpaid":
        teams = teams.filter(is_paid=False)
    # else: show all if no status filter

    context = {
        "teams": teams,
        "query": query,
        "status": status,
    }
    return render(request, "staff_home/verify_payments.html", context)

@login_required
@organiser_only
def view_payment_screenshot(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if not team.payment_screenshot:
        messages.warning(request, "No screenshot available for this team.")
        return redirect('verify_payments')

    return render(request, "staff_home/payment_screenshot.html", {"team": team})
