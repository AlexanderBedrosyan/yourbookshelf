from django import forms
from .models import Report


class ReportBaseForm(forms.ModelForm):

    class Meta:
        model = Report
        exclude = ['created_at', 'user']


class ReportDeleteForm(ReportBaseForm):
    pass


class DetailReportForm(ReportBaseForm):
    class Meta(ReportBaseForm.Meta):
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'report_text': forms.Textarea(attrs={'class': 'form-control'})
        }

        labels = {
            'report_text': 'Report Details'
        }


class CreateReportForm(ReportBaseForm):
    class Meta(ReportBaseForm.Meta):
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'report_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your report...'})
        }

        labels = {
            'report_text': 'Report Details'
        }
