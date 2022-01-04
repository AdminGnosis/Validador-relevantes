import pandas as pd
import numpy as np
import os
from timeit import default_timer
from datetime import datetime
from Funciones_relevantes import *
from act_eco import *


def relevantes(file_path):
    inicio = default_timer()
    del err[:]
    df = pd.read_csv(file_path, encoding="ISO-8859-2", sep=";", header=None, dtype=str)
    
    col1(df)
    col2(df)
    col3(df)
    col4(df)
    col5(df)
    col6(df)
    col7(df)
    col8(df)
    col9(df)
    col10(df)
    col11(df)
    col12(df)
    col13(df)
    col14(df)
    col15(df)
    col16(df)
    col17(df)
    col18(df)
    col19(df)
    col20(df)
    col21(df)
    col22(df)
    col23(df)
    col24(df)
    col25(df)
    col26(df)
    col27(df)
    col28(df, dic_act)
    col29(df)
    col30(df)
    col31(df)
    col32(df)
    col33(df)
    col34(df)
    col35(df)
    col36(df)
    col37(df)
    col38(df)
    col39(df)
    col40(df)
    col41(df)
    fin = default_timer()
    
    err2 = []
    for i in err:
        err2.append(i.split(','))
        
    df_errores = pd.DataFrame(err2, columns = ["tipo_de_error", "columna", "nombre", "Numero del registro", "Contenido del registro", "leyenda"])
    
    now = datetime.today().strftime('%Y-%m-%d %H:%M')
    bitacora = []
    #############################
    # Para bitacora
    #############################
    bitacora.append('Ubicación del archivo: '+os.path.abspath(file_path))
    nombre_del_archivo = os.path.abspath(file_path)
    nombre_del_archivo = 'Nombre del archivo: '+nombre_del_archivo.split("/")[-1]
    bitacora.append(nombre_del_archivo)
    bitacora.append('Fecha y hora de validacion:'+' '+now)
    bitacora.append('Numero de registros: '+str(len(df)))
    bitacora.append('Numero total de errores encontrados: '+str(len(err)))
    bitacora.append('Tiempo total de validacion del archivo: '+str(str((fin-inicio)/60)[:5])+' minutos')
    
    bitacora = pd.DataFrame(bitacora)

    
    return [df_errores,bitacora]


