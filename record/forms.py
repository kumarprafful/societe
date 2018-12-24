from django import forms
from record.models import Society, Member, MonthlyRecord

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = ['society_name', 'president', 'address',]

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'starting_share', 'starting_loan']

# class MonthlyRecordForm(forms.ModelForm):
#     class Meta:
#         model = MonthlyRecord
#