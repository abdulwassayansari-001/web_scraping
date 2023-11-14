# from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from data.models import DataScrap
from django.contrib.auth.decorators import login_required
from verify_email.models import UserVerification

# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Your Account has been created! You are now able to login')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your Account has been Updated!')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form': u_form,
#         'p_form': p_form
#     }
#     return render(request, 'users/profile.html', context)

from django.shortcuts import render, redirect
from admin_argon.forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm,
)
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
from django.contrib.auth import logout


# Create your views here.
@login_required
def index(request):
    scrap_data = DataScrap.objects.all()

    total_items = scrap_data.count()
    total_unvalidated = scrap_data.filter(validation__isnull=True).count()
    total_accepted = scrap_data.filter(validation=True).count()
    total_rejected = scrap_data.filter(validation=False).count()

    context = {
        "total_items": total_items,
        "total_unvalidated": total_unvalidated,
        "total_accepted": total_accepted,
        "total_rejected": total_rejected,
    }

    return render(request, "pages/dashboard.html", context)


def billing(request):
    return render(request, "pages/billing.html")


def profile(request):
    return render(request, "pages/profile.html")


def tables(request):
    return render(request, "pages/tables.html")


def rtl(request):
    return render(request, "pages/rtl.html")


def vr(request):
    return render(request, "pages/virtual-reality.html")


# def register(request):
#   if request.method == 'POST':
#     form = RegistrationForm(request.POST)
#     if form.is_valid():
#       form.save()
#       print("Account created successfully!")
#       return redirect('/accounts/login/')
#     else:
#       print("Registration failed!")
#   else:
#     form = RegistrationForm()

#   context = { 'form': form }
#   return render(request, 'accounts/sign-up.html', context)

from verify_email.email_handler import send_verification_email

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            existing_user = (
                get_user_model()
                .objects.filter(email=form.cleaned_data["email"])
                .first()
            )
            if existing_user:
                form.add_error("email", "An account with this email already exists.")
                return render(request, "accounts/sign-up.html", {"form": form})

            try:
                user = form.save(commit=False)
                user.save()
            except Exception as e:
                # Handle other potential exceptions during user save
                form.add_error(None, f"An error occurred: {str(e)}")
                return render(request, "accounts/sign-up.html", {"form": form})

            # Create UserVerification instance
            UserVerification.objects.create(user=user)

            # Now that the user is successfully saved, send the verification email
            send_verification_email(request, form)

            messages.success(
                request,
                f"Your account has been created! Check your email for verification.",
            )

            return render(
                request,
                template_name="accounts/signup_success.html",
                context={"status": "Account Created Successfully!"},
            )
    else:
        form = UserRegisterForm()

    context = {"form": form}
    return render(request, "accounts/sign-up.html", context)


class UserLoginView(LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = LoginForm


class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    form_class = UserPasswordChangeForm


def user_logout_view(request):
    logout(request)
    return redirect("/login/")
