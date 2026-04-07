from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, 
    DeleteView, TemplateView)
from django.contrib.auth.mixins import PermissionRequiredMixin


from .models import Post
from .forms import PostForm
from .filters import PostFilter


class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news_feed.add_post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    

class NewsCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'NE'
        return super().form_valid(form)
    

class ArticleCreate(PostCreate):
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'AR'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news_feed.change_post')
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news_feed.delete_post')
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostSearch(PostList):
    template_name = 'post_search.html'
