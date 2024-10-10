from django.shortcuts import render,redirect
from app.models import Registration, Event, RegistrationStatus
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def HOME(request):
    # Get the current registration status
    registration_status = RegistrationStatus.objects.first()  # Assuming only one instance

    if registration_status and not registration_status.is_open:
        return render(request, 'closed.html')
    
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        # Extract individual records from the form
        name = request.POST.get('name')
        college = request.POST.get('college')
        department = request.POST.get('dept')
        paper_title = request.POST.get('paper_title')
        paper_abstract = request.POST.get('paper_abstract')
        payment_mode = request.POST.get('payment_mode')  # New payment mode field
        payment_link = request.POST.get('payment_link') if payment_mode == 'Online' else None
        transaction_number = request.POST.get('transaction_number') if payment_mode == 'Online' else None
        technical_events = request.POST.getlist('technical_events')
        non_technical_events = request.POST.getlist('non_technical_event')

        # Create a new Registration instance
        registration = Registration(
            name=name,
            college=college,
            department=department,
            paper_title=paper_title,
            paper_abstract=paper_abstract,
            payment_mode=payment_mode,
            payment_link=payment_link,
            transaction_number=transaction_number,
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            food_preference=request.POST.get('food_preference'),
        )

        # Generate member_id
        count = Registration.objects.count() + 1
        registration.member_id = f'CISABZ/CSE/{count:02d}'
        registration.save()  # Save the registration first

        # Add selected technical events
        for event_name in technical_events:
            event_instance, created = Event.objects.get_or_create(name=event_name, event_type='technical')
            registration.technical_events.add(event_instance)

        # Add selected non-technical events
        for event_name in non_technical_events:
            event_instance, created = Event.objects.get_or_create(name=event_name, event_type='non_technical')
            registration.non_technical_events.add(event_instance)

        # Prepare email content
        subject = 'CISABZ\'24 Symposium Registration Successful'

        html_message = render_to_string('email-sending.html', {
            'name': name,
            'college': college,
            'department': department,
            'paper_title': paper_title,
            'technical_events': technical_events,
            'non_technical_events': non_technical_events,
            'member_id': registration.member_id,
            'payment_mode': payment_mode,  # Include payment mode in email
        })
        plain_message = strip_tags(html_message)
        from_email = 'cisabz2k24@gmail.com'
        to_email = registration.email   # Send to the user's email

        # Send email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        # After saving, redirect to a success page with the member ID
        return render(request, 'success.html', {'member_id': registration.member_id})

    # If not POST, return the registration form
    return render(request, 'home.html')


def search_registration(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        registration = Registration.objects.filter(member_id=member_id).first()
        return render(request, 'search.html', {'registration': registration})
    
    return render(request, 'search.html')
