from django import forms
from django.core.validators import validate_email
#from dajax.core import Dajax

issues = (
    (0, '-- Select Type of issue --'),
    (1, 'Blank Code / Incorrect code'),
    (2, 'Output error'),
    (3, 'Execution error'),
    (4, 'Missing example(s)'),
    (6, 'Blank output'),
    (7, 'Any other / General'),
)


class BugForm(forms.Form):
    example = forms.CharField(widget=forms.HiddenInput(), required=False)
    issue = forms.CharField(widget=forms.Select(choices=issues), required=True)
    description = forms.CharField(widget=forms.Textarea)
    email = forms.CharField(widget=forms.TextInput(), required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if not email:
            raise forms.ValidationError('Email id is required.')
        return email

    def clean(self):
        cleaned_data = super(BugForm, self).clean()
        issue = self.cleaned_data.get('issue', None)
        # example = self.cleaned_data.get('example', None)
        if (issue and int(issue) == ''):
            raise forms.ValidationError("""
                Please select book, chapter and example.
                Or select the *Any other/General* issue type.
            """)
        return cleaned_data


class RevisionForm(forms.Form):
    commit_message = forms.CharField(
        widget=forms.Textarea,
        required=True,
        min_length=10)
