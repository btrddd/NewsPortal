from django.views.generic import TemplateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


from news_feed.models import CategorySubscribers
from .forms import CategorySubscribeForm


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['category_subscriptions'] = CategorySubscribers.objects.filter(
            user=self.request.user)
        return context


@login_required
def upgrade_profile(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news')


class CategorySubscribe(LoginRequiredMixin, CreateView):
    model = CategorySubscribers
    form_class = CategorySubscribeForm
    template_name = 'category_subscribe.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        subscribe = form.save(commit=False)
        subscribe.user = self.request.user
        return super().form_valid(form)
        

@login_required
def category_unsubscribe(request, pk):
    subscription = get_object_or_404(CategorySubscribers, pk=pk)
    if request.method == 'POST':
        subscription.delete()
    return redirect('profile')
