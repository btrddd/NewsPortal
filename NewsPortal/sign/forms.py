from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms


from news_feed.models import Category, CategorySubscribers


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


class CategorySubscribeForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        label='Категория',
        empty_label=None,
        queryset=Category.objects
    )


    class Meta:
        model = CategorySubscribers
        fields = ['category']