from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import SignUpForm, LoginForm
from .models import User
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = 'home.html'

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        resp = super().form_valid(form)
        user = self.object
        if user.requires_approval():
            messages.success(self.request,
                "Account created. An administrator must approve your account before you can sign in.")
        else:
            messages.success(self.request, "Account created. You can sign in now.")
        return resp

class SignInView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        # Only block login if approval is required and not yet approved
        if hasattr(user, "requires_approval") and user.requires_approval() and not user.is_approved:
            messages.error(self.request, "Your account is pending admin approval.")
            return redirect('login')
        # If approved, let Django handle login + session
        return super().form_valid(form)

class SignOutView(LogoutView):
    next_page = reverse_lazy('login')