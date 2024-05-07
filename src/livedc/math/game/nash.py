from specs.hardware import ensure_libs
import pandas as pd
from ...desc import add_rdoc


data = [
    {'A\B': '合作', '合作': (3, 2),  '对抗': (1, 4)},
    {'A\B': '对抗', '合作': (5, 0),  '对抗': (-5, -10)}
]





@ensure_libs(["sympy"])
def eqlib(df):
  """
  data = [
    {'A\B': '合作', '合作': (3, 2),  '对抗': (1, 4)},
    {'A\B': '对抗', '合作': (5, 0),  '对抗': (-5, -10)}
    ]

 Reference:
 * [为什么国家之间不能好好合作？](https://www.youtube.com/watch?v=pzh-3A2jJ8k)

  
  """
  A_AcBc,B_AcBc = df.iloc[0,0] ; A_AcBb,B_AcBb = df.iloc[0,1]
  A_AbBc,B_AbBc = df.iloc[1,0] ; A_AbBb,B_AbBb = df.iloc[1,1]
  import sympy as sym
  y = sym.Symbol("y")

  E_Ac = y * A_AcBc + (1-y) * A_AcBb
  E_Ab = y * A_AbBc + (1-y) * A_AbBb
  expr = E_Ac - E_Ab 
  # print (E_Ac)
  # print (E_Ab)
  # print (expr)
  val_y = sym.solve(expr,y)[0]
  print ("A 合作：%s"%val_y)
  v_Ea = E_Ac.subs({y:val_y}).evalf()
  print ("EA :%2.2f"%v_Ea)


  x = sym.Symbol("x")
  E_Bc = x * B_AcBc + (1-x) * B_AbBc
  E_Bb = x * B_AcBb + (1-x) * B_AbBb
  expr = E_Bc - E_Bb 
  # print (E_Bc)
  # print (E_Bb)
  # print (expr)
  val_x = sym.solve(expr,x)[0]
  print ("B 合作：%s"%val_x)
  v_Eb = E_Bc.subs({x:val_x}).evalf()
  print ("EB :%2.2f"%v_Eb)

  return val_y,v_Ea,val_x,v_Eb


if __name__ == "__main__":
    df = pd.DataFrame(data)
    df.set_index('A\B', inplace=True)
    print (df)
    val_y,v_Ea,val_x,v_Eb = eqlib(df)
