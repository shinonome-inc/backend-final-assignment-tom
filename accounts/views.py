from django.conf import settings
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from .forms import SignupForm
from tweets.models import Tweet

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_profile.html"
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_list"] = Tweet.objects.filter(user=self.object).select_related("user")
        return context
