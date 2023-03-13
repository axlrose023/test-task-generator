from django import forms
from .models import DataSchema, Column


class SchemaForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DataSchema
        fields = ['title', 'column_separator', 'string_character']


class SchemaColumnsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Column
        fields = ['name', 'data_type', 'range_min', 'range_max', 'order']


class EditSchemaForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = DataSchema
        fields = ['title', 'column_separator', 'string_character']

