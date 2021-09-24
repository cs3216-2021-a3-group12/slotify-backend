from django.core.mail import EmailMessage
from authentication.models import User
from events.models import Event, SignUp


class SignupUtil:
    @staticmethod
    def send_registration_confirmation(user: User, event: Event, signup: SignUp):
        signup_status = "Confirmed" if signup.is_confirmed else "Waitlisted"
        status_message = "Your registration has been confirmed!" if signup.is_confirmed \
            else """ 
            You are currently waitlisted. You will be registered immediately (on a 
            first-come-first-serve basis) if a slot becomes available.
            """

        email_subject = f"Slotify App | Event sign up | {signup_status}"
        email_body = \
        f"""
        Hi {user.username}!
        
        You have signed up for the following event. 
        
        {status_message}
        
        Event: {event.title}
        Date and time: {event.start_date_time} - {event.end_date_time}
        Location: {event.location}
        Organizing group: {event.group.name}

        Check out the event at the following link:
        https://slotify.club/events/{event.id}

        Check out the organizing group at the following link:
        https://slotify.club/groups/{event.group.id}
        """

        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()

    @staticmethod
    def send_waitlist_confirmation_notification(user: User, event: Event):
        email_subject = f"Slotify App | Event sign up | Confirmed"
        email_body = \
        f"""
        Hi {user.username}!
        
        You have been moved from the waitlist, and your sign up for the following event has been confirmed!
        
        Event: {event.title}
        Date and time: {event.start_date_time} - {event.end_date_time}
        Location: {event.location}
        Organizing group: {event.group.name}

        Check out the event at the following link:
        https://slotify.club/events/{event.id}

        Check out the organizing group at the following link:
        https://slotify.club/groups/{event.group.id}
        """

        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()