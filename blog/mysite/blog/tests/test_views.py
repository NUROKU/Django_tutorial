from django.test import TestCase
from django.urls import reverse

from ..models import Post

class IndexTests(TestCase):
    def test_get(self):
        # これだけでも書けってさ、
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)

class PostListTests(TestCase):
    def setUp(self):
        post1 = Post.objects.create(title="title1", text="text1")
        post2 = Post.objects.create(title="title2", text="text2")

    def test_get(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_get_2posts_by_list(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "title1")
        self.assertContains(response, "title2")

    def tearDown(self):
        post1 = Post.objects.create(title="title1", text="text1")
        post2 = Post.objects.create(title="title2", text="text2")

class PostCreateTests(TestCase):
    def test_get(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_with_data(self):
        response = self.client.post(reverse('blog:post_create'), data={
            'title': 'hoge',
            'text': 'huga'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_post_with_null(self):
        response = self.client.post(reverse('blog:post_create'), data={})
        self.assertEqual(response.status_code, 200)

class PostDetailTests(TestCase):
    def test_not_found_pk_get(self):
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_get(self):
        post = Post.objects.create(title="test", text="test")
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'pk': post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)

class PostUpdateTests(TestCase):
    def test_not_found_pk_get(self):
        response = self.client.get(
            reverse('blog:post_update', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 404)
    def test_get(self):
        post = Post.objects.create(title="test", text="test")
        response = self.client.get(
            reverse('blog:post_update', kwargs={'pk': post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)

class PostDeleteTests(TestCase):
    def test_not_found_pk_get(self):
        response = self.client.get(
            reverse('blog:post_delete', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, 404)
    def test_get(self):
        post = Post.objects.create(title="test", text="test")
        response = self.client.get(
            reverse('blog:post_delete', kwargs={'pk': post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.text)
