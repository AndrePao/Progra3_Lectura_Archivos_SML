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
    lista=verifica(lista)
    return tipo_dato(lista) #invoca a la funcion verifica


#Funcion para agregar el tipo de dato a la lista de alcance
def tipo_dato(lista):
    for e in lista:
        if type(e[1])==int:		#Si es un int Agrega 'int'
            e+=['int']
        elif type(e[1])== bool:		#Si es un bool agregar 'bool'
            e+= ['boolean']
        elif type(e[1])== list:		#Si es de tipo lista llama a la funcion evalua tipo lista
            tipo_lista= Evalua_Tipo_Lista(e[1]) 
            e+=[tipo_lista]
        elif type(e[1])==tuple:		#Si es de tipo lista llama a la funcion evalua tipo tupla
            tipo_tupla= Evalua_Tipo_Tupla(e[1])
            e+=[tipo_tupla]
        else:
            e+=['string']
    return lista    

#Evalua el tipo de una tupla
def Evalua_Tipo_Tupla(tupla):
    Tipo=''
    for i in tupla:
        if type(i)==tuple:		#si la tupla contiene otra tupla, llama otra vez a la funcion de evalua tipo tupla
            res=Evalua_Tipo_Tupla(i)
            Tipo+='*'+res		#Agrega
            
        elif type(i)==int:		#Si es de tipo int y Tipo esta vacio agrega int sino agrega *int
            if Tipo=='':
                Tipo+='int'
            else:
                Tipo+='*int'

        elif type(i)==bool:		#Si es de tipo bool y Tipo esta vacio agrega bool sino agrega *bool
            if Tipo=='':
                Tipo+='bool'
            else:
                Tipo+='*bool'
            
        elif type(i)==list:		#Si es de tipo lista llama a la funcion evalua tipo lista con la lista 
            res=Evalua_Tipo_Lista(i)
            if Tipo=='':
                Tipo+=+res		#Agrega resultado
            else:
                Tipo+='*'+res
        
            
    return '('+Tipo+')'

# Funcion que evalua el tipo de dato de una lista
def Evalua_Tipo_Lista(Lista):
    Tipo=''
    if type(Lista[0])== int:    #si el primer elemento es de tipo int, es int list
        Tipo+= 'int list'
        
    elif type(Lista[0])== bool:   #si el primer elemento es de tipo bool, es bool list
        Tipo+= 'bool list'
        
    elif type(Lista[0])== tuple:	#si el primer elemento es de tipo tupla, se llama a la funcion evalua tipo tupla y se le agrega el list
        tipo_tupla= Evalua_Tipo_Tupla(Lista[0])
        Tipo+= tipo_tupla+' list'
        
    elif type(Lista[0])== list:		#si el primer elemento es de tipo list llama de nuevo a evalua tipo lista
        tipo=Evalua_Tipo_Lista(Lista[0])
        Tipo+= tipo+' list'
            
    return Tipo
        

#separa las lineas que se encuentran divididas por un ; o por un \n y elimina los espacios entre las letras
def separarLineas(LineaArchivo):
    Lista_Lineas=[] #almacena el archivo
    linea='' #almacena cada linea
    for elemento in LineaArchivo: #recorre el string
        if elemento==';' or elemento=='\n': #verifica cuando existe ; o salto de linea para almacenar la linea en la lista, significa que cambia de declaracion
            if linea!="": # Verifica que la linea no sea vacia
                if Lista_Lineas==[]:
                    Lista_Lineas.append(linea)
                    linea=''
                else:
                    n=Lista_Lineas[-1].find('let')
                    if linea[:3]!='val' or (linea[:3]=='val' and Lista_Lineas[-1][n:]=='let'):
                            Lista_Lineas[-1]+=linea
                    else:
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
        Valor=linea[contador+1:]
        return [[Variable,Valor]]
