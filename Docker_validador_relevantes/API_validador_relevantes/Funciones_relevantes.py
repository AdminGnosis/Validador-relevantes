#==================Gonzalez Ariza Alexis++++++++==============
#===================Validador RELEVANTES======================
##############################################################
import pandas as pd
import re
import xlrd

######################################################
##############################################################
def open_txt(path):
    with open(path, 'r') as file:
        text = file.read()

    text = text.split(";")
    # eliminamos el último por ser vacío
    ytext = text[:-1]
    return text
def cat2list(datafile, col, sheet_index = 0):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(sheet_index)
    lst = []
    for i in range(1,sheet.nrows):
        c_val = sheet.cell_value(i,col)
        if c_val == '':
            c_val = -1
        lst.append(int(c_val))
    return lst
######################################################
err = []
cat_casfim = open_txt('/ara/API_validador_relevantes/Catalogos/casfim_claves.txt')
cat_loc = list(pd.read_csv('/ara/API_validador_relevantes/Catalogos/Localidades.csv', encoding="ISO-8859-2", sep=";", header=None, dtype=str)[0])
cat_suc = open_txt("/ara/API_validador_relevantes/Catalogos/donde_suc.txt")
pais = pd.read_csv('/ara/API_validador_relevantes/Catalogos/Paises.txt', encoding="ISO-8859-1", sep=";", header=None, dtype=str)
cat_nac = list(pais[1])
cat_mon = open_txt('/ara/API_validador_relevantes/Catalogos/cat_mon')

#======================Columna 1=================================
#======================TIPO DE REPORTE===========================

