def abrir_archivo(NOMBRE):
    f= open (NOMBRE)
    lista=[]
    for line in f :
        if line[0:3]=="val":
            lista+=separa_variable_valor(line,"","",3)
        elif line[0:3]!="fun":
            lista+=separa_variable_valor(line,"","",0)
        else:
            print"Es funcion"
    f.close()
    return lista


def separa_variable_valor(linea,Variable,Valor,contador):
        while linea[contador]!= "=":
            Variable+=linea[contador]
            contador+=1
        Valor=linea[contador+1:-1]
        return [[Variable,Valor]]




                
            
        




        




