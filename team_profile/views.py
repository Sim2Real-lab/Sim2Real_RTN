from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JoinRequest,Team
from .forms import TeamCreationForm, JoinCodeForm, PaymentProofForm
from django.contrib import messages
from django.db import transaction
from .decorator import user_view,profile_updated
# Create your views here.
@login_required
@user_view
@profile_updated
def team_profile_views(request):
    if hasattr(request.user, 'led_team'):
        return redirect('create_team_with_code')
    
    if request.user.team.exists():
        return redirect('join_team_with_code')

    existing_request = JoinRequest.objects.filter(user=request.user).order_by('-id').first()
    
    if existing_request:
        if existing_request.status == "pending":
            return render(request, 'team_profile/join_team.html', {
                'pending': True,
                'team_name': existing_request.team.name
            })
        elif existing_request.status == "accepted":
            existing_request.team.members.add(request.user)
            existing_request.delete()
            return redirect('join_team_with_code')
        elif existing_request.status == "declined":
            existing_request.delete()
    
    # If no team, no pending request, and not a leader
    return render(request, 'team_profile/team.html')

@login_required
@user_view
@profile_updated
def create_team(request):
    if hasattr(request.user,'led_team'):
        return redirect('create_team_with_code')
    if request.method=='POST':
        form =TeamCreationForm(request.POST)
        if form.is_valid():
            team=form.save(commit=False) #This creates team object but doesn't save it.
            team.leader=request.user
            team.save() # Makes the user as team leader then saves 
            team.members.add(request.user) # makes the teamleader part of the team also
            messages.success(request,f"Team '{team.name}'created with join code  '{team.join_code}'")
            return redirect('create_team_with_code')
    else:
        form= TeamCreationForm()
    return render(request, 'team_profile/create_team.html', {'form': form})


@login_required
@user_view
@profile_updated
def create_team_with_code(request):
    if not hasattr(request.user, 'led_team'):
        return redirect('create_team')
    team = request.user.led_team

    if team.is_paid and request.method == 'POST':
        messages.error(request, "Team is registered and payment completed. No changes allowed.")
        return redirect('create_team_with_code')

    pending_requests = team.requests.filter(status='pending')
    members=team.members.all()
    context={'team': team,
        'pending_requests': pending_requests,
        'show_join_code': True,
        'members':members,
        'team_locked': team.is_paid,
        'registered':team.is_paid
    }
    return render(request, 'team_profile/create_team.html',context)

@login_required
@user_view
@profile_updated
def join_team_with_code(request):
    if request.user.team.exists():
        team = request.user.team.first()
        members = team.members.all()
        return render(request, 'team_profile/join_team.html', {
            'joined_team': True,
            'team': team,
            'members': members,
            'registered':team.is_paid
        })

    existing_request = JoinRequest.objects.filter(user=request.user).order_by('-id').first()
    
    if existing_request:
        if existing_request.status == 'pending':
            return render(request, 'team_profile/request_team.html', {
                'pending': True,
                'team_name': existing_request.team.name
            })
        elif existing_request.status == 'accepted':
            existing_request.team.members.add(request.user)
            return redirect('join_team_with_code')
        elif existing_request.status == 'declined':
            existing_request.delete()
            messages.error(request, "Request denied. Try joining with another code.")
            return redirect('join_team')
    
    return redirect('join_team')

@login_required
@user_view
@profile_updated
def join_team(request):
    if request.user.team.exists():
        return render(request, 'team_profile/join_team.html', {
            'already_in_team': True
        })
    existing_request = JoinRequest.objects.filter(user=request.user).order_by('-id').first()
    if existing_request:
        if existing_request.status == 'pending':
            return render(request, 'team_profile/join_team.html', {
                'pending': True,
                'team_name': existing_request.team.name
            })
        elif existing_request.status == 'accepted':
            existing_request.delete()
            return redirect('join_team_with_code')

        elif existing_request.status == 'declined':
            existing_request.delete()
            messages.error(request, "Your previous request was declined. Try a different join code.")
            return redirect('join_team')
    if request.method == 'POST':
        form = JoinCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['join_code']
            team = get_object_or_404(Team, join_code=code)
            if team.is_full():
                messages.error(request, "Team is full.")
            elif JoinRequest.objects.filter(user=request.user, team=team).exists():
                messages.info(request, "You have already requested to join.")
            else:
                JoinRequest.objects.create(user=request.user, team=team)
                messages.success(request, "Join request sent.")
                return redirect('teamprofile')
    else:
        form = JoinCodeForm()
    return render(request, 'team_profile/join_team.html', {'form': form})

