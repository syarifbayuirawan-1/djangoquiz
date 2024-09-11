from django import forms
from .models import Question, Choice

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', None)
        super().__init__(*args, **kwargs)
        if questions:
            for question in questions:
                choices = [(choice.id, choice.text) for choice in question.choices.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=choices,
                    widget=forms.RadioSelect,
                    label=question.text
                )

    def clean(self):
        cleaned_data = super().clean()
        for key in self.fields:
            if not cleaned_data.get(key):
                self.add_error(key, 'This question is required.')
        return cleaned_data
