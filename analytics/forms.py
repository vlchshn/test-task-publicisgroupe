from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Select file (CSV/XLSX)",
        widget=forms.FileInput(
            attrs={"class": "form-control", "accept": ".csv, .xls, .xlsx"}
        ),
    )
