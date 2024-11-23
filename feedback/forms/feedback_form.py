from django import forms

from ..models import Feedback
INFRASTRCUTURE = 'INF'
GENERIC = 'GEN'
CURRICULUM = 'CUR'

FEEDBACK_CHOICES = (
        (INFRASTRCUTURE,'Infrastructure'),
        (GENERIC,'Generic'),
        (CURRICULUM,'Curriculum'),
    )

class FeedbackForm(forms.ModelForm):
    username = forms.CharField(max_length=120, required=False)
    text = forms.CharField(max_length=400, widget=forms.Textarea())
    class Meta:
         model = Feedback
         include = ['username']
         exclude = ['user']

    def __init__(self, *args, **kwargs):
        size = kwargs.pop('size')
        maxChars = kwargs.pop('maxChars')
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['text'].widget.attrs['onkeypress'] = 'return textCounter(this,this.form.counter,%d);'% maxChars
        self.fields['text'].widget.attrs['rows'] = size
        self.fields['text'].widget.attrs['cols'] ='40'

