# landing_page/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Sponsor, Query, GeneralQuery

def main_landing_page_view(request):
    """
    Renders the new main landing page (index.html).
    """
    # No specific data needed for the main landing page, but you can add it if sections become dynamic.
    return render(request, 'landing_page/index.html')

def landing_page_sponsor_view(request):
    """
    Renders the dedicated sponsor page (sponsor.html), fetching sponsors.
    """
    sponsors = Sponsor.objects.all().order_by('tier')
    
    # Organize sponsors by tier for easier rendering in the template
    sponsors_by_tier = {
        'Gold': [],
        'Platinum': [],
        'Silver': [],
        'Bronze': []
    }
    for sponsor in sponsors:
        sponsors_by_tier[sponsor.tier].append(sponsor)

    past_sponsors = Sponsor.objects.all() # Or filter by a field like `is_past_sponsor=True`

    context = {
        'sponsors_by_tier': sponsors_by_tier,
        'past_sponsors': past_sponsors,
    }
    return render(request, 'landing_page/sponsor.html', context)

def general_query_submit_view(request):
    """
    Handles submissions from the general query form on the main landing page.
    Uses the GeneralQuery model.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        contact_email = request.POST.get('contact_email')
        institution_name = request.POST.get('institution_name')
        message_text = request.POST.get('message')

        if not all([name, contact_email, message_text]):
            messages.error(request, "Please fill in all required fields (Name, Email, Message).")
            return redirect(reverse('landing_page:main_landing_page') + '#queries')

        try:
            GeneralQuery.objects.create(
                name=name,
                contact_email=contact_email,
                institution_name=institution_name,
                message=message_text
            )
            messages.success(request, "Your query has been sent successfully! We'll get back to you soon.")
            return redirect(reverse('landing_page:main_landing_page') + '#queries')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}. Please try again later.")
            return redirect(reverse('landing_page:main_landing_page') + '#queries')

    return redirect('landing_page:main_landing_page')

def sponsor_contact_submit_view(request):
    """
    Handles submissions from the sponsor contact form on the dedicated sponsor page.
    Uses the Query model (for sponsor inquiries).
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        organisation = request.POST.get('organisation')
        contact_email = request.POST.get('contact_email')
        mobile_number = request.POST.get('mobile_number')
        message_text = request.POST.get('message')

        if not all([name, contact_email, message_text]):
            messages.error(request, "Please fill in all required fields for sponsor inquiry.")
            return redirect(reverse('landing_page:sponsor_page') + '#contact')

        try:
            Query.objects.create( # Using the 'Query' model for sponsor inquiries
                name=name,
                organisation=organisation,
                contact_email=contact_email,
                mobile_number=mobile_number,
                message=message_text
            )
            messages.success(request, "Your sponsor inquiry has been sent successfully! We'll get back to you soon.")
            return redirect(reverse('landing_page:sponsor_page') + '#contact')
        except Exception as e:
            messages.error(request, f"An error occurred with your sponsor inquiry: {e}. Please try again later.")
            return redirect(reverse('landing_page:sponsor_page') + '#contact')

    return redirect('landing_page:sponsor_page') # Redirect to sponsor page if not a POST request
