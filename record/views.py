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
            member.save()

            first_record = MonthlyRecord()
            MonthlyRecord.objects.create(member=member,
                                                    year=first_record.fill_year(),
                                                    month=first_record.fill_month(),
                                                    previous_share=member.starting_share,
                                                    previous_loan=member.starting_loan,
                                                    share=first_record.fill_share(),
                                                    total_share=first_record.fill_total_share(member.starting_share, 200),
                                                    installment=first_record.fill_installment(5000),
                                                    balance_loan=first_record.fill_balance_loan(member.starting_loan, 5000),
                                                    interest=first_record.fill_interest(member.starting_loan),
                                                    # total_amount=first_record.fill_total_amount,
                                            )

            # first_record.year = first_record.fill_year
            # first_record.previous_share = member.starting_share
            # first_record.previous_loan = member.starting_loan
            # first_record.share = first_record.fill_share
            # first_record.total_share = first_record.fill_total_share
            # first_record.installment = first_record.fill_installment
            # first_record.balance_loan = first_record.fill_balance_loan
            # first_record.interest = first_record.fill_interest
            # first_record.total_amount = first_record.fill_total_amount
            #
            #
            #
            # print(first_record.interest)
            # first_record.save()


        return HttpResponseRedirect(reverse('record:dashboard'))
    else:
        member_form = MemberForm()
    return render(request, 'record/add_member.html', {'member_form': member_form})