def col1(df):
    for i in range(len(df[0])):
        if df[0][i] == None or type(df[0][i]) == float:
            err.append('vacio, Columna 1, Tipo_de_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[0][i]) + ', El registro se encuentra vacio o tiene punto y coma y es obligatorio')
        else:
            if len(df[0][i]) > 1:
                err.append('longitud, Columna 1, Tipo_de_reporte, Numero de registro: ' + str(i+1) +  ', Contenido de registro: ' + str(df[0][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
        
            if df[0][i] != '1':
                err.append('catalogo, Columna 1, Tipo_de_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[0][i]) + ', La informacion de la columna no se encuentra deacuerdo con el catalogo')

#======================Columna 2 INUSUALES======================
#======================Periodo del reporte======================

def col2(df):
    for i in range(len(df[1])):
        if df[1][i] == None or type(df[1][i]) == float:
            err.append('vacio, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', El registro se encuentra vacio o tiene punto y coma y es obligatorio')
        else:
            if len(df[1][i]) != 6:
                err.append('longitud, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', La cadena de números es mayor o menor a una longitud de 6 y La longitud del campo excede lo dispuesto en el DOF')
            
            if len(df[1][i]) != 6 or df[1][i].isdigit() == False :
                err.append('fecha, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', La secuencia numerica no cumple con el formato AAAAMM')
            
            if df[1][i].isdigit() == False :
                err.append('alfabetico, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', Hay información alfabética en el campo')
            
            else:    
                if len(df[1][i]) == 6:
                    if int(df[1][i][0:4]) < 2014:
                        err.append('fecha, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', Los números de año son inferiores a 2014')
                        
                    if int(df[1][i][4:6]) > 12:
                        err.append('fecha, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', Los números de mes son distintos a los números 1 al 12')
                    if int(df[1][i][0:4]) < 2014 or int(df[1][i][4:6]) > 12:
                        err.append('fecha, Columna 2, periodo_del_reporte, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[1][i]) + ', La secuencia numerica no cumple con el formato AAAAMM')

#======================Columna 3=================================
#======================FOLIO ====================================

def col3(df):
    
    if df[2][0] != '000001' or  type(df[2][0]) == float:
            err.append('numerico, Columna 3, folio, Numero de registro: ' + str(1) + ', Contenido de registro: ' + str(df[2][0]) + ', El primer registro no contiene en la columna 3 000001')
    
    for i in range(len(df[2])):
        if df[2][i] == None or type(df[2][i]) == float:
            err.append('vacio, Columna 3, folio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[2][i]) + ', El registro se encuentra vacio o tiene punto y coma y es obligatorio')
            
        else:
            if len(df[2][i]) != 6:
                err.append('longitud, Columna 3, folio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[2][i]) + ', La longitud del campo no es de 6 caracteres/la longitud del campo debe de ser de 6 caracteres númericos')
            
            if df[2][i].isdigit() == False:
                    err.append('incremento, Columna 3, folio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[2][i]) + ', El campo no continua el incremento de la serie numerica del folio')
            else:
                try:
                    if df[2][i].isdigit() == True:
                        if int(df[2][i+1]) == int(df[2][i]):
                            True
                        else:
                            if int(df[2][i+1]) != int(df[2][i]) + 1:
                                err.append('incremento, Columna 3, folio, Numero de registro: ' + str(i+2) + ', Contenido de registro: ' + str(df[2][i+1]) + ', El campo no continua el incremento de la serie numerica del folio')
                except:
                    True
                    
#======================Columna 4=================================
#======================ORGANO SUPERVISOR=========================

def col4(df):
    for i in range(len(df[3])):
        if df[3][i] == None or type(df[3][i]) == float:
            err.append('vacio, Columna 4, organo_supervisor, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[3][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            if df[3][i][0] != '0':
                err.append('numerico, Columna 4, organo_supervisor, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[3][i]) + ', La clave no comienza con un 0')
            
            if len(df[3][i]) != 6:
                err.append('longitud, Columna 4, organo_supervisor, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[3][i]) + ', La longitud del campo no es de 6 caracteres/la longitud del campo debe de ser de 6 caracteres númericos')
                
            if '-' in df[3][i]:
                err.append('alfanumerico, Columna 4, organo_supervisor, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[3][i]) + ', No se suprimió el guion intermedio de la clave')
                
            if df[3][i] not in cat_casfim:
                err.append('catalogo, Columna 4, organo_supervisor, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[3][i]) + ', La clave no corresponde al catalogo')
                

#======================Columna 5=================================
#======================SUJETO OBLIGADO===========================

def col5(df):
    for i in range(len(df[4])):
        if df[4][i] == None or type(df[4][i]) == float:
            err.append('vacio, Columna 5, sujeto_obligado, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[4][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio ')
        else:
            if len(df[4][i]) != 6:
                err.append('longitud, Columna 5, sujeto_obligado, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[4][i]) + ', La longitud del campo no es de 6 caracteres/la longitud del campo debe de ser de 6 caracteres númericos')
            
            if '-' in df[4][i]:
                err.append('alfanumerico, Columna 5, sujeto_obligado, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[4][i]) + ', No se suprimió el guion intermedio de la clave')
            
            if df[4][i][0] != '0':
                err.append('numerico, Columna 5, sujeto_obligado, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[4][i]) + ', La clave no comienza con un 0')
                
#======================Columna 6=================================
#======================LOCALIDAD=================================

def col6(df):
    for i in range(len(df[5])):
        if df[5][i] == None or type(df[5][i]) == float:
            err.append('vacio, Columna 6, localidad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[5][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        
        else:
            if len(df[5][i]) != 8:
                err.append('longitud, Columna 6, localidad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[5][i]) + ', La longitud del campo no es de 8 caracteres/la longitud del campo debe de ser de 8 caracteres númericos')
            ###### Hay muchos errores checar catalogos ####
            if df[5][i] not in cat_loc and df[5][i] not in cat_suc:
                err.append('catalogo, Columna 6, localidad,  Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[5][i]) + ', La localidad señalada no corresponde al catalogo')
            
                
#======================Columna 7=================================
#======================SUCURSALES================================

def col7(df):
    for i in range(len(df[6])):
        if df[33][i] == '00' or type(df[33][i]) == float:
            if df[6][i] == None or type(df[6][i]) == float:
                err.append('vacio, Columna 7, sucursal, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[6][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
            
            else:
                if len(df[6][i]) > 8:
                    err.append('longitud, Columna 7, sucursal, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[6][i]) + ', La longitud mínima del campo es de 1 carácter alfanumérico y la máxima es de 8 caracteres alfanuméricos')
                    
                #### Checar catalogo ###
                if df[6][i] not in cat_suc and str(df[6][i]) != '0':
                    err.append('catalogo, Columna 7, sucursal,  Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[6][i]) + ', El campo no contiene ninguna de las claves de sucursal entregadas por el cliente o el numero cero')
                
#======================Columna 8=================================
#======================TIPO DE OPERACION=========================

def col8(df):
    cat_op = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13','14', '15', '16', '17', '18', '19',
              '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
    for i in range(len(df[7])):
        if df[7][i] == None or type(df[7][i]) == float:
            err.append('vacio, Columna 8, tipo_de_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[7][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        
        else:
            if len(df[7][i]) != 2:
                err.append('longitud, Columna 8, tipo_de_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[7][i]) + ', La longitud del campo es de 2 caracteres conforme al catálogo')
                
            if df[7][i] not in cat_op:
                err.append('catalogo, Columna 8, tipo_de_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[7][i]) + ', El tipo de operación no corresponde al catalogo')
                
#======================Columna 9=================================
#======================INSTRUMENTO_MONETARIO=====================

def col9(df):
    cat_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    
    for i in range(len(df[8])):
        if df[8][i] == None or type(df[8][i]) == float:
            err.append('vacio, Columna 9, instrumento_monetario, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[8][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        
        else:
            if len(df[8][i]) != 2:
                err.append('longitud, Columna 9, instrumento_monetario, Numero de registro: ' + str(i+1) +', Contenido de registro: ' + str(df[8][i]) + ', La longitud del campo es de 2 caracteres conforme al catálogo')
            
            if df[8][i] not in cat_list:
                err.append('catalogo, Columna 9, instrumento_monetario, Numero de registro: ' + str(i+1) +', Contenido de registro: ' + str(df[8][i]) + ', El tipo de operación no corresponde al catalogo')
                
            if df[8][i] == '05' or df[8][i] == '06':
                if df[10][i].isdigit() == False and str(df[10][i][-1]) != '0' and str(df[10][i][-2]) != '0' and str(df[10][i][-3]) != '.':
                    err.append('catalogo, Columna 9, instrumento_monetario, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[8][i]) + ', El instrumento monetario es Oro/Platino/Plata amonedados revisar Columna 11 MONTO')
                    
#=======================Columna 10=================================
#======================NUMERO DE CUENTA============================

def col10(df):
    for i in range(len(df[9])):
        if df[9][i] == None or type(df[9][i]) == float:
            err.append('vacio, Columna 10, numero_de_cuenta, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[9][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(df[9][i]) > 16:
                err.append('longitud, Columna 10, numero_de_cuenta, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[9][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
            
            if len(df[9][i]) == 1:
                if str(df[9][i]) != '0':
                    err.append('longitud, Columna 10, numero_de_cuenta, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[9][i]) + ', La longitud del campo contiene un solo carácter numérico diferente a cero')

#======================Columna 11=================================
#======================MONTO======================================

def col11(df):
    a = []
    for i in range(len(df[10])):
        if df[10][i] == None or type(df[10][i]) == float:
            err.append('vacio, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(df[10][i]) > 17:
                err.append('longitud, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
            
            a.append(df[10][i].replace('.','').replace(' ',''))
            
            if df[8][i] == '05' or df[8][i] == '06':
                if df[10][i].isdigit() == False and str(df[10][i][-1]) != '0' and str(df[10][i][-2]) != '0' and str(df[10][i][-3]) != '.':
                    err.append('catalogo, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', El registro es Oro/plata/platino amonedado no se indicaron con un numero de unidades del metal en cantidades enteras')
                    
            if df[8][i] != '05' and df[8][i] != '06':
                if ' ' in df[10][i]:
                    err.append('catalogo, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', El registro contiene espacios en blanco y no debe ser asi pues debe truncarse con el caracter punto y coma (;)')
                
                else:
                    if df[10][i][-3] != '.':
                        err.append('catalogo, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', El monto de las operaciones no contiene decimales/ las primeras 14 posiciones se utilizan con enteros y las ultimas 2 posiciones se utilizan para los decimales/ las fracciones se separan con un punto')
                 
    for i in range(len(a)):
        if a[i].isdigit() == False:
            err.append('alfanumerico, Columna 11, monto, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[10][i]) + ', El registro contiene valores alfabeticos')
            
#======================Columna 12=================================
#======================CATALOGO MONEDA============================
def col12(df):
    for i in range(len(df[11])):
        if df[11][i] == None or type(df[11][i]) == float:
            err.append('vacio, Columna 12, catalogo_moneda, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[11][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')     
        else:
            if len(df[11][i]) > 3:
                err.append('longitud, Columna 12, catalogo_moneda, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[11][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
            if df[11][i] not in cat_mon:
                err.append('catalogo, Columna 12, catalogo_moneda, Numero de registro: ' + str(i+1) + ',  Contenido de registro: ' + str(df[11][i]) + ', La clave no corresponde al catalogo')
                

#======================Columna 13=================================
#======================FECHA DE LA OPERACION======================

def col13(df):
    for i in range(len(df[12])):
        if df[12][i] == None or type(df[12][i]) == float:
            err.append('vacio, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', El registro se encuentra vacio o tiene punto y coma y es obligatorio')
        else:
            if len(df[12][i]) != 8:
                err.append('longitud, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La cadena de números es mayor o menor a una longitud de 8 y La longitud del campo excede lo dispuesto en el DOF')
            
            if len(df[12][i]) != 8 or df[12][i].isdigit() == False :
                err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La secuencia numerica no cumple con el formato AAAAMMDD')
            
            if df[12][i].isdigit() == False :
                err.append('alfabetico, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', Hay información alfabética en el campo')
            
            else:    
                if len(df[12][i]) == 8:
                    if int(df[12][i][0:4]) < 2014:
                        err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', Los números de año son inferiores a 2014')
                        
                    if int(df[12][i][4:6]) > 12:
                        err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', Los números de mes son distintos a los números 1 al 12')
                    if int(df[12][i][0:4]) < 2014 or int(df[12][i][4:6]) > 12 or int(df[12][i][6:8]) > 31:
                        err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La secuencia numerica no cumple con el formato AAAAMMDD')
                    if df[12][i][4:6] == '01':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de enero')
                    
                    if df[12][i][4:6] == '02':
                            if df[12][i][0:4] in ['1804', '1808', '1812', '1816', '1820', '1824', '1828', '1832', '1836', '1840', '1844', '1848', '1852', '1856', '1860', '1864', '1868', '1872', '1876', '1880', '1884', '1888', '1892', '1896', '1904', '1908', '1912', '1916', '1920', '1924', '1928', '1932', '1936', '1940', '1944', '1948', '1952', '1956', '1960', '1964', '1968', '1972', '1976', '1980', '1984', '1988', '1992', '1996', '2000', '2004','2008','2012','2016','2020','2024','2028','2032','2036','2040','2044','2048','2052','2056','2060','2064','2068','2072','2076','2080','2084','2088','2092','2096']:
                                if int(df[12][i][6:8]) > 29:
                                    err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de febrero')
                            else:
                                if int(df[12][i][6:8]) > 28:
                                    err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de febrero')
                 
                    if df[12][i][4:6] == '03':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de marzo')
                    
                    if df[12][i][4:6] == '04':
                        if int(df[12][i][6:8]) > 30:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de abril')
                    
                    if df[12][i][4:6] == '05':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de mayo')
                    
                    if df[12][i][4:6] == '06':
                        if int(df[12][i][6:8]) > 30:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de junio')
                    
                    if df[12][i][4:6] == '07':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de julio')
                    
                    if df[12][i][4:6] == '08':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de agosto')
                
                    if df[12][i][4:6] == '09':
                        if int(df[12][i][6:8]) > 30:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de septiembre')
                            
                    if df[12][i][4:6] == '10':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de octubre')
                            
                    if df[12][i][4:6] == '11':
                        if int(df[12][i][6:8]) > 30:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de noviembre')
                            
                    if df[12][i][4:6] == '12':
                        if int(df[12][i][6:8]) > 31:
                            err.append('fecha, Columna 13, fecha_de_la_operacion, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[12][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de diciembre')
                            

#======================Columnas 14=================================
#======================VACIO=======================================
def col14(df):
    for i in range(len(df[13])):
        if df[13][i] == None or type(df[13][i]) == float:
            True
        else:
            err.append('vacio, Columna 14, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[28][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')
            
                            
#======================Columna 15=================================
#======================CATALOGO PAIS==============================

def col15(df):
    for i in range(len(df[14])):
        if df[14][i] == None or type(df[14][i]) == float:
            err.append('vacio, Columna 15, pais, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[14][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(df[14][i]) > 2:
                err.append('longitud, Columna 15, pais, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[14][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
            
            if (df[14][i]) not in cat_nac:
                err.append('catalogo, Columna 15, pais, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[14][i]) + ', El campo no contiene una clave encontrada en el catalogo')
                
#======================Columna 16=================================
#======================TIPO DE PERSONA============================

def col16(df):
    cat_tip_persona = ['1', '2']
    for i in range(len(df[15])):
        if df[15][i] == None or type(df[15][i]) == float:
            err.append('vacio, Columna 16, tipo_de_persona, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[15][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(df[15][i]) != 1:
                err.append('longitud, Columna 16, tipo_de_persona, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[15][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
                
            if df[15][i] not in cat_tip_persona:
                err.append('catalogo, Columna 16, tipo_de_persona, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[15][i]) + ', No se utilizaron las claves establecidas por el formato')                
                
#======================Columna 17=================================
#======================RAZON SOCIAL===============================

def col17(df):
    for i in range(len(df[16])):
        if df[15][i] == '1':
            if df[16][i] != None and type(df[16][i]) != float:
                err.append('relacion, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El registro debe ir vacio pues es una persona fisica')
        
        if df[15][i] == '2':
            if df[16][i] == None or type(df[16][i]) == float:
                err.append('relacion, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El registro no debe ir vacio pues es una persona Moral')
                
                if (df[18][i] == None or type(df[18][i]) == float) and (df[19][i] == None or type(df[19][i]) == float):
                    err.append('relacion, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El campo se encuentra vacío pero las columnas 19 y 20 también se encuentran vacías indicando la existencia de una persona moral')
    
            else:
                if len(df[16][i]) >= 300:
                    err.append('longitud, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El registro supera lo establecido en el DOF')
                    
                if df[21][i] != None and type(df[21][i]) != float:
                    err.append('alfanumerico, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El registro cuenta con caracteres alfanumérico pero la columna 22 cuenta con caracteres alfanuméricos indicando en el registro a una persona física y no una moral')
                    
                if (df[18][i] != None and type(df[18][i]) != float) or (df[19][i] != None and type(df[19][i]) != float) or df[18][i] == 'XXXX' or df[19][i] == 'XXXX':
                    err.append('relacion, Columna 17, razon_social, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[16][i]) + ', El campo cuenta con caracteres alfanumérico y las columnas 19 y 20 cuentan con caracteres alfanuméricos o XXXX indicando una persona física y no una moral')
                
#======================Columna 18=================================
#========================NOMBRE===================================

def col18(df):
    for i in range(len(df[17])):
        if df[15][i] == '1':
            if df[17][i] == None or type(df[17][i]) == float:
                err.append('vacio, Columna 18, nombre, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[17][i]) + ', El registro no debe ir vacio pues es una persona fisica')
                
                if df[21][i] != None or type(df[21][i]) != float:
                    err.append('relacion, Columna 18, nombre, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[17][i]) + ', La columna 22  tiene caracteres alfanumericos y el campo de la columna esta vacío')
                if (df[18][i] != None and type(df[18][i]) != float) or (df[19][i] != None and type(df[19][i]) != float):
                    err.append('relacion, Columna 18, nombre, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[17][i]) + ', Las columnas 19 y 20 contienen caracteres alfanuméricos y el campo de la columna esta vacio')
            else:
                if len(df[17][i]) > 60:
                        err.append('longitud, Columna 18, nombre, Numero de registro: ' + str(i+1) + ',  Contenido de registro: ' + str(df[17][i]) + ', La longitud del campo excede lo dispuesto en el DOF')

                        
#======================Columna 19=================================
#======================APELLIDO PATERNO===========================

def col19(df):
    for i in range(len(df[18])):
        if df[15][i] == '1':
            if df[19][i] == 'XXXX' or df[19][i] == None or type(df[19][i]) == float:
                if df[18][i] == None or type(df[18][i]) == float or df[18][i] == 'XXXX':
                    err.append('vacio, Columna 19, apellido_paterno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[18][i]) + ', La columna 20 tiene XXXX o esta vacio y el campo de esta columna esta vacío o tiene XXXX')
                    #if df[21][i] != None or type(df[21][i]) != float:
                    #    err.append('relacion, Columna 19, apellido_paterno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[18][i]) + ', El campo de la columna esta vacio pero la columna 22 contiene caracteres alfanuméricos')
                        
                    #if df[19][i] != None or type(df[19][i]) != float or df[19][i] == 'XXXX':
                    #    err.append('relacion, Columna 19, apellido_paterno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[18][i]) + ', El campo de la columna esta vacio pero la columna 20 contiene caracteres alfanuméricos o XXXX')
                        
                else:
                    if len(df[18][i]) > 30:
                        err.append('longitud, Columna 19, apellido_paterno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[18][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
        
        elif df[15][i] == '2':
            if df[18][i] != None and type(df[18][i]) != float:
                err.append('vacio, Columna 19, apellido_paterno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[18][i]) + ', El registro debe ir vacio pues es una persona Moral')
                
                
#======================Columna 20=================================
#======================APELLIDO MATERNO===========================

def col20(df):
    for i in range(len(df[19])):
        if df[15][i] == '1':
            if df[18][i] == 'XXXX' or df[18][i] == None or type(df[18][i]) == float:
                if df[19][i] == None or type(df[19][i]) == float or df[19][i] == 'XXXX':
                    err.append('vacio, Columna 20, apellido_materno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[19][i]) + ', La columna 19 tiene XXXX o esta vacio y el campo de esta columna esta vacío o tiene XXXX')
            #if df[18][i] == 'XXXX' and (df[21][i] != None or type(df[21][i]) != float):
            #    err.append('relacion, Columna 20, apellido_materno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[19][i]) + ', El campo de la columna esta vacío pero la columna 19 contiene XXXX y la columna 22  contiene caracteres alfanuméricos')
        
            if df[19][i] == None or type(df[19][i]) == float:
                True
            else:
                if len(df[19][i]) > 30:
                    err.append('longitud, Columna 20, apellido_materno, Numero de registro: '+ str(i+1) +', Contenido de registro: ' + str(df[19][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
        
        elif df[15][i] == '2':
            if df[19][i] != None and type(df[19][i]) != float:
                err.append('vacio, Columna 20, apellido_materno, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[19][i]) + ', El registro debe ir vacio pues es una persona Moral')
                
#======================Columna 21=================================
#======================RFC========================================

def col21(df):
    for i in range(len(df[20])):
        if df[15][i] == '1':
            if df[21][i] == None or type(df[21][i]) == float:
                if df[22][i] == None or type(df[22][i]) == float:
                    if df[20][i] == None or type(df[20][i]) == float:
                        err.append('relacion, Columna 21, RFC, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', La columna 22 y 23 están vacias al igual que la columna 21')
            
            if df[20][i] == None or type(df[20][i]) == float:
                True
            else:
                if len(df[20][i]) != 13:
                    err.append('longitud, Columna 21, rfc, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', La longitud del campo RFC no corresponde para el de una persona fisica')
                if '-' in df[20][i] or ' ' in df[20][i]:
                    err.append('alfanumerico, Columna 21, rfc, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', El RFC no debe de utilizar guion/espacio o cualquier otro tipo de carácter que no forme parte de el')
        
        if df[15][i] == '2':
            if df[21][i] == None or type(df[21][i]) == float:
                if df[22][i] == None or type(df[22][i]) == float:
                    if df[20][i] == None or type(df[20][i]) == float:
                        err.append('relacion, Columna 21, RFC, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', La columna 22 y 23 están vacias al igual que la columna 21')
            
            if df[20][i] == None or type(df[20][i]) == float:
                True
            else:
                if len(df[20][i]) != 12:
                    err.append('longitud, Columna 21, rfc, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', La longitud del campo RFC no corresponde para el de una persona moral')
                
                if '-' in df[20][i] or ' ' in df[20][i]:
                    err.append('alfanumerico, Columna 21, rfc, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[20][i]) + ', El RFC no debe de utilizar guion/espacio o cualquier otro tipo de carácter que no forme parte de el')
                
#======================Columna 22=================================
#======================CURP=======================================

def col22(df):
    for i in range(len(df[21])):
        if df[15][i] == '1' or df[15][i] == '2':
            if df[20][i] == None or type(df[20][i]) == float:
                if df[22][i] == None or type(df[22][i]) == float:
                    if df[21][i] == None or type(df[21][i]) == float:
                        err.append('relacion, Columna 22, curp, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[21][i]) + ', La columna 21 y 23 se encuentran vacias al igual que la columna 22')
            if df[21][i] == None or type(df[21][i]) == float:
                True
            else:
                if len(df[21][i]) != 18:
                    err.append('longitud, Columna 22, curp, Numero de registro: '+ str(i+1) +', Contenido de registro: ' + str(df[21][i]) + ', La longitud del campo es diferente a lo dispuesto en el DOF')
                    
#======================Columna 23=================================
#=========FECHA DE NACIMIENTO O CONSTITUCIÓN======================

def col23(df):
    for i in range(len(df[22])):
        if df[21][i] == None or type(df[21][i]) == float:
            if df[22][i] == None or type(df[22][i]) == float:
                err.append('relacion, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La columna esta vacia al igual que la columna 22')
        
        if df[20][i] == None or type(df[20][i]) == float:
            if df[22][i] == None or type(df[22][i]) == float:
                err.append('relacion, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La columna esta vacia al igual que la columna 21')
                
        if (df[21][i] == None or type(df[21][i]) == float) and (df[20][i] == None or type(df[20][i]) == float):
            if df[22][i] == None or type(df[22][i]) == float:
                err.append('relacion, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La columna 21 y la Columna 22 están vacías al igual que la Columna 23')
        
        if df[22][i] == None or type(df[22][i]) == float:
            True
        else:
            if len(str(df[22][i])) != 8:
                err.append('longitud, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
                
            if len(df[22][i]) != 8 or df[22][i].isdigit() == False :
                err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ',  Contenido de registro: ' + str(df[22][i]) + ', La secuencia numerica no cumple con el formato AAAAMMDD')
            
            if df[22][i].isdigit() == False :
                err.append('alfabetico, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', Hay información alfabética en el campo')
            
            else:    
                if len(df[22][i]) == 8:
                    if int(df[22][i][4:6]) > 12:
                        err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', Los números de mes son distintos a los números 1 al 12')
                    if int(df[22][i][4:6]) > 12 or int(df[22][i][6:8]) > 31:
                        err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La secuencia numerica no cumple con el formato AAAAMMDD')
                    if df[22][i][4:6] == '01':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de enero')
                    
                    if df[22][i][4:6] == '02':
                            if df[22][i][0:4] in ['1804', '1808', '1812', '1816', '1820', '1824', '1828', '1832', '1836', '1840', '1844', '1848', '1852', '1856', '1860', '1864', '1868', '1872', '1876', '1880', '1884', '1888', '1892', '1896', '1904', '1908', '1912', '1916', '1920', '1924', '1928', '1932', '1936', '1940', '1944', '1948', '1952', '1956', '1960', '1964', '1968', '1972', '1976', '1980', '1984', '1988', '1992', '1996', '2000', '2004','2008','2012','2016','2020','2024','2028','2032','2036','2040','2044','2048','2052','2056','2060','2064','2068','2072','2076','2080','2084','2088','2092','2096']:
                                if int(df[22][i][6:8]) > 29:
                                    err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de febrero')
                            else:
                                if int(df[22][i][6:8]) > 28:
                                    err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de febrero')
                 
                    if df[22][i][4:6] == '03':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de marzo')
                    
                    if df[22][i][4:6] == '04':
                        if int(df[22][i][6:8]) > 30:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de abril')
                    
                    if df[22][i][4:6] == '05':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de mayo')
                    
                    if df[22][i][4:6] == '06':
                        if int(df[22][i][6:8]) > 30:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de junio')
                    
                    if df[22][i][4:6] == '07':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de julio')
                    
                    if df[22][i][4:6] == '08':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de agosto')
                
                    if df[22][i][4:6] == '09':
                        if int(df[22][i][6:8]) > 30:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de septiembre')
                            
                    if df[22][i][4:6] == '10':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de octubre')
                            
                    if df[22][i][4:6] == '11':
                        if int(df[22][i][6:8]) > 30:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de noviembre')
                            
                    if df[22][i][4:6] == '12':
                        if int(df[22][i][6:8]) > 31:
                            err.append('fecha, Columna 23, fecha_de_nacimiento, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[22][i]) + ', La fecha no es válida/ el día no es válido correspondiente al mes de diciembre')
                                
#======================Columna 24=================================
#======================DOMICILIO==================================
def col24(df):
    for i in range(len(df[23])):
        if df[23][i] == None or type(df[23][i]) == float:
            err.append('vacio, Columna 24, domicilio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[23][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(df[23][i]) > 60:
                err.append('longitud, Columna 24, domicilio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[23][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
                
#======================Columna 25=================================
#======================COLONIA====================================
def col25(df):
    for i in range(len(df[24])):
        if df[24][i] == None or type(df[24][i]) == float:
            err.append('vacio, Columna 25, colonia, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[24][i]) + ', El registro se encuentra vacio o con punto y coma y es obligatorio')
        else:
            if len(str(df[24][i])) > 30:
                err.append('longitud, Columna 25, colonia, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[24][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
                
            if len(str(df[24][i])) == 1 and df[24][i] != '0':
                err.append('alfabetico, Columna 25, colonia, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[24][i]) + ', El campo contiene un solo carácter numérico o alfabetico distinto a 0')
                
#======================Columna 26=================================
#======================LOCALIDAD==================================
def col26(df):
    for i in range(len(df[25])):
        if df[25][i] == None or type(df[25][i]) == float:
            err.append('vacio, Columna 26, localidad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[25][i]) + ', El registro se encuentra vacio y es obligatorio ')
        else:
            if len(df[25][i]) > 8:
                err.append('longitud, Columna 26, localidad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[25][i]) + ', La longitud del campo excede lo dispuesto en el DOF')


#======================Columna 27=================================
#======================TELEFONO===================================
def col27(df):
    for i in range(len(df[26])):
        if df[26][i] == None or type(df[26][i]) == float:
            True
        else:
            if len(df[26][i]) > 40:
                err.append('longitud, Columna 27, telefono, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[26][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
            
            if not re.match('(([\d]{10,12})$|([CELULAR\s0-9\s/FIJO]{1,}))', df[26][i]) and '/' not in  df[26][i] and '(' not in  df[26][i] and ')' not in  df[26][i]:
                err.append('alfanumerico, Columna 27, telefono, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[26][i]) + ', El telefono no es válido')



#======================Columna 28=================================
#======================ACTIVIDAD==================================
def col28(df, act_eco):
    for i in range(len(df[27])):
        if df[27][i] == None or type(df[27][i]) == float:
            err.append('vacio, Columna 28, actividad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[27][i]) + ', El registro se encuentra vacio ')
        else:
            if len(df[27][i]) > 7:
                err.append('longitud, Columna 28, actividad, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[27][i]) + ', La longitud del campo excede lo dispuesto en el DOF')
                
            if df[27][i] not in act_eco:
                err.append('alfanumerico, Columna 28, actividad,  Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[27][i]) + ', El campo contiene caracteres alfanuméricos que no corresponden al catalogo')
            
                
                
#======================Columnas 29=================================
#======================VACIO=======================================
def col29(df):
    for i in range(len(df[28])):
        if df[28][i] == None or type(df[28][i]) == float:
            True
        else:
            err.append('vacio, Columna 29, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[28][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 30=================================
#======================VACIO=======================================
def col30(df):
    for i in range(len(df[29])):
        if df[29][i] == None or type(df[29][i]) == float:
            True
        else:
            err.append('vacio, Columna 30, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[29][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 31=================================
#======================VACIO=======================================
def col31(df):
    for i in range(len(df[30])):
        if df[30][i] == None or type(df[30][i]) == float:
            True
        else:
            err.append('vacio, Columna 31, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[30][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 32=================================
#======================VACIO=======================================
def col32(df):
    for i in range(len(df[31])):
        if df[31][i] == None or type(df[31][i]) == float:
            True
        else:
            err.append('vacio, Columna 32, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[31][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 33=================================
#======================VACIO=======================================
def col33(df):
    for i in range(len(df[32])):
        if df[32][i] == None or type(df[32][i]) == float:
            True
        else:
            err.append('vacio, Columna 33, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[32][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')
            
#======================Columnas 34=================================
#======================VACIO=======================================
def col34(df):
    for i in range(len(df[33])):
        if df[33][i] == None or type(df[33][i]) == float:
            True
        else:
            err.append('vacio, Columna 34, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[33][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 35=================================
#======================VACIO=======================================
def col35(df):
    for i in range(len(df[34])):
        if df[34][i] == None or type(df[34][i]) == float:
            True
        else:
            err.append('vacio, Columna 35, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[34][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 36=================================
#======================VACIO=======================================
def col36(df):
    for i in range(len(df[35])):
        if df[35][i] == None or type(df[35][i]) == float:
            True
        else:
            err.append('vacio, Columna 36, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[35][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 37=================================
#======================VACIO=======================================
def col37(df):
    for i in range(len(df[36])):
        if df[36][i] == None or type(df[36][i]) == float:
            True
        else:
            err.append('vacio, Columna 37, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[36][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 38=================================
#======================VACIO=======================================
def col38(df):
    for i in range(len(df[37])):
        if df[37][i] == None or type(df[37][i]) == float:
            True
        else:
            err.append('vacio, Columna 38, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[37][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')
            
#======================Columnas 39=================================
#======================VACIO=======================================
def col39(df):
    for i in range(len(df[38])):
        if df[38][i] == None or type(df[38][i]) == float:
            True
        else:
            err.append('vacio, Columna 39, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[38][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 40=================================
#======================VACIO=======================================
def col40(df):
    for i in range(len(df[39])):
        if df[39][i] == None or type(df[39][i]) == float:
            True
        else:
            err.append('vacio, Columna 40, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[39][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')

#======================Columnas 41=================================
#======================VACIO=======================================
def col41(df):
    for i in range(len(df[40])):
        if df[40][i] == None or type(df[40][i]) == float:
            True
        else:
            err.append('vacio, Columna 41, vacio, Numero de registro: ' + str(i+1) + ', Contenido de registro: ' + str(df[40][i]) + ', El campo de la columna contiene caracteres alfanuméricos debe ir vacio')


        
