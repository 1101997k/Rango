from django import forms
from rango.models import Page, Category

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
