#metodo que abre el archivo de sml
def abrir_archivo(NOMBRE):
    archivo= open (NOMBRE)
    lista=[] #almacena la informacion en una lista
    lineas=''
    for linea in archivo :
        lineas+=linea
    Lista_lineas=separarLineas(lineas)#lista en la cual cada elemento es una linea diferente
    for linea in Lista_lineas:
        if linea[0:3]=="val": #determina si es una variable
            lista+=separa_variable_valor(linea,"","",4)
        elif linea[0:3]!="fun": #determina si es una funcion
            lista+=separa_variable_valor(linea,"","",1)
        else:
            print"Es funcion"
        archivo.close() #cierra el archivo
    return verifica(lista) #invoca a la funcion verifica

#separa las lineas que se encuentran divididas por un ; o por un \n y elimina los espacios entre las letras
def separarLineas(LineaArchivo):
    Lista_Lineas=[] #almacena el archivo
    linea='' #almacena cada linea
    for elemento in LineaArchivo: #recorre el string
        if elemento==';' or elemento=='\n': #verifica cuando existe ; o salto de linea para almacenar la linea en la lista, significa que cambia de declaracion
            Lista_Lineas.append(linea)
            linea=''
        else:
            if elemento==' ' and linea[0:len(linea)]=='val': #ingresa un espacio si esta entre la el val y el nombre de la variable
                linea+=elemento
            elif elemento!= ' ': # no ingresa espacios
                linea+=elemento
    if linea!='':
        Lista_Lineas.append(linea) #agrega el elemento final a la lista
    return Lista_Lineas
    
#funcion que por cada declaracion de variable separa la variable y el valor
def separa_variable_valor(linea,Variable,Valor,contador):
        while linea[contador]!= "=":
            Variable+=linea[contador]
            contador+=1
        Valor=linea[contador+1:]#-1]
        return [[Variable,Valor]]
#Llamada por archivo_abrir, cuando termina
def verifica(lista):
    contador=0
    for i in lista:
        evaluando=i[1]
        n=0
        if evaluando[n]==" ":
            n=1
        if evaluando[n:].find('::')!=-1:
            i[1]=Concatenar(evaluando[n:],lista[:contador])
        elif evaluando[n:].find('<=')!=-1 or evaluando[n:].find('orelse')!=-1 or evaluando[n:].find('andalso')!=-1 or evaluando[n:].find('<=')!=-1 or evaluando[n:].find('<')!=-1 or evaluando[n:].find('>')!=-1 or evaluando[n:].find('=')!=-1 or evaluando[n:].find('<>')!=-1:
            i[1]=ExpBooleans(evaluando[n:],lista[:contador])
        elif evaluando[n]=="[" :
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido,lista[:contador])
            i[1]=contenido
        elif evaluando[n]=="(":
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido,lista[:contador])
            i[1]=tuple(contenido)
        elif evaluando[n:3]=="if":
            i[1]=i[1]
        else:
            contenido=convertir_elemento([evaluando[n:]],lista[:contador])
            i[1]=contenido[0]
        contador+=1
    return lista

#Llamada por verifica(), cuando esta en proceso.
def separa_contenido_estructuras(string):
    elementos=[]
    valor=""       
    for i in string:
        if i!=",":
             valor+=i
        else:
            if valor[0]=="[" and not verifica_listas_tuplas(valor,"[","]"):
                valor+=i
            elif valor[0]=="(" and not verifica_listas_tuplas(valor,"(",")"):
                valor+=i
            else:
                elementos+=[valor]
                valor=""
    elementos+=[valor]
    return elementos

#Verifica que las lista o tuplas estan bien cerradas.
def verifica_listas_tuplas(valor,signo,signo2):
    abrir=0
    cerrar=0
    for i in valor:
        if i==signo:
            abrir+=1
        else:
            if i==signo2:
                cerrar+=1
    return abrir==cerrar

def convertir_elemento(ListaSeparada,Scope):
    lista=[]
    for elemento in ListaSeparada:
        if elemento.isdigit():
            lista.append(int(elemento))
        elif elemento[0]=='~' and  elemento[1:].isdigit():
            lista.append(-1*int(elemento[1:]))
        elif elemento.find('<=')!=-1 or elemento.find('orelse')!=-1 or elemento.find('andalso')!=-1 or elemento.find('<=')!=-1 or elemento.find('<')!=-1 or elemento.find('>')!=-1 or elemento.find('=')!=-1 or elemento.find('<>')!=-1:
            lista.append(ExpBooleans(elemento,Scope))
        elif elemento.find('+')!=-1 or elemento.find('-')!=-1 or elemento.find('*')!=-1 or elemento.find('/')!=-1 or elemento.find('div')!=-1 or elemento.find('mod')!=-1:
            lista.append(evaluarExpresionesN(elemento, Scope)[0])
        elif elemento[0]=='[':
            x=convertir_elemento(separa_contenido_estructuras(elemento[1:-1]),Scope)
            lista.append(x) 
        elif elemento[0]=='(':
            x=convertir_elemento(separa_contenido_estructuras(elemento[1:-1]),Scope)
            lista.append(tuple(x))
        elif elemento.lower()=='true' or elemento.lower()== ' true':
            lista.append(True)
        elif elemento.lower()=='false' or elemento.lower()==' false':
            lista.append(False)
        else:
            lista.append(Cambia_Variables(elemento,Scope))
    return lista

