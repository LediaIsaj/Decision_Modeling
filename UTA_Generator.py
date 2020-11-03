# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 01:06:53 2020

@author: Ledia
"""
import pandas as pd
class UTA_Grenerator:
    
    
    def __init__(self,filepath):
        
        filename = file.split(".")
        self.filename = filename[0]+".py"
        
        self.df = pd.read_excel(filepath,header=0)
        
    
    def create_uta_file(self):
        f= open(self.filename,"w+")
        line1 = "# Auto-Grenerated python file \r\n"
        line2 = "from pulp import * \r\n"
        line3 = "prob = LpProblem('UTA', LpMinimize) \r\n"
        
        lines_vars = "# Create problem variables \r\n"
        
        # Get problem variables
        count_prod = 1
        for product in self.df['productname']:
            
            lines_vars += "x_"+str(count_prod)+ " = LpVariable('"+product+"',0,None) \r\n"
        
            count_prod +=1
        
        
        
        # Get marginal utility variables
        marginal_uility = "# Create variables associated to the marginal utility functions for each product \r\n"
                
        for index, row in self.df.iterrows():
            prodNumb = str(index+1)
            marginal_uility += " # Variables associated to the marginal utility functions of food 1 x_"+prodNumb+"\r\n"
            
            energy100g = row['energy100g']
            saturatedfat100g = row['saturatedfat100g']
            sugars100g = row['sugars100g']
            fiber100g = row['fiber100g']
            proteins100g = row['proteins100g']
            sodium100g = row['sodium100g']
            
            marginal_uility += "U"+prodNumb+"_"+str(energy100g)+"=LpVariable('utilite_"+prodNumb+"_energy100g',0, None) \r\n"
            marginal_uility += "U"+prodNumb+"_"+str(saturatedfat100g)+"=LpVariable('utilite_"+prodNumb+"_saturatedfat100g',0, None) \r\n"
            marginal_uility += "U"+prodNumb+"_"+str(sugars100g)+"=LpVariable('utilite_"+prodNumb+"_sugars100g',0, None) \r\n"
            marginal_uility += "U"+prodNumb+"_"+str(fiber100g)+"=LpVariable('utilite_"+prodNumb+"_fiber100g',0, None) \r\n"
            marginal_uility += "U"+prodNumb+"_"+str(proteins100g)+"=LpVariable('utilite_"+prodNumb+"_proteins100g',0, None) \r\n"
            marginal_uility += "U"+prodNumb+"_"+str(sodium100g)+"=LpVariable('utilite_"+prodNumb+"_sodium100g',0, None) \r\n"
            
        f.writelines([line1, line2, line3,lines_vars,marginal_uility])
file = "OpenFood_Petales.xlsx"
test1 = UTA_Grenerator(file)
test1.create_uta_file()