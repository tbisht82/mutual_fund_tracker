from django import forms

from .models import MutualFund


class MutualFundForm(forms.ModelForm):
    '''
        Django form for adding a new ISIN to database. Using ModelForm to create a new form object.
    '''
    class Meta:
        model = MutualFund
        fields = ('ISIN',)
        widgets = {
            'ISIN': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'enter ISIN here',
                    'id': 'isin'
                }
            ),
        }
