from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tweets"] = Tweet.objects.all()  # すべてのツイートを取得
        return context


class TweetDetailView(ListView):
    model = Tweet
    template_name = "tweets/detail.html"
    # テンプレート内で {{ tweets }} で表示できる
    context_object_name = "tweets"

    def get_queryset(self):
        # pk を使って特定のツイートを取得
        return Tweet.objects.filter(pk=self.kwargs["pk"])


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ["text"]
    template_name = "tweets/create.html"

    success_url = reverse_lazy("tweets:home")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy("tweets:home")
    template_name = "delete.html"
