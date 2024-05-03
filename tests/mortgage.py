from livedc.math.financial.compound import (pd,
                                            compound_interest,
                                            mortgage_interest)

if __name__ == "__main__":
  # print (approx_Euler(10))
  # plot_Euler()
  rv = 0.15 
  print ("年利率：%s%%"%(rv*100))
  print ("月复利",  compound_interest(r=rv, n=12))
  print ("日复利",   compound_interest(r=rv,n=365))
  print ("高利贷：连续复利",  compound_interest(r=0.5,n=365))

  ### morgate rate
  rv,t = 0.05625,30
  rv,t = 0.05250,15
  pv = 500000
  mortgage_interest(P=pv,r=rv,ny=t)
  


  ###
  x = [ i*0.01 for i in range(1,100) ]
  df = pd.DataFrame(data={"x":x})
  # df["y"] = df.x.apply(lambda x: compound_interest(r=x,n=365))
  # df["y"] = df.x.apply(lambda x: compound_interest(r=x,n=12))
  df["y"] = df.x.apply(lambda x: compound_interest(r=x,n=2))
  df.plot(x="x",y="y",kind="line")

  # https://educationdata.org/average-student-loan-interest-rate
  rv = 0.035
  pv = 33000 * 2.5
  t = 15

  print ( "本金: %s \n 利息（月）：%s" %(pv,compound_interest( r=rv,P=pv, n=12,t=t)-pv))
  print ("年利率：%.4s%% 按 %s 年还清"%(rv*100,t))
  print ("月复利",  compound_interest( r=rv,P=pv, n=12,t=t))
  print ("日复利",   compound_interest(r=rv,P=pv, n=365,t=t))

  print ("月复利_月还款",  compound_interest( r=rv,P=pv, n=12,t=t)/t/12)
  print ("日复利_月还款",   compound_interest(r=rv,P=pv, n=365,t=t)/t/12)
  # print ("高利贷：连续复利",  compound_interest(r=0.5,n=365))


  # https://www.bankofamerica.com/mortgage/
  # Rates based on a $800,000 loan in ZIP code 01255
  rv = 0.067
  pv = 800000 
  t,tv = 30,13

  print ( "本金: %s \n 利息：%s" %(pv,compound_interest( r=rv,P=pv, n=1,t=tv)-pv))
  print ("年利率：%.4s%% 按 %s 年还清"%(rv*100,t))
  print ("年复利",  compound_interest( r=rv,P=pv, n=1,t=tv))
  print ("月复利",  compound_interest( r=rv,P=pv, n=12,t=tv))
  print ("日复利",   compound_interest(r=rv,P=pv, n=365,t=tv))

  print ("年复利_月还款",  compound_interest( r=rv,P=pv, n=1,t=tv)/t/12)
  print ("月复利_月还款",  compound_interest( r=rv,P=pv, n=12,t=tv)/t/12)
  print ("日复利_月还款",  compound_interest( r=rv,P=pv, n=365,t=tv)/t/12)