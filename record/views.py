from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from record.models import Society, Member, MonthlyRecord, SocietySetting
from record.forms import SocietyForm, MemberForm, NewMonthlyRecordForm, MonthlyRecordForm, SocietySettingForm, EditMonthlyRecordForm

from record import functions as func

from datetime import datetime
# Create your views here.

@login_required(login_url=reverse_lazy('account:user_login'))
def dashboard(request):
    societies = Society.objects.filter(user=request.user)
    return render(request, 'record/dashboard.html', {'societies': societies})

@login_required(login_url=reverse_lazy('account:user_login'))
def society_dash(request, slug):
    society = Society.objects.get(slug=slug, user=request.user)
    members = Member.objects.filter(society=society, active=1)
    return render(request, 'record/society_dash.html', {'society': society, 'members': members})

@login_required(login_url=reverse_lazy('account:user_login'))
def monthly_record(request, slug):
    society = Society.objects.get(slug=slug)
    monthly_records = MonthlyRecord.objects.filter(member__society=society, installment_filled=False, member__active=1)
    return render(request, 'record/monthly_record.html', {'society': society,'monthly_records': monthly_records})

@login_required(login_url=reverse_lazy('account:user_login'))
def monthly_record_ajax(request, slug, month=datetime.now().month):
    society = Society.objects.get(slug=slug);
    monthly_records = MonthlyRecord.objects.filter(member__society=society, month=month, installment_filled=False, member__active=1).values('balance_loan', 'date', 'id', 'installment', 'interest', 'late_fees', 'member','member_name', 'member_id', 'month', 'previous_loan', 'previous_share', 'remarks', 'share', 'total_amount', 'total_share', 'year')

    return JsonResponse({'monthly_records': list(monthly_records)}, content_type="application/json")

@login_required(login_url=reverse_lazy('account:user_login'))
def all_record(request, slug):
    society = Society.objects.get(slug=slug)
    records = MonthlyRecord.objects.filter(member__society=society, member__active=1).order_by('-month')
    return render(request, 'record/all_records.html', {'society':society, 'records': records})

@login_required(login_url=reverse_lazy('account:user_login'))
def createMonthlyRecordView(request, slug, id, month):
    society = Society.objects.get(slug=slug)
    society_settings = SocietySetting.objects.get(society=society)
    if request.method=='POST':
        member = Member.objects.get(id=id)
        prevRecord = MonthlyRecord.objects.get(member=member, month=month, member__active=1)
        new_record_form = NewMonthlyRecordForm(data=request.POST)
        if new_record_form.is_valid():
            record = new_record_form.save(commit=False)
            record.member = member
            record.member_name = member.name
            record.month = func.getNextMonth(prevRecord.month)
            record.year = func.getNextYear(prevRecord.month, prevRecord.year)
            record.previous_share = prevRecord.total_share
            record.previous_loan = prevRecord.balance_loan
            record.share = func.fill_share(society_settings.basic_share)
            record.total_share = func.fill_total_share(record.previous_share, record.share)
            record.balance_loan = func.fill_balance_loan(record.previous_loan, int(new_record_form.data['installment']))
            prevRecord.installment_filled = 1
            record.interest = func.fill_interest(society_settings.interest_rate,record.previous_loan)
            record.total_amount = func.fill_total_amount(record.share, record.installment, record.interest)
            prevRecord.save()
            record.save()
            return HttpResponseRedirect(reverse('record:monthly-record', kwargs={'slug':prevRecord.member.society.slug}))
    else:
        new_record_form = NewMonthlyRecordForm()
    return render(request, 'record/new_monthly_record.html', {'new_record_form': new_record_form, 'society': society})

@login_required(login_url=reverse_lazy('account:user_login'))
def editMonthlyRecordView(request, member_id, month, slug):
    society = Society.objects.get(slug=slug)
    member = Member.objects.get(id=member_id)
    member_record = MonthlyRecord.objects.get(member=member, month=month)
    if request.method == 'POST':
        edit_record_form = EditMonthlyRecordForm(data=request.POST, instance=member_record)
        if edit_record_form.is_valid():
            record = edit_record_form.save(commit=False)
            member.name = record.member_name
            record.save()
            member.save()
            return HttpResponseRedirect(reverse('record:all-records', kwargs={'slug':slug}))
    else:
        edit_record_form = EditMonthlyRecordForm(instance=member_record)
    return render(request, 'record/edit_record.html', {'edit_record_form': edit_record_form, 'society': society})

@login_required(login_url=reverse_lazy('account:user_login'))
def addSocietyView(request):
    if request.method == 'POST':
        society_form = SocietyForm(data=request.POST)
        if society_form.is_valid():
            society = society_form.save(commit=False)
            society.user = request.user
            society.save()
            SocietySetting.objects.create(society=society)
            return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        society_form = SocietyForm()
            # return HttpResponseRedirect(reverse('record:index'))
    return render(request, 'record/add_society.html', {'society_form': society_form})

@login_required(login_url=reverse_lazy('account:user_login'))
def society_settings(request, slug):
    settings = SocietySetting.objects.get(society__slug=slug)
    if request.method == 'POST':
        settings_form = SocietySettingForm(data=request.POST, instance=settings)
        if settings_form.is_valid():
            settings_form.save()
            return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        settings_form = SocietySettingForm(instance=settings)
    return render(request, 'record/society_settings.html', {'settings_form': settings_form})

@login_required(login_url=reverse_lazy('account:user_login'))
def addMemberView(request, slug):
    society = Society.objects.get(slug=slug)
    society_settings = SocietySetting.objects.get(society=society)
    if request.method == 'POST':
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
            record_form.member_name = member.name
            record_form.year = first_record.fill_year()
            record_form.month = first_record.fill_month()
            record_form.previous_share = member.starting_share
            record_form.previous_loan = member.starting_loan
            record_form.share = func.fill_share(society_settings.basic_share)
            record_form.total_share = func.fill_total_share(member.starting_share, society_settings.basic_share)
            record_form.installment = func.fill_installment(0)
            record_form.balance_loan = func.fill_balance_loan(member.starting_loan, 0)
            record_form.interest = func.fill_interest(society_settings.interest_rate, member.starting_loan)
            record_form.total_amount = func.fill_total_amount(record_form.share, record_form.installment, record_form.interest)
            record_form.save()

        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        member_form = MemberForm()
    return render(request, 'record/add_member.html', {'member_form': member_form, 'society': society})


@login_required(login_url=reverse_lazy('account:user_login'))
def delete_member_view(request, soc_id, id):
    member = Member.objects.get(society_id=soc_id, id=id)
    member.active = 0
    member.save()
    return HttpResponseRedirect(reverse('record:society-dash', kwargs = {'slug':member.society.slug}))
