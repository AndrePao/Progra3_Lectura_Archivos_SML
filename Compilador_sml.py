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
    
#Lamada por archivo_abrir, cuando termina
def verifica(lista):
    contador=0
    for i in lista:
        evaluando=i[1]
        n=0
        if evaluando[n]==" ":
            n=1
        if evaluando[n:].isdigit():
            i[1]=int(evaluando[n:])
        elif evaluando[n:].lower()=='false':
            i[1]=False
        elif evaluando[n:].lower()=='true':
            i[1]=True
        elif evaluando[n]=="[" :
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido)
            i[1]=contenido
        elif evaluando[n]=="(":
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido)
            i[1]=tuple(contenido)
        else:
            i[1]=evaluando
        contador+=1
    return lista

#Lamada por verifica(), cuando esta en proceso.
def separa_contenido_estructuras(string):
    elementos=[]
    valor=""       
    for i in string:
        if i!=",":
             valor+=i
        else:
            if valor[0]=="[" and not verifica2(valor,"[","]"):
                valor+=i
            elif valor[0]=="(" and not verifica2(valor,"(",")"):
                valor+=i
            else:
                elementos+=[valor]
                valor=""
    elementos+=[valor]
    return elementos

#Verifica que las lista o tuplas estan bien cerradas.
def verifica2(valor,signo,signo2):
    abrir=0
    cerrar=0
    for i in valor:
        if i==signo:
            abrir+=1
        else:
            if i==signo2:
                cerrar+=1
    return abrir==cerrar


def convertir_elemento(ListaSeparada):
    lista=[]
    for elemento in ListaSeparada:
        if elemento.isdigit():
            lista.append(int(elemento))
        elif elemento[0]=='[':
            print 'entre'
            x=convertir_elemento(separa_contenido_estructuras(elemento[1:-1]))
            lista.append(x) #funcion de paola
        elif elemento[0]=='(':
            x=convertir_elemento(separa_contenido_estructuras(elemento[1:-1]))
            lista.append(tuple(x))#funcion de paola
        elif elemento.lower()== 'true' or elemento.lower()== ' true':
            lista.append(True)
        elif elemento.lower()=='false' or elemento.lower()==' false':
            lista.append(False)
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
            
   
        
        
    






                 




                
            
   
        




        




