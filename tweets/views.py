from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from .forms import TweetForm
from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"


class TweetDetailView(ListView):
    model = Tweet
    template_name = "tweets/detail.html"
    # テンプレート内で {{ tweets }} で表示できる
    context_object_name = "tweets"


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = "tweets/create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tweets:detail', kwargs={'pk': self.object.pk})


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy('detail')
    template_name = "delete.html"
