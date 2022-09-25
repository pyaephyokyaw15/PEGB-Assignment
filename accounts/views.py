from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from accounts.utils import generate_token
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.conf import  settings


User = get_user_model()

# Create your views here.

def send_account_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
                 to=[user.email])
    email.send()


def activate_user(request, uidb64, token):

    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None


    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/success.html')

    return render(request, 'authentication/error.html')