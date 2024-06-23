from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")

    def test_success_get(self):
        self.url = reverse("tweets:home")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        post_data = {"content": "This is a test tweet!"}
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tweets:home"))
        self.assertTrue(Tweet.objects.filter(id=1).exists())
        self.assertEqual(Tweet.objects.get(id=1).text, post_data["text"])

    def test_failure_post_with_empty_content(self):
        not_available_data = {"text": ""}
        response = self.client.post(self.url, not_available_data)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("このフィールドは必須です。", form.errors["text"])
        self.assertFalse(Tweet.objects.filter(id=1).exists())

    def test_failure_post_with_too_long_content(self):
        too_long_content = "a" * (Tweet.objects.get_field("text").max_length + 1)
        max_length = Tweet.objects.get_field("text").max_length
        response = self.client.post(self.url, {"text": too_long_content})
        self.assertEqual(response.status_code, 200)
        form = response.text["form"]
        self.assertTrue(
            "このフィールドの文字数は {0} 文字以下にしてください。".format(max_length),
            form.errors["text"],
        )
        self.assertFalse(Tweet.objects.filter(id=1).exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.tweet1 = Tweet.objects.create(user=self.user, text="Test tweet 1")
        self.url = reverse("tweets:detail", kwargs={"pk": self.tweet1.pk})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tweet.objects.filter(text=self.tweet1.text).exists())


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpassword")
        self.client.login(username="tester", password="testpassword")
        self.tweet1 = Tweet.objects.create(user=self.user, text="Test tweet 1")
        self.url = reverse("tweets:delete", kwargs={"pk": self.tweet1.pk})

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, "/tweets/home/", status_code=302)
        self.assertFalse(Tweet.objects.filter(pk=self.tweet1.pk).exists())

    def test_failure_post_with_not_exist_tweet(self):
        queryset_before_deletion = Tweet.objects.all()
        not_exist_tweet_pk = 999
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": not_exist_tweet_pk}))
        self.assertEqual(response.status_code, 404)
        self.assertQuerysetEqual(Tweet.objects.all(), queryset_before_deletion)

    def test_failure_post_with_incorrect_user(self):
        queryset_before_deletion = Tweet.objects.all()
        self.user = User.objects.create_user(username="tester2", password="testpassword2")
        self.client.login(username="tester2", password="testpassword2")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertQuerysetEqual(Tweet.objects.all(), queryset_before_deletion)


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
