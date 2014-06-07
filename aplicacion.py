from flask import Flask, render_template, request, redirect, url_for, abort, session
import compilador_sml

app = Flask(__name__)
#Pagina principal
@app.route('/')
def home():
    return render_template('principal.html')

#Pagina para subir achivo, recibe el archivo
@app.route('/upload_file',  methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
	lista=[] #almacena la informacion en una lista
    	lineas=''
    	for linea in f :
        	lineas+=linea
		
    	Lista_lineas=compilador_sml.separarLineas(lineas)#lista en la cual cada elemento es una linea diferente
   	for linea in Lista_lineas:
		
        	if linea[0:3]=="val": #determina si es una variable
           	 	lista+=compilador_sml.separa_variable_valor(linea,"","",4)
			
			
        	elif linea[0:3]!="fun": #determina si es una funcion
            		lista+=compilador_sml.separa_variable_valor(linea,"","",1)
			
        	else:
            		print"Es funcion"
        	
   	Lista=compilador_sml.verifica(lista) #invoca a la funcion verifica 
	Lista=compilador_sml.tipo_dato(Lista)
	print lista
    return render_template('restpla2.html', lista=Lista)

@app.route('/Principal')
def Principal():
    return render_template('home.html')
if __name__ == '__main__':
    app.run()

