from  django import forms
from django.core.validators import validate_email

issues = (
    ('', '-- Select Type of issue --'),
    (1, 'Blank Code / Incorrect code'),
    (2, 'Output error'),
    (3, 'Execution error'),
    (4, 'Missing example(s)'),
    (6, 'Blank output'),
    (7, 'Any other / General'),
)


class BugForm(forms.Form):
    example = forms.CharField(widget=forms.HiddenInput(), required=False)
    issue = forms.CharField(widget=forms.Select(choices=issues))
    description = forms.CharField(widget=forms.Textarea)
    notify = forms.BooleanField(required=False)
    email = forms.CharField(required=False)

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        notify = self.cleaned_data.get('notify', None)
        if notify and not email:
            raise forms.ValidationError('Email id is required if you want to be notified.')
        elif notify:
            validate_email(email)

    def clean(self):
        issue = self.cleaned_data.get('issue', None)
        example = self.cleaned_data.get('example', None)
        if (issue and int(issue) != 7) and (not example):
            raise forms.ValidationError("""
                Please select book, chapter and example.
                Or select the *Any other/General* issue type.
            """)


class RevisionForm(forms.Form):
    commit_message = forms.CharField(widget=forms.Textarea)