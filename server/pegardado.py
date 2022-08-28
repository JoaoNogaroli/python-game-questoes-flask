import csv
from dataclasses import replace
from importlib.resources import path
import os
from tkinter.tix import COLUMN
import pandas as pd
def pegardado2():
    cwd = os.getcwd()         
    path_ = os.path.join(cwd,'server','lista_csv.csv')
    # with open(path_,encoding='utf-8') as f:
    #     reader = csv.reader(f)
    #     lista = list(reader)
    # return lista
    dicio = pd.read_csv(path_)
    dicio = dicio.rename(columns={'Unnamed: 0':'cod_questao'})
    return dicio
