import pandas as pd
import numpy as np
from specs.hardware import ensure_libs
# tdm23.0.1\tdm23\code\model\tdmpy\wkfhm.py
# pyomo==6.2
# require a different python version: 6.2 Requires-Python >=3.6, <3.10
import logging
import os



class BalanceOR:
    @ensure_libs(["pyomo==6.7.1","cplex"])
    def __init__(self) -> None:
        self.data = {None: {'I': {None: [1, 2, 3, 4, 5, 6]},
                        'J': {None: [1, 2, 3, 4, 5, 6]},
                        'TR': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0},
                        'TC': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0},
                        'AT': {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0},
                        'rho': {1: 0.2, 2: 0.3, 3: 0.6, 4: 0.6, 5: 0.7, 6: 0.7},
                        'tau': {1: 1759937, 2: 1488121, 3: 907115, 4: 227444, 5: 112550, 6: 219481},
                        'ttr': {None: 0},
                        'gama': {(1, 1): 6499.8,
                                 (1, 2): 6407.4,
                                 (1, 3): 4945.2,
                                 (1, 4): 1431.0,
                                 (1, 5): 714.6,
                                 (1, 6): 1765.8,
                                 (2, 1): 103813.2,
                                 (2, 2): 86193.0,
                                 (2, 3): 51919.2,
                                 (2, 4): 12454.8,
                                 (2, 5): 6301.8,
                                 (2, 6): 14059.199999999999,
                                 (3, 1): 217023.6,
                                 (3, 2): 154393.8,
                                 (3, 3): 85684.8,
                                 (3, 4): 20428.2,
                                 (3, 5): 9643.199999999999,
                                 (3, 6): 19753.8,
                                 (4, 1): 117310.2,
                                 (4, 2): 93483.59999999999,
                                 (4, 3): 54950.4,
                                 (4, 4): 13647.6,
                                 (4, 5): 6755.4,
                                 (4, 6): 14549.4,
                                 (5, 1): 235798.19999999998,
                                 (5, 2): 202938.0,
                                 (5, 3): 130617.0,
                                 (5, 4): 34707.0,
                                 (5, 5): 17016.6,
                                 (5, 6): 33037.2,
                                 (6, 1): 375517.2,
                                 (6, 2): 349456.8,
                                 (6, 3): 216152.4,
                                 (6, 4): 53797.799999999996,
                                 (6, 5): 27098.399999999998,
                                 (6, 6): 48523.2}}}

        # Model coeff
        self.deltafct_R = 0.01
        self.deltafct_C = 0.01
        self.wcol     = 1
        self.wrow     = 1
        self.prop_row  = 0.1
        self.Tlimit = 5

        self.log_level = "DEBUG"
        self.logfile = self.init_logger()
        self.logger = self.add_logger()


    def init_logger(self):
        LOG_FILE = "bal.log"
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        else:
            pass
        return LOG_FILE

        

    def add_logger(self,name = "__name__"):
        LOG_FILE = self.logfile
        logger = logging.getLogger(name)
        FORMATTER = logging.Formatter("%(asctime)s * %(levelname)8s * %(module)15s * %(funcName)20s * %(message)s")
        file_handler = logging.FileHandler(LOG_FILE,mode='a')
        file_handler.setFormatter(FORMATTER)
        logger.addHandler(file_handler)
        logger.setLevel(self.log_level)
        return logger
    
    def createModel(self):
        from pyomo.environ import (AbstractModel,
                                   Set,
                                   Param,
                                   Var,
                                   Constraint,
                                   Objective,
                                   minimize
                                   )
        import pyomo.kernel as pmo
        

        model = AbstractModel()
        # index
        # Define sets
        model.I  = Set()     # Set of income level 
        model.J  = Set()     # Set of area type 
        # # Parameters 
        # Data_deterministic
        model.ttr = Param() 
        model.TC  = Param(model.J) ## sort in asending order
        model.TR  = Param(model.I)  
        model.AT  = Param(model.J)
        model.rho = Param(model.J)
        model.tau = Param(model.J)
        model.gama = Param(model.I,model.J)

        # # Decision Variables
        model.x = Var(model.I, model.J,bounds=(0, 10**6),name='people')  
        model.abs_row = Var()  
        model.abs_col = Var()   
        model.Sum_cost =Var()
        model.Ave_cost =Var()

        # Constraints
        def Cap(model,j):
            return sum(model.x[i,j] for i in model.I)  <= model.tau[j] * model.rho[j]
        model.Cap = Constraint(model.J, rule=Cap)

        def Cap_cell(model,i,j):
            return model.x[i,j]  <= model.gama[i,j]
        model.Cap_cell = Constraint(model.I,model.J, rule=Cap_cell)

        def Prop_lower(model,i,j):
            """ pair with Prop_upper,
                make sure values across each row fits a row proportion AT

            Args:
                model (_type_): _description_
                i (int): area type index
                j (int): column index

            Returns:
                _type_: _description_
            """
            return model.x[i,j] >= model.x[1,j] * model.AT[i] * (1 - self.prop_row)
        model.Prop_lower = Constraint(model.I, model.J, rule=Prop_lower)

        def Prop_upper(model,i,j):
            return model.x[i,j] <= model.x[1,j] * model.AT[i] * (1 + self.prop_row)
        model.Prop_upper = Constraint(model.I, model.J, rule=Prop_upper)

        def Col_Sum(model,j):
            return sum(model.x[i,j] for i in model.I) - model.TC[j]  >= model.TC[j] * self.deltafct_C * -1                                                 
        model.sumc = Constraint(model.J, rule=Col_Sum)    

        def Col_Sum_max(model,j):
            return sum(model.x[i,j] for i in model.I) - model.TC[j]  <= model.TC[j] * self.deltafct_C
        model.sumcm = Constraint(model.J, rule=Col_Sum_max)    

        def Row_Sum_min(model,i):
            return sum(model.x[i,j] for j in model.J) - model.TR[i]  >= model.TR[i] * self.deltafct_R * -1                                                       
        model.sumr = Constraint(model.I,rule=Row_Sum_min)    

        def Row_Sum_max(model,i):
            return sum(model.x[i,j] for j in model.J) - model.TR[i]  <=  model.TR[i]* self.deltafct_R                                            
        model.sumrm = Constraint(model.I,rule=Row_Sum_max)    

        def Sum_cost(model):
            return model.Sum_cost ==  self.wcol * sum(sum(model.x[i,j] for i in model.I) - model.TC[j] for j in model.J) + self.wrow * sum(sum(model.x[i,j] for j in model.J) - model.TR[i] for i in model.I)                                                  
        model.OBj_1 = Constraint(rule=Sum_cost)   

        def abs_col1(model):
            return model.abs_col >=  sum(sum(model.x[i,j] for i in model.I) - model.TC[j] for j in model.J) 
        model.abs_col1 = Constraint(rule=abs_col1)

        def abs_col2(model):
            return model.abs_col >= -1 * sum(sum(model.x[i,j] for i in model.I) - model.TC[j] for j in model.J) 
        model.abs_col2 = Constraint(rule=abs_col2)

        def abs_row1(model):
            return  model.abs_row >=  sum(sum(model.x[i,j] for j in model.J) - model.TR[i] for i in model.I)
        model.abs_row1 = Constraint(rule=abs_row1) 

        def abs_row2(model):
            return  model.abs_row >= -1 *sum(sum(model.x[i,j] for j in model.J) - model.TR[i] for i in model.I)
        model.abs_row2 = Constraint(rule=abs_row2) 

        def Nonneg(model):
            return model.Sum_cost >= 0
        # model.Nonneg = Constraint(rule=Nonneg) 
        
        # Objective
        def total_cost(model):
            # return (model.abs_row + model.abs_col )
            # return (model.ttr - sum(sum(model.x[i,j] for i in model.I) for j in model.J))
            return (self.wrow* model.abs_row + self.wcol *model.abs_col )

        model.total_cost_Objective = Objective(rule=total_cost, sense=minimize)

        self.FB_model = model.create_instance(self.data)
    
    def solve(self,wfh_summ="wfh_summary.csv",logger="logger"):
        """    Solve and print
        """
        from pyomo.opt import (SolverFactory,
                               SolverStatus, 
                               TerminationCondition
                              )
        opt = SolverFactory('cplex',solver_io="python",validate=False,tee =False)

        # logger.debug(self.FB_model.pprint() )
        results = opt.solve(self.FB_model, timelimit = self.Tlimit)

        if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
            # Do something when the solution in optimal and feasible
            print ("min value obj: %s \n" %self.FB_model.total_cost_Objective())

            recods = []
            for i in list(range(1,len(self.FB_model.I)+1)):
                row_tup = []
                for j in list(range(1,len(self.FB_model.J)+1)):
                    value =int(self.FB_model.x[i,j].value)
                    # value = int(value(FB_model.x[i,j,k]))
                    row_tup.append(value)
                    # print("%s[%s,%s] = %s" % (self.FB_model.x.name, i,j,value))
                recods.append(row_tup)
            dffit = pd.DataFrame.from_records(recods)
            col_sfit = dffit.sum("index").to_numpy() #income
            row_sfit = dffit.sum(1).to_numpy()      #area
            col_diff = col_sfit - np.array(list(self.data[None]["TC"].values()))
            row_diff = row_sfit - np.array(list(self.data[None]["TR"].values()))
            diff_rtc = col_diff/np.array(list(self.data[None]["TC"].values()))
            diff_rtr = row_diff/np.array(list(self.data[None]["TR"].values()))

            with open(wfh_summ,"a",newline='') as f:
                logger.debug("min value: %s \n" %self.FB_model.Sum_cost.value)
                # f.write(dffit.to_csv())
                # summarywriter = csv.writer(f, delimiter=',',
                #                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
                logger.debug([])
                logger.debug( ["Income_lvl"]    + list(self.data[None]["TC"].keys()) )
                logger.debug( ["Targetsum"]     + list(self.data[None]["TC"].values()) )
                logger.debug( ["Balancesum"]    + list(col_sfit) )
                logger.debug( ["column_diff"]   + list(col_diff) )
                logger.debug( ["diff_ratio"]    + list(diff_rtc) )
                logger.debug( ["col_diff_sum"]  + [col_diff.sum()] )
                logger.debug([])
                logger.debug( ["Area_type"]    + list(self.data[None]["TR"].keys()) )
                logger.debug( ["Targetsum"]    + list(self.data[None]["TR"].values()) )
                logger.debug( ["Balancesum"]   + list(row_sfit) )
                logger.debug( ["row_diff"]     + list(row_diff) )
                logger.debug( ["diff_ratio"]    + list(diff_rtr) )
                logger.debug( ["row_diff_sum"] + [row_diff.sum()] )
                logger.debug([])
                logger.debug(["Overall difference:", abs(col_diff.sum()) + abs(row_diff.sum()) ])

            return 0, dffit

        elif (results.solver.termination_condition == TerminationCondition.maxTimeLimit):
            # Do something when model in timelimit
            print (value(self.FB_model.total_cost_Objective))
            return 1,None
        elif (results.solver.termination_condition == TerminationCondition.infeasible):
            print ("infeasible boudrary, relax the constraint" )
            return 2,None
        else:
            # Something else is wrong
            print ("Error Solver Status: " , results.solver.status)
            print ("Error Solver Status: " , results.solver.termination_condition )
            return 3,None



if __name__ == "__main__":


    bal = BalanceOR()
    bal.createModel()
    bal.solve(logger=bal.logger)
