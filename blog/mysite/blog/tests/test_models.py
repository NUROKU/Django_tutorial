from django.test import TestCase
from blog.models import Post

# Create your tests here.

class PostModelTests(TestCase):
    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(),0)

    def test_is_count_one(self):
        post = Post(title="test", text="test_text")
        post.save()
        saved_post = Post.objects.all()
        self.assertEqual(saved_post.count(), 1)

    def test_saving_and_retrieing_post(self):
        post = Post(title="test", text="test_text")
        post.save()

        saved_post = Post.objects.all()
        actual_post = saved_post[0]

        self.assertEqual(actual_post.title, "test")