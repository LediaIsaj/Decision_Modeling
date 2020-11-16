# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 01:06:53 2020

@author: Ledia
"""
import pandas as pd
import re

class UTA_Grenerator:
    
    
    def __init__(self,filepath):
        self.filepath = filepath
        filename = filepath.split(".")
        self.filename = filename[0]+".py"
        
        self.df = pd.read_excel(filepath,header=0)
        #Drop duplicate products
        self.df = self.df.drop_duplicates('productname').reset_index(drop=True)
    
    def string_sanitizer(self,string):
        #function to clean strings
        #keep letters from a-z and A-Z, numbers \d, non white spaces
        # other patters need to be substituded with an empty string
        return re.sub(r"[^a-zA-Z0-9]+", ' ', string)
    
    def double_sanitizer(self,string):
        return string.replace ('.', "_")
        
        
    
    def create_uta_file(self):
        f= open(self.filename,"w+")
        line1 = "# Auto-Grenerated python file \r\n"
        line2 = "from pulp import * \r\n"
        line2 += "import pandas as pd \r\n"
        line3 = "prob = LpProblem('NutriScore', LpMaximize) \r\n"
        
        lines_vars = "# Create problem variables \r\n"
        
        # Get problem variables
        count_prod = 1
        for product in self.df['productname']:
            
            lines_vars += "x_"+str(count_prod)+ " = LpVariable('"+self.string_sanitizer(product)+"',0,20) \r\n"
        
            count_prod +=1
        
        # Cretae the variables measuring the differences between classes
        lines_epsilon = '# Variables measuring differences between two consecutives classes \r\n'
        lines_epsilon += 'epsilon_1=LpVariable("epsilon_1",1, 20) \r\n'
        lines_epsilon += 'epsilon_2=LpVariable("epsilon_2",1, 20) \r\n'
        lines_epsilon += 'epsilon_3=LpVariable("epsilon_3",1, 20) \r\n'
        lines_epsilon += 'epsilon_4=LpVariable("epsilon_4",1, 20) \r\n'

 
        # Get marginal utility variables
        marginal_uility = "# Create variables associated to the marginal utility functions for each product \r\n"
        constraints = '# Constraints associated to global utility of each food \r\n'
        grade_A = list()
        grade_B = list()
        grade_C = list()
        grade_D = list()
        grade_E = list()
        
        #Get ordered products
        ordered_results = "results = {} \r\n"
        for index, row in self.df.iterrows():
            prodNumb = str(index+1)
            marginal_uility += " # Variables associated to the marginal utility functions of food 1 x_"+prodNumb+"\r\n"
            
            
            energy100g = self.double_sanitizer(str(row['energy100g']))      
            saturatedfat100g = self.double_sanitizer(str(row['saturatedfat100g']))
            sugars100g = self.double_sanitizer(str(row['sugars100g']))
            fiber100g = self.double_sanitizer(str(row['fiber100g']))
            proteins100g = self.double_sanitizer(str(row['proteins100g']))
            sodium100g = self.double_sanitizer(str(row['sodium100g']))
            
            marginal_uility += "U1_"+energy100g+"=LpVariable('U1_"+energy100g+"',0, 20) \r\n"
            marginal_uility += "U2_"+saturatedfat100g+"=LpVariable('U2_"+saturatedfat100g+"',0, 20) \r\n"
            marginal_uility += "U3_"+sugars100g+"=LpVariable('U3_"+sugars100g+"',0, 20) \r\n"
            marginal_uility += "U4_"+fiber100g+"=LpVariable('U4_"+fiber100g+"',0, 20) \r\n"
            marginal_uility += "U5_"+proteins100g+"=LpVariable('U5_"+proteins100g+"',0, 20) \r\n"
            marginal_uility += "U6_"+sodium100g+"=LpVariable('U6_"+sodium100g+"',0, 20) \r\n"
            
            constraints +="prob+=U1_"+energy100g
            constraints += " + U2_"+saturatedfat100g
            constraints += " + U3_"+sugars100g
            constraints += " + U4_"+fiber100g
            constraints += " + U5_"+proteins100g
            constraints += " + U6_"+sodium100g + " == x_"+prodNumb + " , 'product "+prodNumb+" constraint' \r\n" 
            
            ordered_results += "results["+prodNumb +"] = U1_"+energy100g +".varValue + U2_"+saturatedfat100g + ".varValue + U3_"+sugars100g +".varValue + U4_"+fiber100g +".varValue + U5_"+proteins100g + ".varValue + U6_"+sodium100g +".varValue \r\n"
            
            nutri_grade = row['nutriscoregrade']
            if (nutri_grade == 'a'):
                grade_A.append("x_"+prodNumb)
            else:
                if (nutri_grade == 'b'):
                    grade_B.append("x_"+prodNumb)
                else:
                    if (nutri_grade == 'c'):
                        grade_C.append("x_"+prodNumb)
                        
                    else:
                        if (nutri_grade == 'd'):
                            grade_D.append("x_"+prodNumb)
                        else:
                            if (nutri_grade == 'e'):
                                grade_E.append("x_"+prodNumb)
                                
              
                
        # Create the objective function
        line_obj = '# The objective function \r\n'
        line_obj += 'prob += epsilon_1+epsilon_2+epsilon_3+epsilon_4, "slack variables (differences between two consecutive classes) to be maximized" \r\n'
      
        #Setting the preferences
        lines_pref = "# Set the preferences \r\n"
        
        lines_pref += "# Food of class A are better than food of class B \r\n"
        for b in grade_B:
            for a in grade_A:
                lines_pref += "prob += "+b+" + epsilon_1 <="+a+" , ' "+b+" after "+ a +"' \r\n"
        
        lines_pref += "# Food of class B are better than food of class C \r\n"
        for c in grade_C:
            for b in grade_C:
                lines_pref += "prob += "+c+" + epsilon_2 <="+b+" , ' "+c+" after "+ b +"' \r\n"

        lines_pref += "# Food of class C are better than food of class D \r\n"
        for d in grade_D:
            for c in grade_D:
                lines_pref += "prob += "+d+" + epsilon_3 <="+c+" , ' "+d+" after "+ c +"' \r\n"

        lines_pref += "# Food of class D are better than food of class E \r\n"
        for e in grade_E:
            for d in grade_E:
                lines_pref += "prob += "+e+" + epsilon_4 <="+d+" , ' "+e+" after "+ d +"' \r\n"

        #Creating the monotonicity constraints
        
        monotonicity1 = "# Monotonicity constraints associated to the values of criterion 1 \r\n"
        const1 = self.df['energy100g']
        ordered1 = const1.sort_values(ascending=False,ignore_index=True)
        
        monotonicity2 = "# Monotonicity constraints associated to the values of criterion 2 \r\n"
        const2 = self.df['saturatedfat100g']
        ordered2 = const2.sort_values(ascending=False,ignore_index=True)
        
        monotonicity3 = "# Monotonicity constraints associated to the values of criterion 3 \r\n"
        const3 = self.df['sugars100g']
        ordered3 = const3.sort_values(ascending=False,ignore_index=True)
        
        monotonicity4 = "# Monotonicity constraints associated to the values of criterion 4 \r\n"
        const4 = self.df['fiber100g']
        ordered4 = const4.sort_values(ascending=False,ignore_index=True)
        
        monotonicity5 = "# Monotonicity constraints associated to the values of criterion 5 \r\n"
        const5 = self.df['proteins100g']
        ordered5 = const5.sort_values(ascending=False,ignore_index=True)
        
        monotonicity6 = "# Monotonicity constraints associated to the values of criterion 6 \r\n"
        const6 = self.df['sodium100g']
        ordered6 = const6.sort_values(ascending=False,ignore_index=True)
        
        
        for i in range (0,len(ordered1)-1):
            monotonicity1 += "prob += U1_"+self.double_sanitizer(str(ordered1[i]))+"  <= U1_"+self.double_sanitizer(str(ordered1[i+1]))+" \r\n"
            monotonicity2 += "prob += U2_"+self.double_sanitizer(str(ordered2[i]))+"  <= U2_"+self.double_sanitizer(str(ordered2[i+1]))+" \r\n"
            monotonicity3 += "prob += U3_"+self.double_sanitizer(str(ordered3[i]))+"  <= U3_"+self.double_sanitizer(str(ordered3[i+1]))+" \r\n"
            monotonicity4 += "prob += U4_"+self.double_sanitizer(str(ordered4[i]))+"  <= U4_"+self.double_sanitizer(str(ordered4[i+1]))+" \r\n"
            monotonicity5 += "prob += U5_"+self.double_sanitizer(str(ordered5[i]))+"  <= U5_"+self.double_sanitizer(str(ordered5[i+1]))+" \r\n"
            monotonicity6 += "prob += U6_"+self.double_sanitizer(str(ordered6[i]))+"  <= U6_"+self.double_sanitizer(str(ordered6[i+1]))+" \r\n"
        
        probl = "# The problem data is written to an .lp file \r\n"
        probl += "prob.writeLP('The Nutriscore.lp') \r\n"
        probl += "prob.solve() \r\n"
        probl += "print('Status:', LpStatus[prob.status]) \r\n"
        probl += "# Each of the variables is printed with it's resolved optimum value \r\n"
        probl += "for v in prob.variables(): \r\n"
        probl += "\t print(v.name, '=', v.varValue) \r\n"
        probl += "print('Value of objective function = ', value(prob.objective)) \r\n"

        mon_consts = monotonicity1 + monotonicity2 + monotonicity3 + monotonicity4 + monotonicity5 + monotonicity6
        ordered_results += "df = pd.read_excel('"+self.filepath+"',header=0) \r\n"
        ordered_results += "df = df.drop_duplicates('productname').reset_index(drop=True) \r\n"
        ordered_results += "df_results = pd.DataFrame(columns=('Food', 'Score', 'Nutri-Score')) \r\n"
        ordered_results += "ordered_results = sorted(results.items(),key = lambda x:x[1],reverse = True) \r\n"
        ordered_results += "for i in ordered_results: \r\n"
        ordered_results += "\t index = i[0]-1 \r\n"
        ordered_results += "\t df_results.loc[index] = [df.loc[index]['productname'], i[1], df.loc[index]['nutriscoregrade']] \r\n"      
        ordered_results += "print(df_results) \r\n"
        ordered_results += "df_results.to_csv('results.csv') \r\n"
        
        #Write all the specified lines of code into the file
        f.writelines([line1, line2, line3,lines_vars,lines_epsilon, marginal_uility,line_obj, constraints, lines_pref,mon_consts,probl, ordered_results])
file = "OpenFood_Petales.xlsx"
test1 = UTA_Grenerator(file)
test1.create_uta_file()