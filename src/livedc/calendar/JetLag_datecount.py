# https://www.dealmoon.com/cn/daily-update-back-to-china-fight-tickets-sorting/2249920.html
# https://www.skyscanner.com/transport/flights/bos/csha/230930/231204/config/10081-2309301243--32571-2-15641-2310020035%7C15641-2312040150--32571-2-10081-2312041225?adultsv2=1&cabinclass=economy&childrenv2=&inboundaltsenabled=false&outboundaltsenabled=false&preferdirects=false&rtn=1

import datetime

td = datetime.datetime.today()
end   = td
jetlag  = 13 #hours
ia_time = 18 #hours
begin_us = datetime.datetime(2023,9,26)
begin_cn = begin_us + datetime.timedelta(hours= jetlag+ia_time)
enddy_cn = begin_cn + datetime.timedelta(days= 62)
enddy_tight = enddy_cn
enddy_cn = datetime.datetime(2023,12,7)
enddy_us = enddy_cn + datetime.timedelta(hours= -jetlag+ia_time)

print (f"departure from Boston   {begin_us}")
print (f"arrival to  Shanghai   {begin_cn}")

print (f"departure from Shanghai {enddy_cn}")
print (f"earliest departure  {enddy_tight}")

# begin = datetime.datetime(2014,8,17) 
# end = datetime.datetime(2015,1,7) 
begin = datetime.datetime(2016,8,20) 
end = datetime.datetime(2017,5,22) 

# begin = datetime.datetime(2023,4,17) 
delta_cn =   enddy_cn - begin_cn
delta_us =   enddy_us - begin_us

print (f"home country presence: {delta_cn} " )
print (f"US calendar  day: {delta_us} " )
