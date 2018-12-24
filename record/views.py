from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from record.models import Society, Member, MonthlyRecord
from record.forms import SocietyForm, MemberForm
# Create your views here.

def index(request):
    return render(request, 'record/index.html')

def dashboard(request):
    societies = Society.objects.all()
    return render(request, 'record/dashboard.html', {'societies': societies})

def addSocietyView(request):
    if request.method == 'POST':
        society_form = SocietyForm(data=request.POST)
        if society_form.is_valid():
            society_form.save()
        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        society_form = SocietyForm()
            # return HttpResponseRedirect(reverse('record:index'))
    return render(request, 'record/add_society.html', {'society_form': society_form})

def addMemberView(request, id):
    if request.method == 'POST':
        society = Society.objects.get(id=id)
        member_form = MemberForm(data=request.POST)
        if member_form.is_valid():
            member = member_form.save(commit=False)
            member.society = society
            member.fill_month()
            print(member_form)
            member.save()

            # MonthlyRecord.objects.create(member=member)
        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        member_form = MemberForm()
    return render(request, 'record/add_member.html', {'member_form': member_form})
