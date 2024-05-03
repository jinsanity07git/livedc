# 纯策略下的纳什均衡

# 混合策略纳什均衡
# - 确定概率
"""
https://www.bilibili.com/video/BV1Ks41157Aj/?spm_id_from=333.337.search-card.all.click
人生中最重要的概念：复利，是什么？想贷款和分期就必须要了解它

https://qwtel.com/posts/finance/continuously-compounding-interest/
"""

import pandas as pd
from ...desc import add_rdoc
### 自然对是的底 -- e


def approx_Euler(n):
  x = (1+1/n)**n
  return x

def plot_Euler():
  x = [ i for i in range(1,10*10000) ]
  df = pd.DataFrame(data={"x":x})
  df["y"] = df.x.apply(approx_Euler)
  print (df.y.iloc[-1])
  df.plot(x="x",y="y",kind="line")


@add_rdoc
def compound_interest(r=0.1, P=100,n=12,t=1):
  """

   $$ A = P(1 + \frac{r}{n})^{nt} $$
  
  Calculate the compound interest.
  - A	=	final amount || 终值
  - P	=	initial principal balance || 现值
  - r	=	interest rate || （年化）利率
  - n	=	number of times interest applied per time period || 期数
  - t	=	number of time periods elapsed || （年数)
  

  Returns:
    The final amount after applying compound interest.
  
  Ref
  - [Compound Interest Calculator](https://www.calculatorsoup.com/calculators/financial/compound-interest-calculator.php)
  """
  A = P*(1+ r/n)**(n*t)
  # print (A)
  ## when n --> +inf
  ## A = e**r

  return A

def mortgage_interest( P=100,r=0.063,ny=1):
  """
  https://www.businessinsider.com/personal-finance/mortgage-calculator
  
  M = P [ i(1 + i)^n ] / [ (1 + i)^n – 1]
   - "P" is your principal
   - "i" is your monthly interest rate
   - "n" the number of months required to repay the loan
  """
  i,n = r/12, ny*12
  ### A = (P=P,r=i,t=n, n=1) ## monthly rate
  A = compound_interest(P=P,r=r,n=12,t=ny) ## monthly rate
  # A = P*(1+i)**n
  M = A * i / ((1+i)**n -1)
  
  print ( "本金: %s \n 利息：%s" %(P,round(M*n-P,1) )  )
  print ( "实际利率: %s %% "%(round((M*n-P)/P*100 ,1) )  )
  ifr = inflation_factor(t=30)
  print ( "届时再买需（只考虑通胀）: %s " %(round(P/ifr,1) )  )
  print ( "跑赢通胀 by 30y: %s " %(round(P/ifr - M*n,1) )  )
  print ("月复利_月还款:%.1f \n 月利息：%.1f"%(M, (M*n-P)/n) )
  # print (i / ((1+i)**n -1))
  return M

def inflation_factor(t=15):
  """
  t : years
  """
  ifln = 3.8 /100
  depreciation_rate =   1 / (1+ifln)**t
  print ( "通膨贬值率: %s %% "%(round(depreciation_rate*100 ,1) )  )
  return depreciation_rate

if __name__ == "__main__":
  # print (approx_Euler(10))
  # plot_Euler()
  pass
