from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Registration View
class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')  # Redirect to login after successful registration

    def form_valid(self, form):
        # Automatically log in the user after registration
        user = form.save()
        messages.success(self.request, "Registration successful!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Registration failed. Please correct the errors.")
        return super().form_invalid(form)

# Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, f"Welcome back, {self.request.user.username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

# Logout View
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redirect to login after logout

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'