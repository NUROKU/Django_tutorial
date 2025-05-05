from django.urls import reverse_lazy
from django.views import generic

from .forms import PostCreateForm
from .models import Post

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "blog/index.html"

class PostListView(generic.ListView):
    model = Post

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:post_list')

class PostDetailView(generic.DetailView):
    model = Post

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')