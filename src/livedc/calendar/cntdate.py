import datetime
from ..desc import add_rdoc

@add_rdoc
def flex_holiday(ymd=(2024,7,4),fiscal_delta = 1 ):
    """
    90-day flexing and fisical year rules applied
    """
    begin = datetime.datetime(*ymd) 
    ### take before
    ddl = begin + datetime.timedelta(days=90)
    
    if ddl < datetime.datetime(begin.year+fiscal_delta,6,30) :
        pass    
    else:
        ddl = datetime.datetime(begin.year+fiscal_delta,6,30)
    print (f"Take holiday before: {ddl.strftime('%Y-%m-%d')}" )
    return ddl

def time_passed(bgn_ymd=(2021,11,1) ,
                end=0):
    begin = datetime.datetime(*bgn_ymd) 
    if isinstance(end,tuple) :
        end =  datetime.datetime(*end) 
    elif end == 0:
        end =  datetime.datetime.today()

    delta = end - begin
    deltam =  (end.year - begin.year) * 12 + (end.month - begin.month)
    #  = delta/np.timedelta64(1, 'M')
    print ("%s days  passed:" %delta.days)
    print ("%s month passed:" %deltam)
    return delta,deltam

if __name__ == "__main__":
    ddl = flex_holiday()
    d,m = time_passed()

