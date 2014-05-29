def abrir_archivo(NOMBRE):
    f= open (NOMBRE)
    lista=[]
    for line in f :
        lista=lista+Diccionario_Datos(line,"","")
    f.close()
    return lista
   

def Diccionario_Datos(linea,Variable,Valor):
    if linea[0:3]=="val":
        contador=3
        while linea[contador]!= "=":
            Variable+=linea[contador]
            contador+=1
        Valor=linea[contador+1:-1]
        return [[Variable,Valor]]
   
        




        




