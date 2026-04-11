from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, 
    DeleteView, TemplateView)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from .models import Post
from .forms import PostForm
from .filters import PostFilter
from NewsPortal.settings import EMAIL_FROM


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


    def send_mail(self, post: Post):
        subscribers = set()
        for category in post.category.all():
            subscribers.update(
                set(category.subscribers.filter().values_list('username', 'email'))
            )
        
        for subscriber in subscribers:
            html_content = render_to_string(
                'post_email_message.html',
                {
                    'post': post,
                    'username': subscriber[0],
                }
            )

            message = EmailMultiAlternatives(
                subject=post.title,
                body=post.text,
                from_email=EMAIL_FROM,
                to=[subscriber[1]]
            )

            message.attach_alternative(html_content, 'text/html')
            message.send()
    

class NewsCreate(PostCreate):
    def form_valid(self, form):
        post: Post = form.save(commit=False)
        post.post_type = 'NE'
        post.save()
        form.save_m2m()
        self.send_mail(post)        
        return super().form_valid(form)
    

class ArticleCreate(PostCreate):
    def form_valid(self, form):
        post: Post = form.save(commit=False)
        post.post_type = 'AR'
        post.save()
        form.save_m2m()
        self.send_mail(post)        
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
