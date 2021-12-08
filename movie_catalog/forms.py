from django import forms
from difflib import SequenceMatcher
import numpy as np
import itertools

from django.core.exceptions import ValidationError

from .models import Comment, Review


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text', 'star')

    def match_texts(self, text1, text2):
        '''returns true if the two texts match 70 percent or more'''
        similarity = lambda x: np.mean([SequenceMatcher(None, a, b).ratio() for a, b in itertools.combinations(x, 2)])
        text1, text2 = ' '.join(sorted(text1.lower().split())), ' '.join(sorted(text2.lower().split()))
        return similarity([text1, text2]) >= 0.7

    def clean(self):
        clean_data = super().clean()
        text = clean_data['text']
        for other_review in Review.objects.all():
            if self.match_texts(text, other_review.text):
                self.add_error('text', 'Уже существует рецензия с похожим текстом')

