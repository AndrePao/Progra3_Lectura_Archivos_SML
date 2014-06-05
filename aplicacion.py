
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('principal.html')


@app.route('/upload_file',  methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
	lista=[] #almacena la informacion en una lista
    	lineas=''
    	for linea in f :
        	lineas+=linea
		print"Lee linea"
    	Lista_lineas=separarLineas(lineas)#lista en la cual cada elemento es una linea diferente
   	for linea in Lista_lineas:
		print"Dentro de segundo if"
        	if linea[0:3]=="val": #determina si es una variable
           	 	lista+=separa_variable_valor(linea,"","",4)
			print"Dentro if linea"
			print lista
        	elif linea[0:3]!="fun": #determina si es una funcion
            		lista+=separa_variable_valor(linea,"","",1)
			print"Dentro elif linea"
        	else:
            		print"Es funcion"
        print "FIN"	
   	Lista=verifica(lista) #invoca a la funcion verifica 
	lista1=tipo_dato(Lista)
    return render_template('restpla2.html', lista=lista1)

@app.route('/Principal')
def Principal():
    return render_template('home.html')
if __name__ == '__main__':
    app.run()