@login_required
@user_view
@profile_updated
@transaction.atomic
def manage_requests(request):
    if not hasattr(request.user, 'led_team'):
        messages.error(request, "You are not a team leader.")
        return redirect('teamprofile')

    team = request.user.led_team
    team.refresh_from_db()
    requests = team.requests.filter(status='pending')
    members = team.members.all()
    member_count = team.members.count()

    # ✅ handle POST first
    if request.method == 'POST':
        action = request.POST.get('action')
        req_id = request.POST.get('request_id')
        joinrequest = get_object_or_404(JoinRequest, id=req_id, team=team)

        if action == 'accept' and not team.is_full():
            joinrequest.status = 'accepted'
            joinrequest.save()
            team.members.add(joinrequest.user)
            joinrequest.delete()
            messages.success(request, f"{joinrequest.user.username} added to the team.")
        elif action == 'decline':
            joinrequest.status = 'declined'
            joinrequest.save()
            joinrequest.delete()
            messages.info(request, f"{joinrequest.user.username}'s request was declined.")

        return redirect('manage_requests')

    # ✅ now handle GET logic
    if team.is_paid and team.is_verified:
        messages.info(request, "Team is registered and payment completed. No further changes allowed.")
        team_locked = True
    elif team.is_paid and not team.is_verified:
        messages.info(request, "Team payment completed. Waiting for Verification.")
        team_locked = True
    else:
        team_locked = False

    return render(request, 'team_profile/manage_requests.html', {
        'requests': requests,
        'team_locked': team_locked,
        'team': team,
        'members_count': member_count
    })


@login_required
@user_view
@profile_updated
def register_for_event(request):
    if not hasattr(request.user, 'led_team'):
        messages.error(request, "Only team leaders can register.")
        return redirect('teamprofile')

    team = request.user.led_team

    if team.is_paid and team.is_verified:
        messages.error(request, "Team is registered and payment completed. No changes allowed.")
        return redirect('manage_requests')
    
    if team.is_paid and not team.is_verified:
        messages.error(request, "Team payment completed. Waiting for Organisers to verify your status.")
        return redirect('manage_requests')

    if team.members.count() < 2:
        messages.error(request, "You need at least 2 members to register.")
        return redirect('create_team_with_code')

    profile = request.user.userprofile
    if profile.is_nitk_user():
        team.is_paid = True
        team.save()
        messages.success(request, "As an NITK student, your team has been registered without payment.")
        return redirect('teamprofile')

    if request.method == 'POST':
        return redirect('payment_page')  # real or simulated payment gateway

    return render(request, 'team_profile/manage_requests.html', {
        'team': team,
        'members_count': team.members.count()
    })


@login_required
@user_view
@profile_updated
def payment_view(request):
    if not hasattr(request.user, 'led_team'):
        messages.error(request, "You don't lead any team.")
        return redirect('teamprofile')

    team = request.user.led_team

    # Just check the boolean field
    if team.is_paid:
        messages.info(request, "Payment proof already submitted.")
        return redirect('teamprofile')

    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            team = form.save(commit=False)
            team.is_paid = True       # ✅ set boolean directly
            team.is_verified = False  # ✅ wait for organisers
            team.save()
            messages.success(request, "Payment proof uploaded. Waiting for verification by organisers.")
            return redirect('teamprofile')
    else:
        form = PaymentProofForm(instance=team)

    return render(request, 'team_profile/register_pay.html', {
        'team': team,
        'form': form
    })