#***************************************************************************
#funcion que evalua las expresiones numericas, los operadores y las variables, las ingresa todas a una lista, invoca a una funcion
#y devuelve el resultado de la operacion
def evaluarExpresionesN(expresion, ListaEvaluada):
    ListaE=[] #almacena la expresion
    numero='' #variable q guardara el numero
    variable=''
    cont=0
    EsNegativo=False
    for e in expresion: #recorre el string
        if e=='~':
            EsNegativo=True
        if e.isdigit(): #si la letra es un numero o es negativo el numero
            numero+=e
        elif (e=='+') or (e=='-') or (e=='*') or (e=='/') or (e==')') or ((e=='d') and  (expresion[cont:cont+3]=='div')) or ((e=='m') and (expresion[cont:cont+3]=='mod')): #si la letra es un operador
            if numero.isdigit():
                if EsNegativo:
                    EsNegativo=False
                    numero='~'+numero
                Numero= convertir_elemento([numero], ListaEvaluada)
                ListaE.append(Numero[0])
                numero=''
            elif variable!='':
                variable=Cambia_Variables(variable,ListaEvaluada)#funcion pao obtengo el valor de la variable
                if EsNegativo:
                    EsNegativo=False
                    variable=-1*variable
                ListaE.append(variable)
                variable=''
            if e== 'd':
                ListaE.append('/')
            elif e=='m':
                ListaE.append('%')
            else:
                ListaE.append(e)
        elif (e=='('):
            ListaE.append(e)
        elif (e!='~') and (e!=' '):   #si la letra es una variable
            if ((e=='i' and e!='v') and (expresion[cont-1:cont+2]!='div')) or ((e=='o' and e!='d') and (expresion[cont-1:cont+2]!='mod')):
                variable+=e
            elif ((e =='v') and ( expresion[cont-2:cont+1]!='div')) or ((e =='d') and ( expresion[cont-2:cont+1]!='mod')):
                variable+=e
            elif (e!='i') and (e!='v') and (e!='o') and (e!='d'):
                variable+=e
        cont+=1
    if numero.isdigit():
        if EsNegativo:
            EsNegativo=False
            numero='~'+numero
        Numero= convertir_elemento([numero],ListaEvaluada)
        ListaE.append(Numero[0])
    elif variable!='':
        variable=Cambia_Variables(variable,ListaEvaluada)#funcion pao obtengo el valor de la variable
        ListaE.append(variable)
        variable=''
    valorExpresion=  OperacionE(ListaE)
    return valorExpresion

#Le ingresa una lista con la expresion y va desarrollando cada operacion, es recursiva
def OperacionE(ListaE):
    if len(ListaE)==1:
        return ListaE
    elif len(ListaE)==2:
        return [ListaE[0]+ListaE[1]]
    else:
        contador=0
        for operador in ListaE:
            if operador=='('and precedencia(ListaE[contador+1:],operador):
                c=0
                for i in ListaE[contador:]:
                
                    if i==')':
                        break
                    c+=1
                resultado=OperacionE(ListaE[contador+1:c+contador])
                ListaE=ListaE[:contador]+resultado+ListaE[contador+c+1:]
                break
            elif  (operador=='/' or operador=='*' or operador=='%') and precedencia(ListaE[contador:],operador):
                resultado=Result_Operacion(ListaE[contador-1:contador+2])
                ListaE=ListaE[:contador-1]+resultado+ListaE[contador+2:]
                break
            elif  (operador=='+' or operador== '-')and precedencia(ListaE[contador:],operador):
                resultado=Result_Operacion(ListaE[contador-1:contador+2])
                ListaE=ListaE[:contador-1]+resultado+ListaE[contador+2:]
                break
            contador+=1
        return OperacionE(ListaE)


#retorna el resultado de aplicar el operador a los dos numeros                
def Result_Operacion(Operacion):
    Result=0 #almacena el resultado
    if Operacion[1]=='+': #si el operador es suma
        Result= Operacion[0]+ Operacion[2]
    elif Operacion[1]=='-': #si el operador es resta
        Result= Operacion[0]-Operacion[2]
    elif Operacion[1]=='*': #si el operador es multiplicacion
        Result= Operacion[0]*Operacion[2]
    elif Operacion[1]=='/': #si el operador es division
        Result= Operacion[0]/ Operacion[2]
    elif Operacion[1]=='%': #si el operador es modulo
        Result= Operacion[0]% Operacion[2]
    return [Result]

