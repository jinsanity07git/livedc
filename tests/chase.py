# https://www.chase.com/personal/credit-cards/education/interest-apr/when-does-interest-start-to-accrue-on-credit-card
# https://creditcards.chase.com/a1/freedom/CFDBAU623?CELL=6D4F&jp_cmp=cc/Freedom+Flex_Brand_Exact_Freedom+Flex_SEM_US_NA_Standard_+Test+(2.23.23)/sea/p75295460413/Freedom+Flex&gclsrc=aw.ds&&gclid=CjwKCAjwq4imBhBQEiwA9Nx1BpTIGh_3O3jhyKtbnGoRizFdPpLk1qwnaqvqyOcoiF6x3B4-OtGNixoCtK8QAvD_BwE&gclsrc=aw.ds
from livedc.math.financial.compound import compound_interest

# a variable APR of 20.24% - 28.99%

APR = 20.24/100
qishu = 365
balence = 1000
p1 = compound_interest(r=APR, P=balence, n=qishu,t=20/qishu) - balence

balence = 2100
p2 = compound_interest(r=APR, P=balence, n=qishu,t=10/qishu) - balence

print (f"{p1:.2f} + {p2:.2f} = {p1+p2:.2f}")