#Llamada por archivo_abrir, cuando termina
'''Recorre la lista donde estan separadas las variables y los valores,
ademas realiza los converciones de los valores'''
def verifica(lista):
    contador=0 #Se especifica el contador para conocer el alcance de las variables
    for i in lista:
        evaluando=i[1]
        n=0
        if evaluando[n]==" ":
            n=1
        if evaluando[n:].find('::')!=-1: #la funcion .find sirve para conocer si una expresion se encuentra en el string
            # En caso de encontrar la expresion :: concatena las listas
            i[1]=Concatenaaux(evaluando[n:],lista[:contador])
        elif evaluando[n:n+2]=='if':
            # En caso de encontrar la expresion if convierte las expresiones condicionales
            i[1]=Exp_If(evaluando[n:],lista[:contador])
        elif evaluando[n:].find('<=')!=-1 or evaluando[n:].find('orelse')!=-1 or evaluando[n:].find('andalso')!=-1 or evaluando[n:].find('<=')!=-1 or evaluando[n:].find('<')!=-1 or evaluando[n:].find('>')!=-1 or evaluando[n:].find('=')!=-1 or evaluando[n:].find('<>')!=-1:
            # convierte las expresiones booleans
            i[1]=ExpBooleans(evaluando[n:],lista[:contador])
        elif evaluando[n]=="[" :
            #Convierte el contenido de la lista
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido,lista[:contador])
            i[1]=contenido
        elif evaluando[n]=="(":
            #Convierte el contenido de las tuplas
            contenido=separa_contenido_estructuras(evaluando[n+1:-1])
            contenido=convertir_elemento(contenido,lista[:contador])
            i[1]=tuple(contenido)
        else:
            #Cambia variables por sus respectivos valores y conviente los numeros
            contenido=convertir_elemento([evaluando[n:]],lista[:contador])
            i[1]=contenido[0]
        contador+=1
    return lista

#Llamada por verifica(), cuando esta en proceso.
# Separa los elementos que se encuentran en una lista o tupla
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
        elif elemento[:2]=='if':
            lista.append(Exp_If(elemento,Scope))
        elif elemento.find('<=')!=-1 or elemento.find('orelse')!=-1 or elemento.find('andalso')!=-1 or elemento.find('<=')!=-1 or elemento.find('<')!=-1 or elemento.find('>')!=-1 or elemento.find('=')!=-1 or elemento.find('<>')!=-1:
            lista.append(ExpBooleans(elemento,Scope))
        elif elemento.find('+')!=-1 or elemento.find('-')!=-1 or elemento.find('*')!=-1 or elemento.find('/')!=-1 or elemento.find('div')!=-1 or elemento.find('mod')!=-1:
            lista.append(evaluarExpresionesN(elemento, Scope)[0])
        elif elemento.find('hd')!=-1 or elemento.find('tl')!=-1 or elemento.find('::')!=-1:
            lista.append(Concatenaaux(elemento,Scope))
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
    c=0
    EsNegativo=False
    largo=len(expresion)
    while cont!=largo:
        if expresion[cont]=='~':
            EsNegativo=True
        if expresion[cont].isdigit(): #si la letra es un numero o es negativo el numero
            numero+=expresion[cont]
        elif expresion[cont]=='#':  #cambieeeee
            c=cont
            expresionTupla=''
            while (expresion[c]!='+') and (expresion[c]!='-') and (expresion[c]!='*')and not ((expresion[c]=='d') and(expresion[c:c+3]=='div')) and not((expresion[c]=='m') and (expresion[c:c+3]=='mod')):
                expresionTupla+=expresion[c]
                c+=1
            variable=expresionTupla
            cont=c-1
        elif (expresion[cont]=='+') or (expresion[cont]=='-') or (expresion[cont]=='*') or (expresion[cont]=='/') or (expresion[cont]==')') or ((expresion[cont]=='d') and  (expresion[cont:cont+3]=='div')) or ((expresion[cont]=='m') and (expresion[cont:cont+3]=='mod')): #si la letra es un operador
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
                print variable
                ListaE.append(variable)
                variable=''
            if expresion[cont]== 'd':
                ListaE.append('/')
            elif expresion[cont]=='m':
                ListaE.append('%')
            else:
                ListaE.append(expresion[cont])
        elif (expresion[cont]=='('):
            ListaE.append(expresion[cont])
        elif (expresion[cont]!='~') and (expresion[cont]!=' '):   #si la letra es una variable
            if ((expresion[cont]=='i' and expresion[cont]!='v') and (expresion[cont-1:cont+2]!='div')) or ((expresion[cont]=='o' and expresion[cont]!='d') and (expresion[cont-1:cont+2]!='mod')):
                variable+=expresion[cont]
            elif ((expresion[cont] =='v') and ( expresion[cont-2:cont+1]!='div')) or ((expresion[cont] =='d') and ( expresion[cont-2:cont+1]!='mod')):
                variable+=expresion[cont]
            elif (expresion[cont]!='i') and (expresion[cont]!='v') and (expresion[cont]!='o') and (expresion[cont]!='d'):
                variable+=expresion[cont]
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



