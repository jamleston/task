from django import forms
from .models import Expense
from .models import Category


class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name',)

    name = forms.CharField(required=False, label="Search by Name")
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