#verifica si existe un operador de mayor precendia del que hay.
def precedencia(Lista,operador):
    for elemento in Lista:
        if ((elemento=='(')): #si hay una operacion entre parentesis anidada
            return False
        elif ((elemento=='(') or (elemento=='/') or (elemento=='*')) and (operador== '+' or operador=='-'): #si el operador es suma o resta y existe otro operador de mayor precedencia
            return False
        elif (elemento== '(') and (operador== '*' or operador=='/'): #si el operador es una multiplicacion o division  existe un parentesis despues de la operacion
            return False
    return True #si no encontro un operador de precedencia.
#***********************************************************************

########Cambia Variables por Valores####################
def Cambia_Variables(Variable,listaScope): 
    resultado=Variable
    for i in listaScope:
        if i[0]==Variable:
            resultado=i[1]
    return resultado

#########Concatena_Listas#################################       
def Concatenar(expresion,Lista):
    lista=[]
    if expresion.find("::")!=-1:
        n=expresion.find("::")
        nueva=convertir_elemento([expresion[:n]],Lista)
        lista+=nueva +Concatenar(expresion[n+2:],Lista)
    else:
        nueva=convertir_elemento([expresion],Lista)
        lista+=nueva[0]
    return lista

def Concatenaaux(expresion,lista2):
    lista=Concatenar(expresion,lista2)
    resultado=[]
    for e in lista:
        if isinstance(e,int):
            resultado+=[e]
        else:
            variable=[Cambia_Variables(e,lista2)]
            resultado+=variable
    return resultado
#########################################################
    
def completa_exp_booleans(Exp):
    Elementos=[]
    nueva=""
    contador=0
    for e in Exp:
        if e!=")":
            nueva+=e
        else:
            nueva+=e
            if verifica_listas_tuplas(nueva,"(",")"):
                Elementos+=[nueva[1:-1]]
                nueva=""
        contador+=1

    Div=Divide(nueva)
    Div=Div[1:]
    Elementos+=Div
    if Div==[]:
        print Elementos[0]
        Elementos=Divide(Elementos[0])
    return Elementos

def Divide(Exp):
    Div=[]
    And=Exp.find("andalso")
    Or=Exp.find("orelse")
    if (And < Or and And !=-1)or (And!=-1 and Or==-1):
        Div=list(Exp.partition("andalso"))
    elif (Or<And and Or!=-1)or(And==-1 and Or!=-1):
        Div=list(Exp.partition("orelse"))
    return Div
    
    
def ExpBooleans(Exp,lista):
    if Exp.find('andalso')!=-1 or Exp.find('orelse')!=-1:
        if Exp[0]=="(":
            Div=completa_exp_booleans(Exp)
            Primer=ExpBooleans(Div[0],lista)
            if len(Div)==3:
                Segund=ExpBooleans(Div[2],lista)
            else:
                Segund=ExpBooleans(Div[1],lista)
            nueva=Booleans(Primer,Segund,Div[1],lista)
        else:
            Div=Divide(Exp)
            Primer=ExpBooleans(Div[0],lista)
            Segund=ExpBooleans(Div[2],lista)
            nueva=Booleans(Primer,Segund,Div[1],lista)
        
    elif Exp.find(' <= ')!=-1:
        n=Exp.find(' <= ')
        m=n+2
        signo='<='
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0],Segund[0],signo,lista)
    elif Exp.find('>=')!=-1:
        n=Exp.find('>=')
        m=n+2
        signo='>='
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0],Segund[0],signo,lista)
    elif Exp.find('<')!=-1:
        n=Exp.find('<')
        m=n+1
        signo='<'
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0],Segund[0],signo,lista)
    elif Exp.find('>')!=-1:
        n=Exp.find('>')
        m=n+1
        signo='>'
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0],Segund[0],signo,lista)
    elif Exp.find('=')!=-1:
        n=Exp.find('=')
        m=n+1
        signo='='
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0],Segund[0],signo,lista)
    elif Exp.find('<>')!=-1:
        n=Exp.find('<>')
        m=n+1
        signo='<>'
        Primer=convertir_elemento([Exp[:n]],lista)        
        Segund=convertir_elemento([Exp[m:]],lista)
        nueva=Booleans(Primer[0][:-1],Segund[0][1:],signo,lista)

        
    return nueva    

def Booleans(Primer,Segund,Signo,lista):
    if not isinstance(Primer,int):
        Cambia_Variables(Primer,lista)
    if not isinstance(Segund,int):
        Cambia_Variables(Segund,lista)
    if Signo=='<':
        return Primer < Segund
    elif Signo=='>':
        return Primer > Segund
    elif Signo =='=':
        return Primer == Segund
    elif Signo =='<=':
        return Primer<= Segund
    elif Signo =='>=':
        return Primer >= Segund
    elif Signo =='<>':
        return Primer!=Segundo
    elif Signo== 'andalso':
        return Primer and Segund
    elif Signo== 'orelse':
        return Primer or Segund
    else:
        return 'Error'

    






                 




                
            
   
        




        




