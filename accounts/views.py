from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import CustomUser
from django.conf import settings


def register(request):
    """
    Handles user registration.

    This view is triggered when a user submits the registration form. It processes the form data,
    creates a new user, logs them in, generates an email verification code, and sends it to the
    user's email address. The code is then saved in the session for later verification.

    If the form is valid:
        - Creates a new user.
        - Logs in the user.
        - Generates a verification code.
        - Sends the verification code to the user's email address.
        - Redirects to the email verification page.

    If the form is not submitted or is invalid, it simply renders the registration form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The response containing the rendered registration form or a redirect to the verification page.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Generate verification code
            verification_code = user.generate_verification_code()

            # Store the code in session or database (for future validation)
            request.session["verification_code"] = verification_code

            # Send email with verification code
            send_mail(
                subject="کد تأیید ایمیل",
                message=f"کد تأیید شما: {verification_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            print(f"Generated verification code: {verification_code}")

            return redirect("verify_email")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def verify_email(request):
    """
    Handles email verification.

    This view is triggered when the user enters the verification code received via email.
    It compares the submitted code with the code stored in the session. If the codes match,
    the session code is deleted, and the user is redirected to the post list page.
    If the code is incorrect, an error message is displayed.

    If the POST request is valid:
        - Compares the submitted verification code with the stored one.
        - Redirects to the post list page if the code is correct.
        - Displays an error message if the code is incorrect.

    If the request method is GET, it simply renders the verification page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The response containing the verification page or a redirect to the post list.
    """
    if request.method == "POST":
        input_code = request.POST.get("verification_code")
        stored_code = request.session.get("verification_code")

        if input_code == stored_code:
            del request.session[
                "verification_code"
            ]  # Delete code from session after verification
            return redirect("post_list")

        else:
            return HttpResponse("کد تأیید نادرست است.")

    return render(request, "registration/verify_email.html")
