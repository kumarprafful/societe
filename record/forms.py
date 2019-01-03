from django import forms
from record.models import Society, Member, MonthlyRecord, SocietySetting

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = ['society_name', 'president', 'address',]

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'starting_share', 'starting_loan']
        widget=forms.TextInput(attrs={'class': "input-field"})


class NewMonthlyRecordForm(forms.ModelForm):
    class Meta:
        model = MonthlyRecord
        fields = ['installment',]

class MonthlyRecordForm(forms.ModelForm):
    class Meta:
        model = MonthlyRecord
        exclude = ('__all__')

class SocietySettingForm(forms.ModelForm):
    class Meta:
        model = SocietySetting
        exclude = ['society']
