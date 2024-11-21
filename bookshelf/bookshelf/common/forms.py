from django import forms
from .models import Report


class ReportBaseForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ['created_at', 'user']


class CreateReportForm(ReportBaseForm):
    class Meta(ReportBaseForm.Meta):
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'report_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your report...'})
        }

        labels = {
            'report_text': 'Report Details'
        }