#funcion que obtiene el elemento de la tupla, EJ w= (1,2)  c=#1w 
def CambiaValorTupla(resultado,Variable):
    if len (Variable)==3 or len (Variable)==2:
        espacio=int(Variable[1])-1
        return resultado[espacio]
    else:
        cont=0
        
        for e in  Variable:
            if e== '(' and precedencia(Variable[cont+1:], '('):
                
                cont2=cont
                for i in Variable[cont:]:
                    if i== ')':
                        break
                    cont2+=1
                resultado= CambiaValorTupla(resultado,Variable[cont+1:cont2-1] )
                return CambiaValorTupla(resultado,Variable[:cont])#-1]#+Variable[cont2+1:])
            cont+=1
                
        
    
"""SE modifico"""
#funcion que cambia las variables por el valor real    
def Cambia_Variables(Variable,listaScope):
    resultado=Variable
    if Variable.find('#')!=-1: #si es un elemento de una tupla
        for i in Variable:
            if not Variable.isdigit() and i!='#' and i!= '(' and i!= ')':
                resultado=Cambia_Variables(i,listaScope)
                if not isinstance(resultado,tuple):
                    resultado= Variable
                else:
                    resultado=CambiaValorTupla(resultado, Variable)
                    
    else:
        for i in listaScope:
            if i[0]==Variable:
                resultado=i[1]
    return resultado
##############################################################################
##################Evaluar Expresiones con Listas##############################      
'''************************************************************************'''
'''En caso de encontar un parentesis completa la expresion, hace uso de la
funcion verifica_listas_tuplas para verificar que la expresion se encuentre
completa, esto ya que el se pueden evaluar precedencias de operaciones'''
'''************************************************************************'''
def completa_exp_Listas(Exp):
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
    Div=nueva.partition('::')
    Elementos+=Div[1:]
    return Elementos
"""'''***********************************************************************'''
'''Evalua las expresiones con lista y encuentra la operacion que se desea
realizar, las cuales pueden ser segun sml: '::','hd' y 'tl y
realiza las operaciones equivalentes en python''''
'''************************************************************************'''"""
def Exp_Listas(expresion,Lista):
    lista=[]

    if expresion.find("::")!=-1:
        if expresion[0]=='(':
            Div=completa_exp_Listas(expresion)
        else:
            Div=expresion.partition('::')
        Cabeza=convertir_elemento([Div[0]],Lista)
        Cuerpo=convertir_elemento([Div[2]],Lista)
        lista+=Cabeza+Cuerpo
    elif expresion.find('hd')!=-1:
        Div=expresion.partition('hd')
        Div=Div[1:]
        Cabeza=convertir_elemento([Div[1]],Lista)[0][0]
        lista=[Cabeza]
    elif expresion.find('tl')!=-1:
        Div=expresion.partition('tl')
        Div=Div[1:]
        Cuerpo=convertir_elemento([Div[1]],Lista)[0]
        lista+=[Cuerpo[1:]]
    if len(lista)==2 and isinstance(lista[1],list):
        lis=lista
        lista=[]
        lista=[lis[0]]+lis[1]
    if len(lista)==1 and isinstance(lista[0],list):
        lista=lista[0]
    return lista
