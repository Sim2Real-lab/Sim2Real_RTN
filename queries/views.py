from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserQueryForm
from .models import Query
from .decorator import user_view,profile_updated
from django.http import JsonResponse

@login_required
@user_view
@profile_updated
def user_query_view(request):
    if request.method == 'POST':
        form = UserQueryForm(request.POST, user=request.user)
        try:
            if form.is_valid():
                query = form.save(commit=False)
                query.sender = request.user
                query.query_type = 'user'

                profile = request.user.userprofile
                query.name = f"{profile.first_name} {profile.last_name}"
                query.contact = profile.contact
                query.email = request.user.email

                query.save()    
                return redirect('query_response')
        except Exception:
                query.name = request.user.username
                query.email = request.user.email
                query.contact = ''

        query.save()
        return redirect('query_response')
    else:
        form = UserQueryForm(user=request.user)

    return render(request, 'queries/query_form.html', {'form': form})

@login_required
@user_view
@profile_updated
def query_response(request):
    queries = Query.objects.filter(sender=request.user).order_by('-created_at')
    return render(request,'queries/query_response.html',{'queries':queries})

@login_required
@user_view
@profile_updated
def fetch_response(request, ticket):
    try:
        query = Query.objects.get(ticket=ticket, email=request.user.email)
    except Query.DoesNotExist:
        return JsonResponse({'error': 'Query not found or not authorized'}, status=404)

    if not query.resolved:
        return JsonResponse({'error': 'Query not resolved yet'}, status=400)

    return JsonResponse({
        'response': query.response,
    })
