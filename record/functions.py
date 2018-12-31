def getNextMonth(curMonth):
    curMonth = int(curMonth)
    if(curMonth>0 and curMonth<13):
        if(curMonth>=1 and curMonth < 12):
            nxtMonth = curMonth+1
        elif curMonth==12:
            nxtMonth=1
    return str(nxtMonth)
