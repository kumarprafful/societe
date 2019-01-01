from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from record.models import Society, Member, MonthlyRecord
from record.forms import SocietyForm, MemberForm, NewMonthlyRecordForm, MonthlyRecordForm

from record import functions as func

from datetime import datetime
# Create your views here.

# def index(request):
#     return render(request, 'record/index.html')

@login_required(login_url=reverse_lazy('account:user_login'))
def dashboard(request):
    societies = Society.objects.filter(user=request.user)
    return render(request, 'record/dashboard.html', {'societies': societies})

@login_required(login_url=reverse_lazy('account:user_login'))
def society_dash(request, slug):
    society = Society.objects.get(slug=slug, user=request.user)
    members = Member.objects.filter(society=society)
    return render(request, 'record/society_dash.html', {'society': society, 'members': members})

@login_required(login_url=reverse_lazy('account:user_login'))
def monthly_record(request, slug, month=datetime.now().month):
    society = Society.objects.get(slug=slug);
    monthly_records = MonthlyRecord.objects.filter(member__society=society, month=month)
    return render(request, 'record/monthly_record.html', {'society': society,'monthly_records': monthly_records})

@login_required(login_url=reverse_lazy('account:user_login'))
def createMonthlyRecordView(request, slug, id, month):
    if request.method=='POST':
        member = Member.objects.get(id=id)
        prevRecord = MonthlyRecord.objects.get(member=member, month=month)
        new_record_form = NewMonthlyRecordForm(data=request.POST)
        if new_record_form.is_valid():
            record = new_record_form.save(commit=False)
            record.member = member
            record.month = func.getNextMonth(prevRecord.month)
            record.previous_share = prevRecord.total_share
            record.previous_loan = prevRecord.balance_loan
            record.share = func.fill_share(200)
            record.total_share = func.fill_total_share(record.previous_share, record.share)
            record.balance_loan = func.fill_balance_loan(record.previous_loan, int(new_record_form.data['installment']))
            record.interest = func.fill_interest(record.previous_loan)
            record.total_amount = func.fill_total_amount(record.share, record.installment, record.interest)
            record.save()
            return HttpResponseRedirect(reverse('record:monthly-record', kwargs={'slug':prevRecord.member.society.slug}))
    else:
        new_record_form = NewMonthlyRecordForm()
    return render(request, 'record/new_monthly_record.html', {'new_record_form': new_record_form})

@login_required(login_url=reverse_lazy('account:user_login'))
def addSocietyView(request):
    if request.method == 'POST':
        society_form = SocietyForm(data=request.POST)
        if society_form.is_valid():
            society = society_form.save(commit=False)
            society.user = request.user
            society.save()

        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        society_form = SocietyForm()
            # return HttpResponseRedirect(reverse('record:index'))
    return render(request, 'record/add_society.html', {'society_form': society_form})

@login_required(login_url=reverse_lazy('account:user_login'))
def addMemberView(request, slug):
    if request.method == 'POST':
        society = Society.objects.get(slug=slug)
        member_form = MemberForm(data=request.POST)
        record_form = MonthlyRecordForm()
        if member_form.is_valid():
            member = member_form.save(commit=False)

            member.society = society
            member.fill_month()
            member.save()

            first_record = MonthlyRecord()

            record_form = record_form.save(commit=False)
            record_form.member = member
            record_form.year = first_record.fill_year()
            record_form.month = first_record.fill_month()
            record_form.previous_share = member.starting_share
            record_form.previous_loan = member.starting_loan
            record_form.share = func.fill_share(200)
            record_form.total_share = func.fill_total_share(member.starting_share, 200)
            record_form.installment = func.fill_installment(0)
            record_form.balance_loan = func.fill_balance_loan(member.starting_loan, 0)
            record_form.interest = func.fill_interest(member.starting_loan)
            record_form.total_amount = func.fill_total_amount(record_form.share, record_form.installment, record_form.interest)
            record_form.save()

        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        member_form = MemberForm()
    return render(request, 'record/add_member.html', {'member_form': member_form})
