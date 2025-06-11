from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,HttpResponseNotFound
from .decorator import organiser_only,profile_updated
from queries.models import Query
from user_profile.models import UserProfile
from django.http import JsonResponse
from .forms import AnnouncmentForm
from .models import Announcments

@login_required
@organiser_only
@profile_updated
def staff_dashboard(request):
    return render(request, 'staff_home/dashboard.html')

@login_required
@organiser_only
def checkregistration(request):
    user=UserProfile.objects.all().order_by('-created_at')
    print(user)
    return render(request,'staff_home/registration.html')

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
            return redirect('make_announcments')  # Replace with your actual redirect
    else:
        form = AnnouncmentForm()
    return render(request, 'staff_home/announcment.html', {'form': form})


