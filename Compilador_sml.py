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


        
        
    






                 




                
            
   
        




        




