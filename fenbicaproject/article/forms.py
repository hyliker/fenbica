#coding: utf-8
from django import forms
from django.contrib.auth.models import User
from article.models import Article, Attachment, ArticleCategory

class EditArticleForm(forms.ModelForm):
    """编辑日志"""
    class Meta:
        model = Article
        exclude = ["read_count", "comment_count", "author"]

class AddArticleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(AddArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ArticleCategory.objects.filter(author=user)

    class Meta:
        model = Article
        exclude = ["read_count", "comment_count", "author"]

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file",]

class ArticleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = ArticleCategory.objects.filter(author=user)

    class Meta:
        model = Article
        exclude = ["read_count", "comment_count", "author"]
