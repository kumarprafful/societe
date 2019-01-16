def getNextMonth(curMonth):
    curMonth = int(curMonth)
    if(curMonth>0 and curMonth<13):
        if(curMonth>=1 and curMonth < 12):
            nxtMonth = curMonth+1
        elif curMonth==12:
            nxtMonth=1
    return str(nxtMonth)

def getNextYear(curMonth, curYear):
    curMonth = int(curMonth)
    if(curMonth>0 and curMonth<13):
        if(curMonth>=1 and curMonth < 12):
            nxtYear = curYear
        elif curMonth==12:
            nxtYear+=1
    return str(nxtYear)

def fill_share(share):
    return share

def fill_total_share(previous_share, share):
    total_share = previous_share + share
    return total_share

def fill_installment(installment):
    # installment = 5000
    return installment

def fill_balance_loan(previous_loan, installment):
    balance_loan = previous_loan - installment
    return balance_loan

def fill_interest(interest_rate,previous_loan):
    interest = interest_rate * previous_loan
    return interest

def fill_total_amount(share, installment, interest):
    total_amount = share + installment + interest
    return total_amount
