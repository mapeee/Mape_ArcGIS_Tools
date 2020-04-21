# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 16:25:31 2020

@author: marcu
"""

from pyproj import Transformer
import pandas as pd


def project_xy(in_x, in_y, transformer):
    X = str(in_x)
    X = X.replace(".","")
    X = X+"00000"
    X = int(X[:7])
    Y = str(in_y)
    Y = Y.replace(".","")
    Y = Y+"00000"
    Y = int(Y[:7])
    x_out, y_out = transformer.transform(X, Y)
    return x_out, y_out


def project_table(indata, in_id, in_x, in_y, in_proj, out_proj, **optional):
    transformer = Transformer.from_crs(in_proj, out_proj, always_xy=True)
    try: all_f = optional["all_f"]
    except KeyError: all_f = False
    proj_list = []

    for index, row in indata.iterrows():
        x_out, y_out = project_xy(row[in_x],row[in_y],transformer)
        values = []

        if all_f == True:
            for i in indata.columns:
                values.append(row[i])
            values.extend([x_out, y_out])               
            proj_list.append(values)
            col = list(indata.columns)
            col.extend([in_x+"_proj", in_y+"_proj"])
        else:
            values.extend([row[in_id],row[in_x],row[in_y],x_out, y_out])            
            proj_list.append(values)
            col = [in_id, in_x, in_y, in_x+"_proj", in_y+"_proj"]
    proj_list = pd.DataFrame(proj_list, columns =col)           
    return proj_list