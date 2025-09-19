from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .decorators import organiser_only,profile_updated
from django.contrib import messages
from django.http import HttpResponseForbidden,HttpResponseNotFound,HttpResponse
from queries.models import Query
from user_profile.models import UserProfile
from team_profile.models import Team
from django.db.models import Q
import csv
from django.http import JsonResponse
from .forms import AnnouncmentForm,ProblemStatementConfigForm,ProblemStatementSectionForm,ResourceForm,BrochureForm
from .models import Announcments,ProblemStatementConfig,ProblemStatementSection,Resource,Brochure
from accounts.models import UserRole
from django.core.paginator import Paginator
from django.db.models.functions import ExtractYear
from collections import defaultdict
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

@login_required
@organiser_only
@profile_updated
def all_users_view(request):
    query = request.GET.get("q", "").strip()
    filter_year = request.GET.get("event_year")
    filter_role = request.GET.get("role")
    filter_college = request.GET.get("college")
    filter_team = request.GET.get("team")
    download_csv = request.GET.get("download") == "csv"

    # Base queryset (bring in profiles + roles efficiently)
    users = User.objects.select_related("userprofile", "userrole").prefetch_related("team", "led_team")

    # --- Search ---
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(userprofile__college__icontains=query)
        )

    # --- Filters ---
    if filter_year:
        users = users.filter(userprofile__event_year=filter_year)

    if filter_role:
        if filter_role == "organiser":
            users = users.filter(userrole__is_organiser=True)
        elif filter_role == "participant":
            users = users.filter(userrole__is_organiser=False)

    if filter_college:
        users = users.filter(userprofile__college__icontains=filter_college)

    if filter_team:
        users = users.filter(
            Q(team__name__icontains=filter_team) |
            Q(led_team__name__icontains=filter_team)
        ).distinct()

    # --- CSV Download ---
    if download_csv:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Username", "Full Name", "Email", "College", "Event Year", "Role", "Teams"
        ])

        for u in users:
            profile = getattr(u, "userprofile", None)
            role = "Organiser" if getattr(u.userrole, "is_organiser", False) else "Participant"

            # Teams: both member + leader
            team_names = list(u.team.values_list("name", flat=True))
            if hasattr(u, "led_team"):
                team_names.append(u.led_team.name)
            teams_str = ", ".join(team_names) if team_names else "No Team"

            writer.writerow([
                u.username,
                u.get_full_name(),
                u.email,
                getattr(profile, "college", "N/A"),
                getattr(profile, "event_year", "N/A"),
                role,
                teams_str
            ])
        return response

    # --- Pagination ---
    paginator = Paginator(users, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Dropdown values
    available_years = (UserProfile.objects.values_list("event_year", flat=True)
                       .distinct().order_by("event_year"))
    available_colleges = (UserProfile.objects.values_list("college", flat=True)
                          .distinct().order_by("college"))
    available_roles = ["organiser", "participant"]

    context = {
        "users": page_obj,
        "page_obj": page_obj,
        "query": query,
        "filter_year": filter_year,
        "filter_role": filter_role,
        "filter_college": filter_college,
        "filter_team": filter_team,
        "available_years": available_years,
        "available_colleges": available_colleges,
        "available_roles": available_roles,
    }
    return render(request, "staff_home/all_users.html", context)


@login_required
@organiser_only
@profile_updated
def staff_dashboard(request):
    return render(request, 'staff_home/dashboard.html')

import csv
from django.http import HttpResponse
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

from staff_home.decorators import organiser_only, profile_updated

@login_required
@organiser_only
@profile_updated
def checkregistration(request):
    query = request.GET.get("q", "")
    filter_paid = request.GET.get("paid")
    filter_verified = request.GET.get("verified")
    filter_outsider = request.GET.get("outsider")
    filter_year = request.GET.get("event_year")
    download_csv = request.GET.get("download") == "csv"

    # Get all teams with prefetch of members and related profiles
    teams = Team.objects.select_related("leader").prefetch_related(
        Prefetch("members", queryset=User.objects.select_related("userprofile"))
    ).order_by("name")

    # --- Search ---
    if query:
        teams = teams.filter(
            Q(name__icontains=query)
            | Q(leader__username__icontains=query)
            | Q(leader__email__icontains=query)
            | Q(members__username__icontains=query)
            | Q(members__email__icontains=query)
        ).distinct()

    # --- Filters ---
    if filter_paid in ["yes", "no"]:
        teams = teams.filter(is_paid=(filter_paid == "yes"))

    if filter_verified in ["yes", "no"]:
        teams = teams.filter(is_verified=(filter_verified == "yes"))

    if filter_year:
        teams = teams.filter(leader__userprofile__event_year=filter_year)

    # Outsider filter
    if filter_outsider in ["yes", "no"]:
        filtered = []
        for t in teams:
            outsider = t.is_outsider()
            if (filter_outsider == "yes" and outsider) or (filter_outsider == "no" and not outsider):
                filtered.append(t)
        teams = filtered

    # --- CSV Download ---
    if download_csv:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="registrations.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Team Name", "Leader", "Leader Email", "Leader Contact",
            "Members", "Event Year", "Paid", "Verified"
        ])

        for team in teams:
            leader_profile = getattr(team.leader, "userprofile", None)
            leader_contact = leader_profile.contact if leader_profile else "N/A"

            members_list = []
            for m in team.members.all():
                profile = getattr(m, "userprofile", None)
                contact = profile.contact if profile else "N/A"
                members_list.append(f"{m.get_full_name()} ({m.email}, {contact})")
            members_str = "; ".join(members_list)

            writer.writerow([
                team.name,
                team.leader.get_full_name(),
                team.leader.email,
                leader_contact,
                members_str,
                getattr(leader_profile, "event_year", "N/A"),
                "Yes" if team.is_paid else "No",
                "Yes" if team.is_verified else "No"
            ])
        return response

    # --- Pagination ---
    paginator = Paginator(teams, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Event years for filter dropdown
    available_years = list(User.objects.filter(userprofile__isnull=False)
                           .values_list("userprofile__event_year", flat=True).distinct().order_by("userprofile__event_year"))

    context = {
        "teams": page_obj,
        "page_obj": page_obj,
        "query": query,
        "filter_paid": filter_paid,
        "filter_verified": filter_verified,
        "filter_outsider": filter_outsider,
        "filter_year": filter_year,
        "available_years": available_years,
    }
    return render(request, "staff_home/registration.html", context)

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



@login_required
@organiser_only
def manage_problem_statement(request):
    config, _ = ProblemStatementConfig.objects.get_or_create(id=1)  # single row

    if request.method == "POST":
        form = ProblemStatementConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Problem statement settings updated.")
            return redirect("manage_problem_statement")
    else:
        form = ProblemStatementConfigForm(instance=config)

    sections = config.sections.all()

    return render(request, "staff_home/manage_problem_statement.html", {
        "form": form,
        "sections": sections
    })


@login_required
@organiser_only
def add_section(request):
    config, _ = ProblemStatementConfig.objects.get_or_create(id=1)

    if request.method == "POST":
        form = ProblemStatementSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.config = config
            section.save()
            messages.success(request, "Section added successfully.")
            return redirect("manage_problem_statement")
    else:
        form = ProblemStatementSectionForm()

    return render(request, "staff_home/section_form.html", {"form": form, "action": "Add"})


@login_required
@organiser_only
def edit_section(request, pk):
    section = get_object_or_404(ProblemStatementSection, pk=pk)

    if request.method == "POST":
        form = ProblemStatementSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully.")
            return redirect("manage_problem_statement")
    else:
        form = ProblemStatementSectionForm(instance=section)

    return render(request, "staff_home/section_form.html", {"form": form, "action": "Edit"})


@login_required
@organiser_only
def delete_section(request, pk):
    section = get_object_or_404(ProblemStatementSection, pk=pk)
    section.delete()
    messages.success(request, "Section deleted successfully.")
    return redirect("manage_problem_statement")

@login_required
@organiser_only
def manage_resources(request):
    # For editing
    edit_id = request.GET.get("edit")
    delete_id = request.GET.get("delete")

    # Add / Edit
    if request.method == "POST":
        if "delete_id" in request.POST:  # Delete request
            resource = get_object_or_404(Resource, pk=request.POST["delete_id"])
            resource.delete()
            messages.success(request, "Resource deleted successfully.")
            return redirect("manage_resources")

        elif "edit_id" in request.POST:  # Edit request
            resource = get_object_or_404(Resource, pk=request.POST["edit_id"])
            form = ResourceForm(request.POST, request.FILES, instance=resource)
            if form.is_valid():
                form.save()
                messages.success(request, "Resource updated successfully.")
                return redirect("manage_resources")

        else:  # New upload
            form = ResourceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Resource added successfully.")
                return redirect("manage_resources")
    else:
        if edit_id:  # Prefill edit form
            resource = get_object_or_404(Resource, pk=edit_id)
            form = ResourceForm(instance=resource)
        else:
            form = ResourceForm()

    resources = Resource.objects.all()
    return render(request, "staff_home/manage_resources.html", {
        "form": form,
        "resources": resources,
        "edit_id": edit_id,
    })


@login_required
@organiser_only
def upload_brochure(request):
    brochure = Brochure.objects.first()  # keep only one
    if request.method == "POST":
        form = BrochureForm(request.POST, request.FILES, instance=brochure)
        if form.is_valid():
            form.save()
            messages.success(request, "Brochure uploaded successfully.")
            return redirect("upload_brochure")
    else:
        form = BrochureForm(instance=brochure)

    return render(request, "staff_home/upload_brochure.html", {
        "form": form,
        "brochure": brochure
    })

