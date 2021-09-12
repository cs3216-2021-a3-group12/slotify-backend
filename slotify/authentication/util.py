from django.urls import reverse
from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class RegistrationUtil:
    @staticmethod
    def send_email_verification(user: User, domain: str):    
        access_token = RefreshToken.for_user(user).access_token    
        relative_link = reverse('verify-email')

        # TODO: replace with https eventually
        verification_link = f"http://{domain}{relative_link}?token={str(access_token)}"

        username = user.username

        email_subject = f"Slotify App: Verify your email address"
        email_body = \
        f"""Hi {username}!
        Thank you for registering to use Slotify!
        Please use the following link to verify your email:
        
        {verification_link}
        """

        print("ACCESS TOKEN:", access_token)

        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()