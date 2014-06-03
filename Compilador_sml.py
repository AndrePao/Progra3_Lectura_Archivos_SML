def abrir_archivo(NOMBRE):
    f= open (NOMBRE)
    lista=[]
    for line in f :
        if line[0:3]=="val":
            lista+=separa_variable_valor(line,"","",4)
        elif line[0:3]!="fun":
            lista+=separa_variable_valor(line,"","",1)
        else:
            print"Es funcion"
    f.close()
    return verifica(lista)

#Llamada por archivo_abrir, mientras lo lee

def separa_variable_valor(linea,Variable,Valor,contador): 
        while linea[contador]!= "=":
            Variable+=linea[contador]
            contador+=1
        Valor=linea[contador+1:-1]
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
        elif elemento.find('<=')!=-1 or elemento.find('orelse')!=-1 or elemento.find('andalso')!=-1 or elemento.find('<=')!=-1 or elemento.find('<')!=-1 or elemento.find('>')!=-1 or elemento.find('=')!=-1 or elemento.find('<>')!=-1:
            lista.append(ExpBooleans(elemento,Scope))
        elif elemento.find('+')!=-1 or elemento.find('-')!=-1 or elemento.find('*')!=-1 or elemento.find('/')!=-1 or elemento.find('div')!=-1 or elemento.find('mod')!=-1:
            lista.append(evaluarExpresionesN(elemento, Scope)[0])
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
                Numero= convertir_elemento([numero])
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
        Numero= convertir_elemento([numero])
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
                ListaE=ListaE[:contador]+resultado+ListaE[contador+c+2:]
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
    
def ExpBooleans(Exp,lista):
        
    if Exp.find('andalso')!=-1:
        Div=Exp.partition(' andalso ')
        Primer=ExpBooleans(Div[0],lista)
        if Div[2][0]=='(':
            se=Div[2][1:-1]
            Segund=ExpBooleans(se,lista)
        else:
            Segund=ExpBooleans(Div[2],lista)
        nueva=Booleans(Primer,Segund,'andalso',lista)
    elif Exp.find('orelse')!=-1:
        Div=Exp.partition(' orelse ')
        Primer=ExpBooleans(Div[0],lista)
        Segund=ExpBooleans(Div[2],lista)
        nueva=Booleans(Primer,Segund,'orelse',lista)
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

    






                 




                
            
   
        




        