"""*************************************************************************"""
""" su objetivo es cambiar variables en caso de que sea necesario"""
"""*************************************************************************"""

def Concatenaaux(expresion,lista2):
    lista=Exp_Listas(expresion,lista2)
    resultado=[]
    if isinstance(lista,int):
        lista=[lista]
    for e in lista:
        if isinstance(e,int):
            resultado+=[e]
        else:
            variable=[Cambia_Variables(e,lista2)]
            resultado+=variable
    if len(resultado)==1:
        resultado=resultado[0]
    elif len(resultado)==2 and isinstance(resultado[1],list):
        resul=resultado
        resultado=[]
        resultado=[resul[0]]+resul[1]
    return resultado
##############################################################################
##################Evaluar Expresiones Booleanas###############################
'''***********************************************************************'''
'''Evalua Expresiones Booleanas, busca en las expresiones al operador logico,
si lo encuentra resuelve la operacion, la lista de entrada
sirve para el cambio y el alcance de las variables.'''
'''************************************************************************'''    
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
    if Div==[]:
        Elementos=Divide(Elementos[0])
    if Div[0]=="":
        Div=Div[1:]   
    else:
        Elementos[0]='('+Elementos[0]+')'+Div[0]
        Div=Div[1:]
    Elementos+=Div
    return Elementos
"""***********************************************************************"""
'''Busca el primer operador en caso de que en una expresion compleja
se encuentren ambos(andalso,orelse), devuelve una lista de tres elementos,
la exresion antes del operador a evaluar, el operador a evaluar y por ultimo
la expresion siguiente a evaluar'''
"""***********************************************************************"""
def Divide(Exp):
    Div=[]
    And=Exp.find("andalso")
    Or=Exp.find("orelse")
    if (And < Or and And !=-1)or (And!=-1 and Or==-1):
        Div=list(Exp.partition("andalso"))
    elif (Or<And and Or!=-1)or(And==-1 and Or!=-1):
        Div=list(Exp.partition("orelse"))
    return Div

'''************************************************************************'''
'''Devuelve el resultado de la expresion booleana,
separa el elemento del lado izquierdo de lo expresion booleana (Primer)y el
del lado derecho(Segund), busca el signo de la operacion a aplicar y la lista
con el alcance y valor de las variables.
Invoca a la funcion Booleans para obtener el resultado y lo retorna'''
"""***********************************************************************"""
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
    else:
        if Exp[0]=='(' and Exp[-1]==')':
            Exp=Exp[1:-1]
        if Exp.find(' <= ')!=-1:
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
        elif Exp.find('<>')!=-1:
            n=Exp.find('<>')
            m=n+2
            signo='<>'
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

    return nueva  
"""************************************************************************"""
'''************************************************************************'''
'''Busca el signo equivalente de los operadores logucis de sml en python y
retorna el resultado, resive los parametros encontrados en la funcion anterior'''
"""***********************************************************************"""
def Booleans(Primer,Segund,Signo,lista):
    if not isinstance(Primer,int):
        Cambia_Variables(Primer,lista)
    if not isinstance(Segund,int):
        Cambia_Variables(Segund,lista)
    if Segund=="":
        return Primer
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
        return Primer!=Segund
    elif Signo== 'andalso':
        return Primer and Segund
    elif Signo== 'orelse':
        return Primer or Segund
    else:
        return 'Error'
