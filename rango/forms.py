from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(),required=False)

    #inline class to provide additional information on form
    class Meta:
        #provide an association between the ModelForm and a model
        model = Category
        fields=('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter page title")
    url = forms.URLField(max_length=200, help_text="Please enter page URL")
    views = forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model = Page
        #what fields to include in form, easier to simply exclude category field from form
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        #if url is not empty and doesn't have http:// add this to start
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data

# user stuff
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