##############################################################################
###############Expresiones Condicionales######################################
"""************************************************************************"""
'''Evalua Expresiones Condicionales, busca en las expresiones operadores como
if,then,elseif,else si lo encuentra resuelve la operacion en forma de descarte, la lista de entrada
sirve para el cambio y el alcance de las variables.'''
"""************************************************************************"""
def Exp_If(Exp,Lista):
    if Exp[:2]=='if':
        Div=Exp[2:].partition('then')
        realiza=convertir_elemento([Div[0]],Lista)
        if realiza[0]==True:
            resultado=DivExpIF(Div[2])
            return convertir_elemento([resultado[0]],Lista)[0]
        else:
            return Exp_If(Div[2],Lista)         
    else:
        realiza=DivExpIF(Exp)
        if realiza[1]=="elseif":
                realiza=realiza[2].partition('then')
                realiza2=convertir_elemento([realiza[0]],Lista)
                if realiza2[0]==True:
                    resultado=DivExpIF(realiza[2])
                    return convertir_elemento([resultado[0]],Lista)[0]
                else:
                    
                    return Exp_If(realiza[2],Lista)
        else:
            if realiza[1]=="else":
                resultado=realiza[2]
                if realiza[2][:3]=='(if':
                    resultado=realiza[2][1:-1]
                return convertir_elemento([resultado],Lista)[0]
"""**************************************************************************"""    
"""************************************************************************"""
'''Si en la operacion booleana no se cumple el if entonces se invoca a esta funcion
su objetivo es encontrar la siguiente expresion booleana sea elseif o else,
devuelve una lista'''
"""************************************************************************"""    
def DivExpIF(Exp):
    if Exp[:3]=='(if':
        RESUL=[]
        nueva=completa_exp_Listas2(Exp)[0]
        RESUL+=[nueva]
        nova=Exp.partition(nueva)
        ELSEIF=nova[2].find('elseif')
        ELSE=nova[2].find('else')
        DIV=[]
        if (ELSEIF < ELSE and ELSEIF !=-1)or (ELSEIF!=-1 and ELSE==-1) or (ELSEIF==ELSE and (ELSEIF!=-1 and ELSE!=-1)):
            DIV=nova[2].partition('elseif')
        elif (ELSE < ELSEIF and ELSE !=-1)or (ELSE!=-1 and ELSEIF==-1):
            DIV=nova[2].partition('else')
        else:
            return ['no','se','pudo']
        RESUL+=DIV[1:]
        RESUL[0]=RESUL[0][1:-1]
        return RESUL
    else:
        ELSEIF=Exp.find('elseif')
        ELSE=Exp.find('else')
        DIV=[]
        if (ELSEIF < ELSE and ELSEIF !=-1)or (ELSEIF!=-1 and ELSE==-1) or (ELSEIF==ELSE and (ELSEIF!=-1 and ELSE!=-1)):
            DIV=Exp.partition('elseif')
        elif (ELSE < ELSEIF and ELSE !=-1)or (ELSE!=-1 and ELSEIF==-1):
            DIV=Exp.partition('else')
        else:
            return ['no','se','pudo']

        return DIV
"""*************************************************************************"""
""""Si se encuentra un paraentesis en las expresiones booleanas se invoca
esta funcion para encontrar la operacion completa que se encuentra en el,
invoca a la funcion verifica_listas_tuplas para verificar los parentesis"""
"""*************************************************************************"""
def completa_exp_Listas2(Exp):
    Elementos=[]
    nueva=""
    contador=0
    for e in Exp:
        if e!=")":
            nueva+=e
        else:
            nueva+=e
            if verifica_listas_tuplas(nueva,"(",")"):
                Elementos+=[nueva]
                nueva=""
        contador+=1
    return Elementos
"""*************************************************************************"""
###############################################################################




                 




                
            
   
        




        




