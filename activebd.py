#activebd 4.00 15/02/2020


from __future__ import unicode_literals
import webapp2
import os
import datetime
import MySQLdb
from google.appengine.api import users
from google.appengine.ext.webapp import template
#from datetime import timedelta

# BASE DE DATOS
################################

# These environment variables are configured in app.yaml
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE= os.environ.get('CLOUDSQL_DATABASE')

def connect_to_cloudsql():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):

        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD,
            db=CLOUDSQL_DATABASE,
            charset='utf8')

    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db



def get_db():
    conn = connect_to_cloudsql()
    return conn

#INICI APLICACIO
class MainPage(webapp2.RequestHandler):
    def get(self):
            self.redirect("/Inicio") #Redirecciona a Inicio
            






###########################################################################################################################################################
# CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES      CONTROL D'ACCES     
########################################################################################################################################################### 
    
def autentificacio(self, users):
    user = users.get_current_user()
    lista = travailleurAct()
    dernierePos = len(lista)-1
    idTravailleur= -1
    
    
    if user:
        
        i=0
        while(i<=dernierePos):
            travailleur=lista[i]
            if user.nickname() ==travailleur.mail:           
                idTravailleur= travailleur.idTravailleur
                i=dernierePos+1
                
            else :
                idTravailleur=-1
                i+=1
    if(idTravailleur == -1):
        self.redirect(users.create_login_url(self.request.uri))
                          
    return idTravailleur

def travailleurAct():
    db= get_db()
    cursor = db.cursor()
    lista= tablaTravailleurAct(cursor)
    db.commit()
    db.close()
    return lista

def tablaTravailleurAct(cursor):   
    cursor.execute('SELECT idTravailleur, codeTravailleur, nomTravailleur, mail, activite FROM TRAVAILLEUR WHERE activite=%s',(1,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Travailleur(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 
           
class Travailleur: 
    def __init__(self, idTravailleur=0, codeTravailleur='', nomTravailleur='', mail='', activite=0):
        self.idTravailleur = idTravailleur
        self.codeTravailleur = codeTravailleur
        self.nomTravailleur = nomTravailleur
        self.mail = mail
        self.activite = activite
   




#---------------------------------------------------------------------------------------------------------------
#    FUNCIONS GENERALS   
#---------------------------------------------------------------------------------------------------------------

#-- FUNCIO DATA FORMAT
#-- Convertix una data al format 2014-01-25
def dataFormat(data):
    try:
        dataF= data.strftime("%Y-%m-%d") # data amb format 
    except:
        dataF= ""
    return dataF

def novar(variable):
    if variable is not None and variable != '':
        variable = variable
    else:
        variable = ""
    return variable

class Proforme:
    def __init__(self, idProforme=0, idIntervention=0, dateProforme='', nombreProforme='', datePaye=''):
        self.idProforme = idProforme
        self.idIntervention = idIntervention
        self.dateProforme = dateProforme
        self.nombreProforme = nombreProforme
        self.datePaye = datePaye

def tablaUltimProforme(cursor):
    cursor.execute('SELECT idProforme, idIntervention, dateProforme, nombreProforme, datePaye FROM PROFORME ORDER BY nombreProforme DESC LIMIT 0,1')
    lista = cursor.fetchall()
    datoD = lista[0][3]
    for i in lista: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista1 = Proforme(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
    idConstant=1
    cursor.execute('SELECT nombreProformeEx, dateProformeEx FROM CONSTANT WHERE idConstant=%s', (idConstant,))
    lista = cursor.fetchall()
    datoC = lista[0][0]
    for i in lista: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[1])       
        lista2 = Proforme(0,0,data,i[0],'') #Modificar si anyadim columna
    if datoD>datoC:
        lista=lista1
    elif datoD<datoC:
        lista=lista2
    else:
        lista=lista2
    return lista1 
###########################################################################################################################################################
# INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE      INDICE
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariInicio (usuari):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    ultimDevis = tablaUltimDevis(cursor)
    ultimFacture = tablaUltimFacture(cursor)
    ultimProforme = tablaUltimProforme(cursor)
    
    #desconectar de la bd
    db.commit()
    db.close()
    
    

    #pasem les llistes al arxiu html
    values = {
             'travailleurSelect': travailleurSelect,
             'ultimDevis': ultimDevis,
             'ultimFacture': ultimFacture,
             'ultimProforme': ultimProforme,
              }
    return values   

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################
def tablaTravailleurSelect(cursor, idTravailleur):
    cursor.execute('SELECT  idTravailleur, codeTravailleur, nomTravailleur, mail, activite FROM TRAVAILLEUR WHERE idTravailleur=%s',(idTravailleur,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Travailleur(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna
    return lista        


def tablaTravailleurTots(cursor):   
    cursor.execute('SELECT idTravailleur, codeTravailleur, nomTravailleur, mail, activite FROM TRAVAILLEUR  ORDER BY activite DESC, nomTravailleur')
    expedients = cursor.fetchall()
    conta=0
    indice=0
    for i in expedients: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in expedients: #cada fila es converteix en un objecte de lista
        lista[indice] = Travailleur(i[0],i[1],i[2],i[3],i[4]) #Modificar si anyadim columna
        indice=indice+1   
    return lista

def tablaUltimDevis(cursor):
    cursor.execute('SELECT idDevis, idIntervention, dateDevis, nombreDevis FROM DEVIS ORDER BY nombreDevis DESC LIMIT 0,1')
    lista = cursor.fetchall()
    datoD = lista[0][3]
    for i in lista: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[2])       
        lista1 = Devis(i[0],i[1],data,i[3]) #Modificar si anyadim columna
    idConstant=1
    cursor.execute('SELECT nombreDevisEx, dateDevisEx FROM CONSTANT WHERE idConstant=%s', (idConstant,))
    lista = cursor.fetchall()
    datoC = lista[0][0]
    for i in lista: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[1])       
        lista2 = Devis(0,0,data,i[0]) #Modificar si anyadim columna
    if datoD>datoC:
        lista=lista1
    elif datoD<datoC:
        lista=lista2
    else:
        lista=lista2
        
    return lista

class Devis:
    def __init__(self, idDevis=0, idIntervention=0, dateDevis='', nombreDevis=''):
        self.idDevis = idDevis
        self.idIntervention = idIntervention
        self.dateDevis = dateDevis
        self.nombreDevis = nombreDevis

def tablaUltimFacture(cursor):
    cursor.execute('SELECT idFacture, idIntervention, dateFacture, nombreFacture, datePaye FROM FACTURE ORDER BY nombreFacture DESC LIMIT 0,1')
    lista = cursor.fetchall()
    datoD = lista[0][3]
    for i in lista: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista1 = Facture(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
    idConstant=1
    cursor.execute('SELECT nombreFactureEx, dateFactureEx FROM CONSTANT WHERE idConstant=%s', (idConstant,))
    lista = cursor.fetchall()
    datoC = lista[0][0]
    for i in lista: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[1])       
        lista2 = Facture(0,0,data,i[0],'') #Modificar si anyadim columna
    if datoD>datoC:
        lista=lista1
    elif datoD<datoC:
        lista=lista2
    else:
        lista=lista2
    return lista

class Facture:
    def __init__(self, idFacture=0, idIntervention=0, dateFacture='', nombreFacture='', datePaye=''):
        self.idFacture = idFacture
        self.idIntervention = idIntervention
        self.dateFacture = dateFacture
        self.nombreFacture = nombreFacture
        self.datePaye = datePaye



# ACCIONS DEL FORMULARI
####################################
class Inicio(webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            #obtenim valors per al html
            values = formulariInicio(usuari)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values))
        else:
            self.response.out.write("acceso denegado")


#--CAPTURA DADES DEL HTML I EDITA
class UltimDevisEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html
            idConstant=1
            nombreDevisEx = novar(self.request.get('nombreDevisEx'))
            dateDevisEx = novar(self.request.get('dateDevisEx'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            #edita fila en tabla
            cursor.execute('UPDATE CONSTANT SET nombreDevisEx=%s, dateDevisEx=%s WHERE idConstant=%s', (nombreDevisEx, dateDevisEx, idConstant))
            #desconectar de la bd
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #obtenim valors per al html
            values = formulariInicio(usuari)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values))

#--CAPTURA DADES DEL HTML I EDITA
class UltimFactureEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):                
            #captura camps del html
            idConstant=1
            nombreFactureEx = novar(self.request.get('nombreFactureEx'))
            dateFactureEx = novar(self.request.get('dateFactureEx'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            #edita fila en tabla
            cursor.execute('UPDATE CONSTANT SET nombreFactureEx=%s, dateFactureEx=%s WHERE idConstant=%s', (nombreFactureEx, dateFactureEx, idConstant))
            #desconectar de la bd
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #obtenim valors per al html
            values = formulariInicio(usuari)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values))
            
#--CAPTURA DADES DEL HTML I EDITA
class UltimProformeEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):                
            #captura camps del html
            idConstant=1
            nombreProformeEx = novar(self.request.get('nombreProformeEx'))
            dateProformeEx = novar(self.request.get('dateProformeEx'))

            #conectar a la bd
            db= get_db()
            cursor = db.cursor()
            #edita fila en tabla
            cursor.execute('UPDATE CONSTANT SET nombreProformeEx=%s, dateProformeEx=%s WHERE idConstant=%s', (nombreProformeEx, dateProformeEx, idConstant))
            #desconectar de la bd
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #obtenim valors per al html
            values = formulariInicio(usuari)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values))



         

###########################################################################################################################################################
# CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             CONTROL             
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################
def formulariControl (usuari, idTravailleur):

    #conectar a la bd
    db= get_db()
    cursor = db.cursor()
        
    #operar en bd 
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    
    if idTravailleur == -1: #sense seleccio
        usuariSelect = ''
        travailleurTots = tablaTravailleurTots(cursor)
        
    elif idTravailleur == -2: #treballador en blanc
        usuariSelect = ''
        travailleurTots = ''
        
    else: #treballador select
        usuariSelect = tablaTravailleurSelect(cursor,idTravailleur)
        travailleurTots = ''
    
    #desconectar de la bd
    db.commit()
    db.close()

    #pasem les llistes al arxiu html
    values = {
             'idTravailleur': idTravailleur,
             'travailleurSelect': travailleurSelect,
             'usuariSelect': usuariSelect,
             'travailleurTots': travailleurTots,
             
              }
    return values 




# ACCIONS DEL FORMULARI
####################################
class UsuariTots (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
                #parametres
                idTravailleur = -1
            
                #obtenim valors per al html
                values = formulariControl(usuari, idTravailleur)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'control.html') 
                self.response.out.write(template.render(path, values))

            

class UsuariNou (webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):

                #parametres
                idTravailleur = -2
            
                #obtenim valors per al html
                values = formulariControl(usuari, idTravailleur)

                #imprimim el arxiu html
                path = os.path.join(os.path.dirname(__file__), 'control.html') 
                self.response.out.write(template.render(path, values))

            
class UsuariSelect (webapp2.RequestHandler):# mostra index.html
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTravailleur= novar(self.request.get('idTravailleur'))
            
            #parametres

            
            #obtenim valors per al html
            values = formulariControl(usuari, idTravailleur)

            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'control.html') 
            self.response.out.write(template.render(path, values))
            
class UsuariEdita (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            idTravailleur= novar(self.request.get('idTravailleur'))
            codeTravailleur = novar(self.request.get('codeTravailleur'))
            nomTravailleur = novar(self.request.get('nomTravailleur'))
            mail = novar(self.request.get('mail'))
            activite = novar(self.request.get('activite'))

            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('UPDATE TRAVAILLEUR SET codeTravailleur=%s, nomTravailleur=%s, mail=%s, activite=%s WHERE idTravailleur=%s', (codeTravailleur, nomTravailleur, mail, activite, idTravailleur))
            
            db.commit()
            db.close()
            
            #redirecciona
            self.redirect("/UsuariTots")

class UsuariCrea (webapp2.RequestHandler):# mostra index.html
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):
            
            #captura del html
            codeTravailleur = novar(self.request.get('codeTravailleur'))
            nomTravailleur = novar(self.request.get('nomTravailleur'))
            mail = novar(self.request.get('mail'))
            activite = novar(self.request.get('activite'))
            
            #accions sobre bd
            db= get_db()
            cursor = db.cursor()
            
            cursor.execute('INSERT INTO TRAVAILLEUR (codeTravailleur, nomTravailleur, mail, activite) VALUES (%s, %s, %s, %s)', (codeTravailleur, nomTravailleur, mail, activite))
            
            db.commit()
            db.close()

            #redirecciona
            self.redirect("/UsuariTots")

#--ELIMINA PASSAT PER LINK
class UsuariElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idTravailleur = novar(self.request.get('idTravailleur'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM TRAVAILLEUR WHERE idTravailleur=%s', (idTravailleur,))
            #tanca conexio
            db.commit()
            db.close()
            
            self.redirect("/UsuariTots")
            
###########################################################################################################################################################
# CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT        CLIENT
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariClient (usuari, idClient):
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idClient < 0:       #si es negatiu monta html preparat per a nou
        clientSelect = Client(idClient,'','','','','','','','','')
    else:                  #sino monta html amb seleccionat
        clientSelect = tablaClientSelect(cursor, idClient)

    clientTots = tablaClientTots(cursor)
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'clientSelect': clientSelect,
            'clientTots': clientTots,
            'travailleurSelect': travailleurSelect,
            }
    return values   

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaClientSelect(cursor, idClient):
    cursor.execute('SELECT idClient, codeClient, nomCommercial, nomSociete, cifClient, directionClient, villeClient, codePostalClient, paysClient, commentClient FROM CLIENT WHERE idClient=%s',(idClient,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Client(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) #Modificar si anyadim columna
    return lista

class Client:
    def __init__(self, idClient=0, codeClient='', nomCommercial='', nomSociete='', cifClient='', directionClient='', villeClient='', codePostalClient='', paysClient='', commentClient=''):
        self.idClient = idClient
        self.codeClient = codeClient
        self.nomCommercial = nomCommercial 
        self.nomSociete = nomSociete
        self.cifClient = cifClient
        self.directionClient = directionClient
        self.villeClient = villeClient 
        self.codePostalClient = codePostalClient
        self.paysClient = paysClient
        self.commentClient = commentClient

def tablaClientTots(cursor):
    cursor.execute('SELECT idClient, codeClient, nomCommercial, nomSociete, cifClient, directionClient, villeClient, codePostalClient, paysClient, commentClient FROM CLIENT ORDER BY nomCommercial')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Client(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])  #Modificar si anyadim columna
        indice=indice+1   
    return lista

# ACCIONS DEL FORMULARI
####################################

#MOSTRA FORMULARI DE FORMA INICIAL
class ClientInicial(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idClient = -1
            #obtenim valors per al html
            values = formulariClient(usuari,idClient)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 
            
class ClientNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idClient = -2
            #obtenim valors per al html
            values = formulariClient(usuari,idClient)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I CREA NOU
class ClientCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html
            codeClient = novar(self.request.get('codeClient'))
            nomCommercial = novar(self.request.get('nomCommercial')) 
            nomSociete = novar(self.request.get('nomSociete'))
            cifClient = novar(self.request.get('cifClient'))
            directionClient = novar(self.request.get('directionClient'))
            villeClient = novar(self.request.get('villeClient')) 
            codePostalClient = novar(self.request.get('codePostalClient'))
            paysClient = novar(self.request.get('paysClient'))
            commentClient = novar(self.request.get('commentClient'))
       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO CLIENT (codeClient, nomCommercial, nomSociete, cifClient, directionClient, villeClient, codePostalClient, paysClient, commentClient) VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)', (codeClient, nomCommercial, nomSociete, cifClient, directionClient, villeClient, codePostalClient, paysClient, commentClient))
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari
            idClient = -1
            #valors per al html
            values = formulariClient(usuari,idClient)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class ClientSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idClient = novar(self.request.get('idClient'))
        
            #valors per al html
            values = formulariClient(usuari,idClient)       
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class ClientEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idClient = novar(self.request.get('idClient'))
            codeClient = novar(self.request.get('codeClient'))
            nomCommercial = novar(self.request.get('nomCommercial')) 
            nomSociete = novar(self.request.get('nomSociete'))
            cifClient = novar(self.request.get('cifClient'))
            directionClient = novar(self.request.get('directionClient'))
            villeClient = novar(self.request.get('villeClient')) 
            codePostalClient = novar(self.request.get('codePostalClient'))
            paysClient = novar(self.request.get('paysClient'))
            commentClient = novar(self.request.get('commentClient'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE CLIENT SET codeClient=%s, nomCommercial=%s, nomSociete=%s, cifClient=%s, directionClient=%s, villeClient=%s, codePostalClient=%s, paysClient=%s, commentClient=%s WHERE idClient=%s', (codeClient, nomCommercial, nomSociete, cifClient, directionClient, villeClient, codePostalClient, paysClient, commentClient, idClient))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #valors per al html
            values = formulariClient(usuari,idClient)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class ClientElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idClient = novar(self.request.get('idClient'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM CLIENT WHERE idClient=%s', (idClient,))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari
            idClient = -1
            #valors per al html
            values = formulariClient(usuari,idClient)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Client.html') 
            self.response.out.write(template.render(path, values)) 

            

###########################################################################################################################################################
# DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER       DOSSIER
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariDossier (usuari, idDossier):
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idDossier < 0:       #si es negatiu monta html preparat per a nou
        dossierSelect = Dossier(idDossier,'','','','','','','','')
        profilDossier = Profil (-1,'','','')
    else:                  #sino monta html amb seleccionat
        dossierSelect = tablaDossierSelect(cursor, idDossier)
        profilDossier = tablaProfilDossier(cursor, idDossier)

    dossierTots = tablaDossierTots(cursor)
    clientTots = tablaClientTots(cursor)
    problemeTots = tablaProblemeTots(cursor)
    industrielTots = tablaIndustrielTots(cursor)
    interventionDossier = tablaInterventionDossier(cursor, idDossier)
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'dossierSelect': dossierSelect,
            'dossierTots': dossierTots,
            'clientTots': clientTots,
            'profilDossier': profilDossier,
            'problemeTots': problemeTots,
            'industrielTots': industrielTots,
            'interventionDossier': interventionDossier,
            'travailleurSelect': travailleurSelect
            }
    return values   

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaDossierSelect(cursor, idDossier):
    cursor.execute('SELECT idDossier, idClient, codeDossier, nomDossier, telDossier, commentDossier, unitMODef, unitMOADef, unitDepDef FROM DOSSIER WHERE idDossier=%s',(idDossier,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Dossier(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]) #Modificar si anyadim columna
    return lista

class Dossier:
    def __init__(self, idDossier=0, idClient=0, codeDossier='', nomDossier='', telDossier='', commentDossier='', unitMODef=0, unitMOADef=0, unitDepDef=0):
        self.idDossier = idDossier
        self.idClient = idClient
        self.codeDossier = codeDossier
        self.nomDossier = nomDossier
        self.telDossier = telDossier
        self.commentDossier = commentDossier
        self.unitMODef = unitMODef
        self.unitMOADef = unitMOADef  
        self.unitDepDef = unitDepDef

def tablaDossierTots(cursor):
    cursor.execute('SELECT idDossier, idClient, codeDossier, nomDossier, telDossier, commentDossier, unitMODef, unitMOADef, unitDepDef FROM DOSSIER ORDER BY nomDossier')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Dossier(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

def tablaProfilDossier(cursor, idDossier):
    cursor.execute('SELECT idProfil, idDossier, idProbleme, idIndustriel FROM PROFIL WHERE idDossier=%s',(idDossier,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Profil(i[0],i[1],i[2],i[3])  #Modificar si anyadim columna
        indice=indice+1 
    return lista 

class Profil:
    def __init__(self, idProfil=0, idDossier=0, idProbleme=0, idIndustriel=0):
        self.idProfil = idProfil
        self.idDossier = idDossier
        self.idProbleme = idProbleme
        self.idIndustriel = idIndustriel

def tablaProblemeTots(cursor):
    cursor.execute('SELECT idProbleme, probleme FROM PROBLEME ORDER BY probleme')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Probleme(i[0],i[1])  #Modificar si anyadim columna
        indice=indice+1   
    return lista

class Probleme:
    def __init__(self, idProbleme=0, probleme=''):
        self.idProbleme = idProbleme
        self.probleme = probleme

def tablaIndustrielTots(cursor):
    cursor.execute('SELECT idIndustriel, nomIndustriel, telIndustriel, mailIndustriel, contactIndustriel, commentIndustriel FROM INDUSTRIEL ORDER BY nomIndustriel')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Industriel(i[0],i[1],i[2],i[3],i[4],i[5])  #Modificar si anyadim columna
        indice=indice+1   
    return lista

class Industriel:
    def __init__(self, idIndustriel=0, nomIndustriel='', telIndustriel='', mailIndustriel='', contactIndustriel='', commentIndustriel=''):
        self.idIndustriel = idIndustriel
        self.nomIndustriel = nomIndustriel
        self.telIndustriel = telIndustriel 
        self.mailIndustriel = mailIndustriel
        self.contactIndustriel = contactIndustriel
        self.commentIndustriel = commentIndustriel

def tablaInterventionDossier(cursor, idDossier):
    cursor.execute('SELECT idIntervention, idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait FROM INTERVENTION WHERE idDossier=%s ORDER BY idIntervention DESC',(idDossier,))        
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dateEntree=dataFormat(i[5])
        dateLimite=dataFormat(i[6])
        dateFait=dataFormat(i[7]) 
        lista[indice] = Intervention(i[0],i[1],i[2],i[3],i[4],dateEntree,dateLimite,dateFait,i[8],i[9],i[10],i[11],i[12],i[13])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 


class Intervention:
    def __init__(self, idIntervention=0, idDossier=0, idSituation=0, numDi='', priorite='', dateEntree='', dateLimite='', dateFait='', demandeEs='', demandeFr='', travailFaitEs='', travailFaitFr='', garantie=0, mailFait=0):
        self.idIntervention = idIntervention
        self.idDossier = idDossier
        self.idSituation = idSituation
        self.numDi = numDi
        self.priorite = priorite
        self.dateEntree = dateEntree
        self.dateLimite = dateLimite
        self.dateFait = dateFait
        self.demandeEs = demandeEs
        self.demandeFr = demandeFr
        self.travailFaitEs = travailFaitEs
        self.travailFaitFr = travailFaitFr
        self.garantie = garantie
        self.mailFait = mailFait

# ACCIONS DEL FORMULARI
####################################

#MOSTRA FORMULARI DE FORMA INICIAL
class DossierInicial(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idDossier = -1
            #obtenim valors per al html
            values = formulariDossier(usuari, idDossier)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 
            
class DossierNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idDossier = -2
            #obtenim valors per al html
            values = formulariDossier(usuari, idDossier)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I CREA NOU
class DossierCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html
            idClient = novar(self.request.get('idClient'))
            codeDossier = novar(self.request.get('codeDossier'))
            nomDossier = novar(self.request.get('nomDossier')) 
            telDossier = novar(self.request.get('telDossier'))
            commentDossier = novar(self.request.get('commentDossier'))
            unitMODef = novar(self.request.get('unitMODef'))
            unitMOADef = novar(self.request.get('unitMOADef'))
            unitDepDef = novar(self.request.get('unitDepDef')) 
       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO DOSSIER (idClient, codeDossier, nomDossier, telDossier, commentDossier, unitMODef, unitMOADef, unitDepDef) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (idClient, codeDossier, nomDossier, telDossier, commentDossier, unitMODef, unitMOADef, unitDepDef))
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari
            idDossier = -1
            #valors per al html
            values = formulariDossier(usuari,idDossier)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class DossierSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idDossier = novar(self.request.get('idDossier'))
        
            #valors per al html
            values = formulariDossier(usuari, idDossier)       
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 

class DossierSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idDossier = novar(self.request.get('idDossier'))
        
            #valors per al html
            values = formulariDossier(usuari, idDossier)       
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class DossierEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idDossier = novar(self.request.get('idDossier'))
            idClient = novar(self.request.get('idClient'))
            codeDossier = novar(self.request.get('codeDossier'))
            nomDossier = novar(self.request.get('nomDossier')) 
            telDossier = novar(self.request.get('telDossier'))
            commentDossier = novar(self.request.get('commentDossier'))
            unitMODef = novar(self.request.get('unitMODef'))
            unitMOADef = novar(self.request.get('unitMOADef'))
            unitDepDef = novar(self.request.get('unitDepDef')) 

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE DOSSIER SET idClient=%s, codeDossier=%s, nomDossier=%s, telDossier=%s, commentDossier=%s, unitMODef=%s, unitMOADef=%s, unitDepDef=%s WHERE idDossier=%s', (idClient, codeDossier, nomDossier, telDossier, commentDossier, unitMODef, unitMOADef, unitDepDef, idDossier))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #valors per al html
            values = formulariDossier(usuari, idDossier)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class DossierElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idDossier = novar(self.request.get('idDossier'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM DOSSIER WHERE idDossier=%s', (idDossier,))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari
            idDossier = -1
            #valors per al html
            values = formulariDossier(usuari, idDossier)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Dossier.html') 
            self.response.out.write(template.render(path, values)) 

###########################################################################################################################################################
# INTERVENTION       INTERVENTION       INTERVENTION       INTERVENTION       INTERVENTION       INTERVENTION       INTERVENTION       INTERVENTION
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariIntervention (usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel):
    
    #dataHui
    valor = datetime.datetime.today()
    hui = valor.strftime('%Y-%m-%d')
    
    #conecta a base de datos
    db= get_db()
    cursor = db.cursor() 
        
    #tables per al html
    if idIntervention < 0:       #si es negatiu monta html preparat per a nou
        interventionSelect = Intervention(idIntervention,'','','','','','','','','','','','','')
        histoireIntervention = Histoire(-1,-1,-1,1,hui,'')
        tacheIntervention = Tache(-1,-1,-1,1,hui,'',0)
        travailIntervention = Travail(-1,-1,'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','')
        devisIntervention = Devis(-1,-1,'','')
        factureIntervention = Facture(-1,-1,'','','')
        proformeIntervention = Proforme(-1,-1,'','','')
        travailFiltro = tablaTravailFiltro(cursor, idDossier, idSituation, idProbleme, idIndustriel)
        profilTravail = Profil(-1,'','','') 
        industrielTravail = Industriel(-1,'','','','','')
        problemeDossier = Probleme(-1,'')
        
    
    else:                  #sino monta html amb seleccionat
        interventionSelect = tablaInterventionSelect(cursor, idIntervention)         
        histoireIntervention = tablaHistoireIntervention(cursor, idIntervention)
        tacheIntervention = tablaTacheIntervention(cursor, idIntervention)
        travailIntervention = tablaTravailIntervention(cursor, idIntervention)
        devisIntervention = tablaDevisIntervention(cursor, idIntervention)
        factureIntervention = tablaFactureIntervention(cursor, idIntervention)
        proformeIntervention = tablaProformeIntervention(cursor, idIntervention)
        travailFiltro = TravailFiltro('','','','','','','','','','','','','','', '')  #Modificar si anyadim columna
        profilTravail = tablaProfilTravail(cursor, idDossier, idProbleme)
        industrielTravail = tablaIndustrielTravail(cursor, idDossier, idProbleme)
        problemeDossier = tablaProblemeDossier(cursor,idDossier)
        

    
    
    dossierTots = tablaDossierTots(cursor)
    situationTots = tablaSituationTots(cursor)
    incidentTots = tablaIncidentTots(cursor)
    typeTacheTots = tablaTypeTacheTots(cursor)
    problemeTots = tablaProblemeTots(cursor)
    travailleurActiu = tablaTravailleurActiu(cursor)
    travailleurTots = tablaTravailleurTots(cursor)
    travailleurSelect = tablaTravailleurSelect(cursor, usuari)
    industrielTots = tablaIndustrielTots(cursor)
   
    #tanca conexio
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'interventionSelect': interventionSelect,
            'travailFiltro': travailFiltro,
            'dossierTots': dossierTots,
            'situationTots': situationTots,
            'histoireIntervention': histoireIntervention,
            'tacheIntervention': tacheIntervention,
            'travailIntervention': travailIntervention,
            'devisIntervention': devisIntervention,
            'factureIntervention': factureIntervention, 
            'proformeIntervention': proformeIntervention,         
            'problemeTots': problemeTots,
            'incidentTots': incidentTots,
            'typeTacheTots': typeTacheTots,
            'travailleurActiu': travailleurActiu,
            'travailleurTots': travailleurTots,
            'travailleurSelect': travailleurSelect,
            'profilTravail': profilTravail,
            'industrielTots': industrielTots,
            'industrielTravail': industrielTravail,
            'problemeDossier': problemeDossier,
            
            }
    return values  

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################

def tablaInterventionSelect(cursor, idIntervention):
    cursor.execute('SELECT idIntervention, idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        dataEntree=dataFormat(i[5])
        dataLimite=dataFormat(i[6])
        dataFait=dataFormat(i[7])         
        lista = Intervention(i[0],i[1],i[2],i[3],i[4],dataEntree,dataLimite,dataFait,i[8],i[9],i[10],i[11],i[12],i[13]) #Modificar si anyadim columna
    return lista


def tablaTravailFiltro(cursor, idDossier, idSituation, idProbleme, idIndustriel):
    if idDossier == -1:
        if idSituation == -1:
            if idProbleme == -1:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE it.mailFait=%s ORDER BY tr.idIntervention DESC LIMIT 100',(0,))    
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s ORDER BY it.idIntervention DESC',(0, idIndustriel))                   
            else:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idProbleme=%s ORDER BY it.idIntervention DESC',(0, idProbleme)) 
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s  AND tr.idProbleme=%s ORDER BY it.idIntervention DESC',(0, idIndustriel, idProbleme))                
        else:
            if idProbleme == -1:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idSituation=%s ORDER BY it.idIntervention DESC',(0, idSituation))               
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s  AND it.idSituation=%s ORDER BY it.idIntervention DESC',(0, idIndustriel, idSituation)) 
            else:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idSituation=%s  AND tr.idProbleme=%s ORDER BY it.idIntervention DESC',(0, idSituation, idProbleme))            
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idSituation=%s  AND tr.idProbleme=%s AND tr.idIndustriel ORDER BY it.idIntervention DESC',(0, idSituation, idProbleme, idIndustriel)) 
            
    else:
        if idSituation == -1:
            if idProbleme == -1:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idDossier))    
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idIndustriel, idDossier))                   
            else:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idProbleme=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idProbleme, idDossier)) 
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s  AND tr.idProbleme=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idIndustriel, idProbleme, idDossier))                
        else:
            if idProbleme == -1:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s  AND it.idSituation=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idSituation, idDossier))               
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND tr.idIndustriel=%s  AND it.idSituation=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idIndustriel, idSituation, idDossier)) 
            else:
                if idIndustriel == -1:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idSituation=%s  AND tr.idProbleme=%s AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idSituation, idProbleme, idDossier))            
                else:
                    cursor.execute('SELECT it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree, it.dateLimite, it.dateFait, it.garantie, it.mailFait, tr.idTravail, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail FROM INTERVENTION it INNER JOIN TRAVAIL tr ON it.idIntervention = tr.idIntervention WHERE tr.ok >= %s AND it.idSituation=%s  AND tr.idProbleme=%s AND tr.idIndustriel AND it.idDossier=%s ORDER BY it.idIntervention DESC',(0, idSituation, idProbleme, idIndustriel, idDossier)) 
                    
           
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista  
        dateEntree=dataFormat(i[5])  
        dateLimite=dataFormat(i[6])
        dateFait=dataFormat(i[7])
        
        lista[indice] = TravailFiltro(i[0],i[1],i[2],i[3],i[4],dateEntree,dateLimite,dateFait,i[8],i[9],i[10],i[11],i[12],i[13], i[14])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class TravailFiltro:
    def __init__(self, idIntervention=0, idDossier=0, idSituation=0, numDi='', priorite='', dateEntree='', dateLimite='', dateFait='', garantie=0, mailFait=0, idTravail=0, idProbleme=0, idIndustriel=0, coutIndustriel='', nomTravail=''):
        self.idIntervention = idIntervention
        self.idDossier = idDossier
        self.idSituation = idSituation
        self.numDi = numDi
        self.priorite = priorite
        self.dateEntree = dateEntree
        self.dateLimite = dateLimite
        self.dateFait = dateFait
        self.garantie = garantie
        self.mailFait = mailFait
        self.idTravail = idTravail
        self.idProbleme = idProbleme
        self.idIndustriel = idIndustriel
        self.coutIndustriel = coutIndustriel
        self.nomTravail = nomTravail
        

def tablaSituationTots(cursor):
    cursor.execute('SELECT idSituation, situation, ordre FROM SITUATION ORDER BY ordre')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Situation(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class Situation:
    def __init__(self, idSituation=0, situation=0, ordre=0):
        self.idSituation = idSituation
        self.situation = situation
        self.ordre = ordre

def tablaProfilTravail(cursor, idDossier, idProbleme):
    cursor.execute('SELECT idProfil, idDossier, idProbleme, idIndustriel FROM PROFIL WHERE idDossier=%s AND idProbleme=%s',(idDossier, idProbleme))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Profil(i[0],i[1],i[2],i[3])  #Modificar si anyadim columna
        indice=indice+1 
    return lista 


def tablaIndustrielTravail(cursor, idDossier, idProbleme):
    cursor.execute('SELECT id.idIndustriel, id.nomIndustriel, id.telIndustriel, id.mailIndustriel, id.contactIndustriel, id.commentIndustriel FROM INDUSTRIEL id INNER JOIN PROFIL pr ON id.idIndustriel=pr.idIndustriel WHERE pr.idDossier=%s AND pr.idProbleme=%s',(idDossier, idProbleme))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Industriel(i[0],i[1],i[2],i[3],i[4],i[5])  #Modificar si anyadim columna
        indice=indice+1 
    return lista 

def tablaProblemeDossier(cursor, idDossier):
    cursor.execute('SELECT pb.idProbleme, pb.probleme FROM PROBLEME pb INNER JOIN PROFIL pr ON pb.idProbleme=pr.idProbleme WHERE pr.idDossier=%s',(idDossier,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Probleme(i[0],i[1])  #Modificar si anyadim columna
        indice=indice+1 
    return lista 



def tablaTravailleurActiu(cursor):
    activite = 1
    cursor.execute('SELECT idTravailleur, codeTravailleur, nomTravailleur, activite FROM TRAVAILLEUR WHERE activite=%s ORDER BY idTravailleur',(activite,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Travailleur(i[0],i[1],i[2],i[3])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

        

def tablaHistoireIntervention(cursor, idIntervention):
    cursor.execute('SELECT idHistoire, idIntervention, idTravailleur, idIncident, dateHistoire, histoire FROM HISTOIRE WHERE idIntervention=%s ORDER BY dateHistoire DESC, idHistoire DESC', (idIntervention,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataHistoire=dataFormat(i[4])
        lista[indice] = Histoire(i[0],i[1],i[2],i[3],dataHistoire,i[5]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class Histoire:
    def __init__(self, idHistoire=0, idIntervention=0, idTravailleur=0, idIncident=0, dateHistoire='', histoire=''):
        self.idHistoire = idHistoire
        self.idIntervention = idIntervention
        self.idTravailleur = idTravailleur
        self.idIncident = idIncident
        self.dateHistoire = dateHistoire
        self.histoire = histoire


def tablaTacheIntervention(cursor, idIntervention):
    ok=0
    cursor.execute('SELECT idTache, idIntervention, idTravailleur, idTypeTache, dateTache, commentTache, ok FROM TACHE WHERE idIntervention=%s AND ok=%s ORDER BY dateTache DESC',(idIntervention, ok))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataTache=dataFormat(i[4])       
        lista[indice] = Tache(i[0],i[1],i[2],i[3],dataTache,i[5], i[6]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class Tache:
    def __init__(self, idTache=0, idIntervention=0, idTravailleur=0, idTypeTache=0, dateTache='', commentTache='', ok=''):
        self.idTache = idTache
        self.idIntervention = idIntervention
        self.idTravailleur = idTravailleur
        self.idTypeTache = idTypeTache
        self.dateTache = dateTache
        self.commentTache = commentTache
        self.ok = ok


def tablaTravailIntervention(cursor, idIntervention):
    cursor.execute('SELECT idTravail, idIntervention, idProbleme, idIndustriel, coutIndustriel, nomTravail, description, materiel1, unite1, unitaire1, quantite1, materiel2, unite2, unitaire2, quantite2, materiel3, unite3, unitaire3, quantite3, materiel4, unite4, unitaire4, quantite4, materiel5, unite5, unitaire5, quantite5, unitaireMO, quantiteMO, unitaireMOA, quantiteMOA, unitaireDep, quantiteDep, ok FROM TRAVAIL WHERE idIntervention=%s',(idIntervention,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista      
        lista[indice] = Travail(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28],i[29],i[30],i[31],i[32],i[33]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class Travail:
    def __init__(self, idTravail=0, idIntervention=0, idProbleme=0, idIndustriel=0, coutIndustriel='', nomTravail='', description='', materiel1='', unite1='', unitaire1='', quantite1='', materiel2='', unite2='', unitaire2='', quantite2='', materiel3='', unite3='', unitaire3='', quantite3='', materiel4='', unite4='', unitaire4='', quantite4='', materiel5='', unite5='', unitaire5='', quantite5='', unitaireMO='', quantiteMO='', unitaireMOA='', quantiteMOA='', unitaireDep='', quantiteDep='', ok=''):
        self.idTravail = idTravail
        self.idIntervention = idIntervention
        self.idProbleme = idProbleme
        self.idIndustriel = idIndustriel
        self.coutIndustriel = coutIndustriel
        self.nomTravail = nomTravail
        self.description = description
        self.materiel1 = materiel1
        self.unite1 = unite1
        self.unitaire1 = unitaire1
        self.quantite1 = quantite1
        self.materiel2 = materiel2
        self.unite2 = unite2
        self.unitaire2 = unitaire2
        self.quantite2 = quantite2
        self.materiel3 = materiel3
        self.unite3 = unite3
        self.unitaire3 = unitaire3
        self.quantite3  = quantite3
        self.materiel4 = materiel4
        self.unite4 = unite4
        self.unitaire4 = unitaire4
        self.quantite4  = quantite4
        self.materiel5 = materiel5
        self.unite5 = unite5
        self.unitaire5 = unitaire5
        self.quantite5  = quantite5
        self.unitaireMO = unitaireMO
        self.quantiteMO = quantiteMO
        self.unitaireMOA = unitaireMOA
        self.quantiteMOA = quantiteMOA
        self.unitaireDep = unitaireDep
        self.quantiteDep = quantiteDep
        self.ok = ok


def tablaDevisIntervention(cursor, idIntervention):
    cursor.execute('SELECT idDevis, idIntervention, dateDevis, nombreDevis FROM DEVIS WHERE idIntervention=%s',(idIntervention,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[2])       
        lista[indice] = Devis(i[0],i[1],data,i[3]) #Modificar si anyadim columna
        indice=indice+1   
    return lista 



def tablaFactureIntervention(cursor, idIntervention):
    cursor.execute('SELECT idFacture, idIntervention, dateFacture, nombreFacture, datePaye FROM FACTURE WHERE idIntervention=%s',(idIntervention,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista[indice] = Facture(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

def tablaProformeIntervention(cursor, idIntervention):
    cursor.execute('SELECT idProforme, idIntervention, dateProforme, nombreProforme, datePaye FROM PROFORME WHERE idIntervention=%s',(idIntervention,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista[indice] = Proforme(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
        indice=indice+1   
    return lista 


       
def tablaIncidentTots(cursor):
    cursor.execute('SELECT idIncident, incident FROM INCIDENT ORDER BY incident')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Incident(i[0],i[1])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class Incident:
    def __init__(self, idIncident=0, incident=0):
        self.idIncident = idIncident
        self.incident = incident
        
def tablaTypeTacheTots(cursor):
    cursor.execute('SELECT idTypeTache, codeTypeTache, typeTache FROM TYPETACHE ORDER BY codeTypeTache')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = TypeTache(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class TypeTache:
    def __init__(self, idTypeTache=0, codeTypeTache='', typeTache=''):
        self.idTypeTache = idTypeTache
        self.codeTypeTache = codeTypeTache
        self.typeTache = typeTache

        


# ACCIONS DEL FORMULARI
####################################

#MOSTRA FORMULARI DE FORMA INICIAL
class InterventionInicial(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #pasem parametres
            idIntervention = -1 
            idDossier = -1          #filtro
            idSituation = -1        #filtro
            idProbleme = -1         #filtro
            idIndustriel = -1       #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values)) 
            
class InterventionNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idIntervention = -2 
            idDossier = -1          #filtro
            idSituation = -1        #filtro
            idProbleme = -1         #filtro
            idIndustriel = -1       #filtro
            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class InterventionCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #captura camps del html
            idDossier = novar(self.request.get('idDossier'))
            idSituation = novar(self.request.get('idSituation'))
            numDi = novar(self.request.get('numDi')) 
            priorite = novar(self.request.get('priorite')) 
            dateEntree = novar(self.request.get('dateEntree'))
            dateLimite = novar(self.request.get('dateLimite'))
            dateFait = novar(self.request.get('dateFait'))
            demandeEs = novar(self.request.get('demandeEs')) 
            demandeFr = novar(self.request.get('demandeFr')) 
            travailFaitEs = novar(self.request.get('travailFaitEs')) 
            travailFaitFr = novar(self.request.get('travailFaitFr')) 
            garantie = novar(self.request.get('garantie')) 
            mailFait = novar(self.request.get('mailFait'))   

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO INTERVENTION (idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait))
            #obtenir el id de la fila que hem insertat
            cursor.execute('SELECT idIntervention FROM INTERVENTION ORDER BY idIntervention DESC LIMIT 0,1')
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanca conexio
            db.commit()
            db.close()

        
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class InterventionSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del link html
            idIntervention = novar(self.request.get('idIntervention'))
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class InterventionSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del link html
            idIntervention = novar(self.request.get('idIntervention'))
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

#--CAPTURA DADES DEL HTML I EDITA
class InterventionEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):               
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idDossier = novar(self.request.get('idDossier'))
            idSituation = novar(self.request.get('idSituation'))
            numDi = novar(self.request.get('numDi')) 
            priorite = novar(self.request.get('priorite'))
            dateEntree = novar(self.request.get('dateEntree'))
            dateLimite = novar(self.request.get('dateLimite'))
            dateFait = novar(self.request.get('dateFait'))
            demandeEs = novar(self.request.get('demandeEs')) 
            demandeFr = novar(self.request.get('demandeFr')) 
            travailFaitEs = novar(self.request.get('travailFaitEs')) 
            travailFaitFr = novar(self.request.get('travailFaitFr')) 
            garantie = novar(self.request.get('garantie')) 
            mailFait = novar(self.request.get('mailFait'))   

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE INTERVENTION SET idDossier=%s, idSituation=%s, numDi=%s, priorite=%s, dateEntree=%s, dateLimite=%s, dateFait=%s, demandeEs=%s, demandeFr=%s, travailFaitEs=%s, travailFaitFr=%s, garantie=%s, mailFait=%s WHERE idIntervention=%s', (idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait, idIntervention))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            # parametres
            idIntervention = idIntervention
            idDossier = idDossier      #filtro
            idSituation =  -1   #filtro
            idProbleme = -1     #filtro
            idIndustriel = -1   #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

#--ELIMINA PASSAT PER LINK
class InterventionElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #rep identificador del boto html
            idIntervention = novar(self.request.get('idIntervention'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM INTERVENTION WHERE idIntervention =%s', (idIntervention,))
            
            #tanca conexio
            db.commit()
            db.close()
            
            # parametres
            idIntervention = -1
            idDossier = -1      #filtro
            idSituation =  -1   #filtro
            idProbleme = -1     #filtro
            idIndustriel = -1   #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

#--CAPTURA DADES DEL HTML I FILTRA
class InterventionTravailFiltro(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):             
            #captura camps del html
            idDossier = novar(self.request.get('idDossier'))
            idSituation = novar(self.request.get('idSituation'))
            idProbleme = novar(self.request.get('idProbleme')) 
            idIndustriel = novar(self.request.get('idIndustriel'))
            idDossier=int(idDossier)
            idSituation=int(idSituation)
            idProbleme=int(idProbleme)
            idIndustriel=int(idIndustriel)

            # parametres
            idIntervention = -1
            idDossier = idDossier      #filtro
            idSituation =  idSituation   #filtro
            idProbleme = idProbleme     #filtro
            idIndustriel = idIndustriel   #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))
            
###########################################################################################################################################################
# INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL      INDUSTRIEL
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariIndustriel (usuari, idIndustriel):
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idIndustriel < 0:       #si es negatiu monta html preparat per a nou
        industrielSelect = Industriel(idIndustriel,'','','','','')
        profilIndustriel = Profil(-1,'','','')
    else:                  #sino monta html amb seleccionat
        industrielSelect = tablaIndustrielSelect(cursor, idIndustriel)
        profilIndustriel = tablaProfilIndustriel(cursor, idIndustriel)

    industrielTots = tablaIndustrielTots(cursor)
    dossierTots = tablaDossierTots(cursor)
    problemeTots = tablaProblemeTots(cursor)
    travailleurSelect = tablaTravailleurSelect(cursor, usuari)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'industrielSelect': industrielSelect,
            'profilIndustriel': profilIndustriel,
            'industrielTots': industrielTots,
            'dossierTots': dossierTots,
            'problemeTots': problemeTots,
            'travailleurSelect': travailleurSelect,
            }
    return values   

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaIndustrielSelect(cursor, idIndustriel):
    cursor.execute('SELECT idIndustriel, nomIndustriel, telIndustriel, mailIndustriel, contactIndustriel, commentIndustriel FROM INDUSTRIEL WHERE idIndustriel=%s',(idIndustriel,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Industriel(i[0],i[1],i[2],i[3],i[4],i[5]) #Modificar si anyadim columna
    return lista


def tablaProfilIndustriel(cursor, idIndustriel):
    cursor.execute('SELECT idProfil, idDossier, idProbleme, idIndustriel FROM PROFIL WHERE idIndustriel=%s',(idIndustriel,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        lista[indice] = Profil(i[0],i[1],i[2],i[3])  #Modificar si anyadim columna
        indice=indice+1   
    return lista



# ACCIONS DEL FORMULARI
####################################

#MOSTRA FORMULARI DE FORMA INICIAL
class IndustrielInicial(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idIndustriel = -1
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 
            
class IndustrielNou(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):       
            #pasem parametre
            idIndustriel = -2
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I CREA NOU
class IndustrielCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html
            nomIndustriel = novar(self.request.get('nomIndustriel'))
            telIndustriel = novar(self.request.get('telIndustriel'))
            mailIndustriel = novar(self.request.get('mailIndustriel')) 
            contactIndustriel = novar(self.request.get('contactIndustriel'))
            commentIndustriel = novar(self.request.get('commentIndustriel'))
       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO INDUSTRIEL (nomIndustriel, telIndustriel, mailIndustriel, contactIndustriel, commentIndustriel) VALUES (%s, %s, %s, %s, %s)', (nomIndustriel, telIndustriel, mailIndustriel, contactIndustriel, commentIndustriel))
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #pasem parametre
            idIndustriel = -1
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class IndustrielSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idIndustriel = novar(self.request.get('idIndustriel'))
        
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 
            

class IndustrielSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):                 
            #rep identificador del link html
            idIndustriel = novar(self.request.get('idIndustriel'))
        
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I EDITA
class IndustrielEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idIndustriel = novar(self.request.get('idIndustriel'))
            nomIndustriel = novar(self.request.get('nomIndustriel'))
            telIndustriel = novar(self.request.get('telIndustriel')) 
            mailIndustriel = novar(self.request.get('mailIndustriel'))
            contactIndustriel = novar(self.request.get('contactIndustriel'))
            commentIndustriel = novar(self.request.get('commentIndustriel'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE INDUSTRIEL SET nomIndustriel=%s, telIndustriel=%s, mailIndustriel=%s, contactIndustriel=%s, commentIndustriel=%s WHERE idIndustriel=%s', (nomIndustriel, telIndustriel, mailIndustriel, contactIndustriel, commentIndustriel, idIndustriel))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari

            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class IndustrielElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idIndustriel = novar(self.request.get('idIndustriel'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM INDUSTRIEL WHERE idIndustriel=%s', (idIndustriel,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametre
            idIndustriel = -1
            #obtenim valors per al html
            values = formulariIndustriel(usuari, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Industriel.html') 
            self.response.out.write(template.render(path, values)) 



###########################################################################################################################################################
# PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL       PROFIL
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariProfil (usuari, idProfil, idDossier, idIndustriel):
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idProfil < 0:       #si es negatiu monta html preparat per a nou
        profilSelect = Profil(idProfil,idDossier,'',idIndustriel)
    else:                  #sino monta html amb seleccionat
        profilSelect = tablaProfilSelect(cursor, idProfil)

    dossierTots = tablaDossierTots(cursor)
    problemeTots = tablaProblemeTots(cursor)
    industrielTots = tablaIndustrielTots(cursor)
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'profilSelect': profilSelect,
            'dossierTots': dossierTots,
            'problemeTots': problemeTots,
            'industrielTots': industrielTots,
            'travailleurSelect': travailleurSelect
            }
    return values   

def tablaProfilSelect(cursor, idProfil):
    cursor.execute('SELECT idProfil, idDossier, idProbleme, idIndustriel FROM PROFIL WHERE idProfil=%s',(idProfil,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        lista = Profil(i[0],i[1],i[2],i[3]) #Modificar si anyadim columna
    return lista

class ProfilNouDossier(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idDossier = novar(self.request.get('idDossier'))
            idDossier = int(idDossier)
            
            #pasem parametre
            idProfil = -2
            idIndustriel = -1
            
            #obtenim valors per al html
            values = formulariProfil(usuari, idProfil, idDossier, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Profil.html') 
            self.response.out.write(template.render(path, values)) 

class ProfilNouIndustriel(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIndustriel = novar(self.request.get('idIndustriel'))
            idIndustriel = int(idIndustriel)
            
            #pasem parametre
            idProfil = -2
            idDossier = -1
            
            #obtenim valors per al html
            values = formulariProfil(usuari, idProfil, idDossier, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Profil.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I CREA NOU
class ProfilCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idDossier = novar(self.request.get('idDossier'))
            idProbleme = novar(self.request.get('idProbleme')) 
            idIndustriel = novar(self.request.get('idIndustriel'))

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO PROFIL (idDossier, idProbleme, idIndustriel) VALUES (%s, %s, %s)', (idDossier, idProbleme, idIndustriel))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idProfil FROM PROFIL ORDER BY idProfil DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idProfil = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari
            idDossier = -1
            idIndustriel=-1
            
            #obtenim valors per al html
            values = formulariProfil(usuari, idProfil, idDossier, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Profil.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class ProfilSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idProfil = novar(self.request.get('idProfil'))
        
            #parametres per a funcio principal del formulari
            idDossier = -1
            idIndustriel=-1
            
            #obtenim valors per al html
            values = formulariProfil(usuari, idProfil, idDossier, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Profil.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class ProfilEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idProfil = novar(self.request.get('idProfil'))
            idDossier = novar(self.request.get('idDossier'))
            idProbleme = novar(self.request.get('idProbleme'))
            idIndustriel = novar(self.request.get('idIndustriel'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE PROFIL SET idDossier=%s, idProbleme=%s, idIndustriel=%s WHERE idProfil=%s', (idDossier, idProbleme, idIndustriel, idProfil))
            #tanca conexio
            db.commit()
            db.close()
            
            #parametres per a funcio principal del formulari
            idDossier = -1
            idIndustriel=-1
            
            #obtenim valors per al html
            values = formulariProfil(usuari, idProfil, idDossier, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Profil.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class ProfilElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idProfil = novar(self.request.get('idProfil'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #elimina de la tabla , fila corresponent al id seleccionat
            cursor.execute('DELETE FROM PROFIL WHERE idProfil=%s', (idProfil,))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariInicio(usuari)
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'index.html') 
            self.response.out.write(template.render(path, values))
            
###########################################################################################################################################################
# HISTOIRE     HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE      HISTOIRE
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariHistoire (usuari, idHistoire, idIntervention):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')
    
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idHistoire < 0:       #si es negatiu monta html preparat per a nou
        dateHistoire=dataHui
        histoireSelect = Histoire(idHistoire,idIntervention,'','',dateHistoire,'')
    else:                  #sino monta html amb seleccionat
        histoireSelect = tablaHistoireSelect(cursor, idHistoire)

    incidentTots = tablaIncidentTots(cursor)
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    travailleurTots=tablaTravailleurTots(cursor)
    travailleurAct=tablaTravailleurAct(cursor)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'histoireSelect': histoireSelect,
            'incidentTots': incidentTots,
            'travailleurSelect': travailleurSelect,
            'travailleurTots': travailleurTots,
            'travailleurAct': travailleurAct,
            'idIntervention': idIntervention,
            }
    return values   

def tablaHistoireSelect(cursor, idHistoire):
    cursor.execute('SELECT idHistoire, idIntervention, idTravailleur, idIncident, dateHistoire, histoire FROM HISTOIRE WHERE idHistoire=%s',(idHistoire,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        dataHistoire=dataFormat(i[4])       
        lista = Histoire(i[0],i[1],i[2],i[3],dataHistoire,i[5]) #Modificar si anyadim columna
    return lista



class HistoireNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idHistoire = -2
            
            #obtenim valors per al html
            values = formulariHistoire(usuari, idHistoire, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Histoire.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class HistoireCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idTravailleur = novar(self.request.get('idTravailleur'))
            idIncident = novar(self.request.get('idIncident')) 
            dateHistoire = novar(self.request.get('dateHistoire'))
            histoire = novar(self.request.get('histoire'))

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO HISTOIRE (idIntervention, idTravailleur, idIncident, dateHistoire, histoire) VALUES (%s, %s, %s, %s, %s)', (idIntervention, idTravailleur, idIncident, dateHistoire, histoire))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idHistoire FROM HISTOIRE ORDER BY idHistoire DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idHistoire = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariHistoire(usuari, idHistoire, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Histoire.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class HistoireSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idHistoire = novar(self.request.get('idHistoire'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM HISTOIRE WHERE idHistoire=%s', (idHistoire,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariHistoire(usuari, idHistoire, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Histoire.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class HistoireEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idHistoire = novar(self.request.get('idHistoire'))
            idIntervention = novar(self.request.get('idIntervention'))
            idTravailleur = novar(self.request.get('idTravailleur'))
            idIncident = novar(self.request.get('idIncident'))
            dateHistoire = novar(self.request.get('dateHistoire')) 
            histoire = novar(self.request.get('histoire'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE HISTOIRE SET idIntervention=%s, idTravailleur=%s, idIncident=%s, dateHistoire=%s, histoire=%s WHERE idHistoire=%s', (idIntervention, idTravailleur, idIncident, dateHistoire, histoire, idHistoire))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariHistoire(usuari, idHistoire, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Histoire.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class HistoireElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idHistoire = novar(self.request.get('idHistoire'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM HISTOIRE WHERE idHistoire=%s', (idHistoire,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM HISTOIRE WHERE idHistoire=%s', (idHistoire,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))
            
###########################################################################################################################################################
# TACHE     TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE      TACHE 
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariTache (usuari, idTache, idIntervention):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idTache < 0:       #si es negatiu monta html preparat per a nou
        dateTache=dataHui
        tacheSelect = Tache(idTache,idIntervention,'','',dateTache,'','')
    else:                  #sino monta html amb seleccionat
        tacheSelect = tablaTacheSelect(cursor, idTache)

    typeTacheTots = tablaTypeTacheTots(cursor)
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    travailleurTots=tablaTravailleurTots(cursor)
    travailleurAct=tablaTravailleurAct(cursor)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'tacheSelect': tacheSelect,
            'typeTacheTots': typeTacheTots,
            'travailleurSelect': travailleurSelect,
            'travailleurTots': travailleurTots,
            'travailleurAct': travailleurAct,
            'idIntervention': idIntervention,
            }
    return values   

def tablaTacheSelect(cursor, idTache):
    cursor.execute('SELECT idTache, idIntervention, idTravailleur, idTypeTache, dateTache, commentTache, ok FROM TACHE WHERE idTache=%s',(idTache,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        dateTache=dataFormat(i[4])       
        lista = Tache(i[0],i[1],i[2],i[3],dateTache,i[5],i[6]) #Modificar si anyadim columna
    return lista



class TacheNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idTache = -2
            
            #obtenim valors per al html
            values = formulariTache(usuari, idTache, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Tache.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class TacheCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idTravailleur = novar(self.request.get('idTravailleur'))
            idTypeTache = novar(self.request.get('idTypeTache')) 
            dateTache = novar(self.request.get('dateTache'))
            commentTache = novar(self.request.get('commentTache'))
            ok = 0

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO TACHE (idIntervention, idTravailleur, idTypeTache, dateTache, commentTache, ok) VALUES (%s, %s, %s, %s, %s, %s)', (idIntervention, idTravailleur, idTypeTache, dateTache, commentTache, ok))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idTache FROM TACHE ORDER BY idTache DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTache = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariTache(usuari, idTache, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Tache.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class TacheSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idTache = novar(self.request.get('idTache'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM TACHE WHERE idTache=%s', (idTache,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariTache(usuari, idTache, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Tache.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class TacheEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idTache = novar(self.request.get('idTache'))
            idIntervention = novar(self.request.get('idIntervention'))
            idTravailleur = novar(self.request.get('idTravailleur'))
            idTypeTache = novar(self.request.get('idTypeTache'))
            dateTache = novar(self.request.get('dateTache')) 
            commentTache = novar(self.request.get('commentTache'))
            ok = self.request.get('ok')
            if ok=='1':
                ok=int(ok)
            else:
                ok=0
                
                

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE TACHE SET idIntervention=%s, idTravailleur=%s, idTypeTache=%s, dateTache=%s, commentTache=%s, ok=%s WHERE idTache=%s', (idIntervention, idTravailleur, idTypeTache, dateTache, commentTache, ok, idTache))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariTache(usuari, idTache, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Tache.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class TacheElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idTache = novar(self.request.get('idTache'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM TACHE WHERE idTache=%s', (idTache,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM TACHE WHERE idTache=%s', (idTache,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

###########################################################################################################################################################
# TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL       TRAVAIL
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariTravail (usuari, idTravail, idIntervention, idProbleme):
    

    #accions sobre bd
    db= get_db()
    cursor = db.cursor() 

    cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
    dato = cursor.fetchall()
    idDossier = dato[0][0]       
        
    #tables per al html
    if idTravail < 0:       #si es negatiu monta html preparat per a nou
        cursor.execute('SELECT unitMODef, unitMOADef, unitDepDef FROM DOSSIER WHERE idDossier=%s',(idDossier,))
        dato = cursor.fetchall()
        unitMODef = dato[0][0]
        unitMOADef = dato[0][1]
        unitDepDef = dato[0][2]
        travailSelect = Travail(idTravail,idIntervention,idProbleme,'','','','','','','','','','','','','','','','','','','','','','','','', unitMODef,'',unitMOADef,'',unitDepDef,'','')
                  
    else:                  #sino monta html amb seleccionat
        travailSelect = tablaTravailSelect(cursor, idTravail)
               
    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    industrielTravail = tablaIndustrielTravail(cursor, idDossier, idProbleme)
    problemeDossier = tablaProblemeDossier(cursor, idDossier)
    problemeTots = tablaProblemeTots(cursor)
    industrielTots = tablaIndustrielTots(cursor)

   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'travailSelect': travailSelect,
            'problemeTots': problemeTots,
            'industrielTots': industrielTots,
            'travailleurSelect': travailleurSelect,
            'idIntervention': idIntervention,
            'industrielTravail': industrielTravail,
            'problemeDossier': problemeDossier
            }
    return values   

def tablaTravailSelect(cursor, idTravail):
    cursor.execute('SELECT idTravail, idIntervention, idProbleme, idIndustriel, coutIndustriel, nomTravail, description, materiel1, unite1, unitaire1, quantite1, materiel2, unite2, unitaire2, quantite2, materiel3, unite3, unitaire3, quantite3, materiel4, unite4, unitaire4, quantite4, materiel5, unite5, unitaire5, quantite5, unitaireMO, quantiteMO, unitaireMOA, quantiteMOA, unitaireDep, quantiteDep, ok  FROM TRAVAIL WHERE idTravail=%s',(idTravail,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista      
        lista = Travail(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21],i[22],i[23],i[24],i[25],i[26],i[27],i[28],i[29],i[30],i[31],i[32],i[33]) #Modificar si anyadim columna
    return lista



class TravailInicial(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idTravail = -1
            idProbleme = -1
            
            #obtenim valors per al html
            values = formulariTravail(usuari, idTravail, idIntervention, idProbleme)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Travail.html') 
            self.response.out.write(template.render(path, values)) 



class TravailNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            idProbleme = novar(self.request.get('idProbleme'))
            idProbleme = int(idProbleme)
            
            #pasem parametre
            idTravail = -2
            
            #obtenim valors per al html
            values = formulariTravail(usuari, idTravail, idIntervention, idProbleme)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Travail.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class TravailCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idProbleme = novar(self.request.get('idProbleme'))
            idIndustriel = novar(self.request.get('idIndustriel'))
            coutIndustriel = self.request.get('coutIndustriel')
            nomTravail = novar(self.request.get('nomTravail'))
            description = novar(self.request.get('description'))
            materiel1 = novar(self.request.get('materiel1'))
            unite1 = novar(self.request.get('unite1'))
            unitaire1 = self.request.get('unitaire1')
            quantite1 = self.request.get('quantite1')
            materiel2 = novar(self.request.get('materiel2'))
            unite2 = novar(self.request.get('unite2'))
            unitaire2 = self.request.get('unitaire2')
            quantite2 = self.request.get('quantite2')
            materiel3 = novar(self.request.get('materiel3'))
            unite3 = novar(self.request.get('unite3'))
            unitaire3 = self.request.get('unitaire3')
            quantite3 = self.request.get('quantite3')
            materiel4 = novar(self.request.get('materiel4'))
            unite4 = novar(self.request.get('unite4'))
            unitaire4 = self.request.get('unitaire4')
            quantite4 = self.request.get('quantite4')
            materiel5 = novar(self.request.get('materiel5'))
            unite5 = novar(self.request.get('unite5'))
            unitaire5 = self.request.get('unitaire5')
            quantite5 = self.request.get('quantite5')
            unitaireMO = self.request.get('unitaireMO')
            quantiteMO = self.request.get('quantiteMO')
            unitaireMOA = self.request.get('unitaireMOA')
            quantiteMOA = self.request.get('quantiteMOA')
            unitaireDep = self.request.get('unitaireDep')
            quantiteDep = self.request.get('quantiteDep')
            ok = 0

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO TRAVAIL (idIntervention, idProbleme, idIndustriel, coutIndustriel, nomTravail, description, materiel1, unite1, unitaire1, quantite1, materiel2, unite2, unitaire2, quantite2, materiel3, unite3, unitaire3, quantite3, materiel4, unite4, unitaire4, quantite4, materiel5, unite5, unitaire5, quantite5, unitaireMO, quantiteMO, unitaireMOA, quantiteMOA, unitaireDep, quantiteDep, ok) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (idIntervention, idProbleme, idIndustriel, coutIndustriel, nomTravail, description, materiel1, unite1, unitaire1, quantite1, materiel2, unite2, unitaire2, quantite2, materiel3, unite3, unitaire3, quantite3, materiel4, unite4, unitaire4, quantite4, materiel5, unite5, unitaire5, quantite5, unitaireMO, quantiteMO, unitaireMOA, quantiteMOA, unitaireDep, quantiteDep, ok))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idTravail FROM TRAVAIL ORDER BY idTravail DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idTravail = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariTravail(usuari, idTravail, idIntervention, idProbleme)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Travail.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class TravailSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idTravail = novar(self.request.get('idTravail'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention, idProbleme FROM TRAVAIL WHERE idTravail=%s', (idTravail,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            idProbleme = dato[0][1]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariTravail(usuari, idTravail, idIntervention, idProbleme)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Travail.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class TravailEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idTravail = novar(self.request.get('idTravail'))
            idIntervention = novar(self.request.get('idIntervention'))
            idProbleme = novar(self.request.get('idProbleme'))
            idIndustriel = novar(self.request.get('idIndustriel'))
            coutIndustriel = self.request.get('coutIndustriel')
            nomTravail = novar(self.request.get('nomTravail'))
            description = novar(self.request.get('description'))
            materiel1 = novar(self.request.get('materiel1'))
            unite1 = novar(self.request.get('unite1'))
            unitaire1 = self.request.get('unitaire1')
            quantite1 = self.request.get('quantite1')
            materiel2 = novar(self.request.get('materiel2'))
            unite2 = novar(self.request.get('unite2'))
            unitaire2 = self.request.get('unitaire2')
            quantite2 = self.request.get('quantite2')
            materiel3 = novar(self.request.get('materiel3'))
            unite3 = novar(self.request.get('unite3'))
            unitaire3 = self.request.get('unitaire3')
            quantite3 = self.request.get('quantite3')
            materiel4 = novar(self.request.get('materiel4'))
            unite4 = novar(self.request.get('unite4'))
            unitaire4 = self.request.get('unitaire4')
            quantite4 = self.request.get('quantite4')
            materiel5 = novar(self.request.get('materiel5'))
            unite5 = novar(self.request.get('unite5'))
            unitaire5 = self.request.get('unitaire5')
            quantite5 = self.request.get('quantite5')
            unitaireMO = self.request.get('unitaireMO')
            quantiteMO = self.request.get('quantiteMO')
            unitaireMOA = self.request.get('unitaireMOA')
            quantiteMOA = self.request.get('quantiteMOA')
            unitaireDep = self.request.get('unitaireDep')
            quantiteDep = self.request.get('quantiteDep')
            ok = self.request.get('ok')
            if ok=='1':
                ok=int(ok)
            else:
                ok=0

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE TRAVAIL SET idIntervention=%s, idProbleme=%s, idIndustriel=%s, coutIndustriel=%s, nomTravail=%s, description=%s, materiel1=%s, unite1=%s, unitaire1=%s, quantite1=%s, materiel2=%s, unite2=%s, unitaire2=%s, quantite2=%s, materiel3=%s, unite3=%s, unitaire3=%s, quantite3=%s, materiel4=%s, unite4=%s, unitaire4=%s, quantite4=%s, materiel5=%s, unite5=%s, unitaire5=%s, quantite5=%s, unitaireMO=%s, quantiteMO=%s, unitaireMOA=%s, quantiteMOA=%s, unitaireDep=%s, quantiteDep=%s, ok=%s WHERE idTravail=%s', (idIntervention, idProbleme, idIndustriel, coutIndustriel, nomTravail, description, materiel1, unite1, unitaire1, quantite1, materiel2, unite2, unitaire2, quantite2, materiel3, unite3, unitaire3, quantite3, materiel4, unite4, unitaire4, quantite4, materiel5, unite5, unitaire5, quantite5, unitaireMO, quantiteMO, unitaireMOA, quantiteMOA, unitaireDep, quantiteDep, ok, idTravail))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariTravail(usuari, idTravail, idIntervention, idProbleme)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Travail.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class TravailElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idTravail = novar(self.request.get('idTravail'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM TRAVAIL WHERE idTravail=%s', (idTravail,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM TRAVAIL WHERE idTravail=%s', (idTravail,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))
            
###########################################################################################################################################################
# DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS        DEVIS
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariDevis (usuari, idDevis, idIntervention):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idDevis < 0:       #si es negatiu monta html preparat per a nou
        dateDevis=dataHui
        devisSelect = Devis(idDevis,idIntervention,dateDevis,'')
        ligneDevisDevis=''
    else:                  #sino monta html amb seleccionat
        devisSelect = tablaDevisSelect(cursor, idDevis)
        ligneDevisDevis = tablaLigneDevisDevis (cursor, idDevis)

    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    ultimDevis = tablaUltimDevis(cursor)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'devisSelect': devisSelect,
            'ligneDevisDevis': ligneDevisDevis,
            'travailleurSelect': travailleurSelect,
            'ultimDevis': ultimDevis,
            'idIntervention': idIntervention,
            'travailIntervention': travailIntervention
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaDevisSelect(cursor, idDevis):
    cursor.execute('SELECT idDevis, idIntervention, dateDevis, nombreDevis FROM DEVIS WHERE idDevis=%s',(idDevis,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        data=dataFormat(i[2])       
        lista = Devis(i[0],i[1],data,i[3]) #Modificar si anyadim columna
    return lista

def tablaLigneDevisDevis(cursor, idDevis):
    cursor.execute('SELECT idLigneDevis, idTravail, idDevis FROM LIGNEDEVIS WHERE idDevis=%s',(idDevis,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista        
        lista[indice] = LigneDevis(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class LigneDevis:
    def __init__(self, idLigneDevis=0, idTravail=0, idDevis=0):
        self.idLigneDevis = idLigneDevis
        self.idTravail = idTravail
        self.idDevis = idDevis

def tablaLigneDevisTots(cursor):
    cursor.execute('SELECT idLigneDevis, idTravail, idDevis FROM LIGNEDEVIS')
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista        
        lista[indice] = LigneDevis(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

# ACCIONS DEL FORMULARI
##############################

class DevisNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idDevis = -2
            
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class DevisCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            dateDevis = novar(self.request.get('dateDevis'))
            nombreDevis = novar(self.request.get('nombreDevis'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO DEVIS (idIntervention, dateDevis, nombreDevis) VALUES (%s, %s, %s)', (idIntervention, dateDevis, nombreDevis))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idDevis FROM DEVIS ORDER BY idDevis DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idDevis = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class DevisSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idDevis = novar(self.request.get('idDevis'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM DEVIS WHERE idDevis=%s', (idDevis,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 

class DevisSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idDevis = novar(self.request.get('idDevis'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM DEVIS WHERE idDevis=%s', (idDevis,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class DevisEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idDevis = novar(self.request.get('idDevis'))
            idIntervention = novar(self.request.get('idIntervention'))
            dateDevis = novar(self.request.get('dateDevis'))
            nombreDevis = novar(self.request.get('nombreDevis'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE DEVIS SET idIntervention=%s, dateDevis=%s, nombreDevis=%s WHERE idDevis=%s', (idIntervention, dateDevis, nombreDevis, idDevis))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 

#--ELIMINA PASSAT PER LINK
class DevisElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idDevis = novar(self.request.get('idDevis'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM DEVIS WHERE idDevis=%s', (idDevis,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM DEVIS WHERE idDevis=%s', (idDevis,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))

###########################################################################################################################################################
# FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE     FACTURE
###########################################################################################################################################################





# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariFacture (usuari, idFacture, idIntervention):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idFacture < 0:       #si es negatiu monta html preparat per a nou
        dateFacture=dataHui
        factureSelect = Facture(idFacture,idIntervention,dateFacture,'','')
        ligneFactureFacture=''
    else:                  #sino monta html amb seleccionat
        factureSelect = tablaFactureSelect(cursor, idFacture)
        ligneFactureFacture = tablaLigneFactureFacture (cursor, idFacture)

    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    ultimFacture = tablaUltimFacture(cursor)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'factureSelect': factureSelect,
            'ligneFactureFacture': ligneFactureFacture,
            'travailleurSelect': travailleurSelect,
            'ultimFacture': ultimFacture,
            'idIntervention': idIntervention,
            'travailIntervention': travailIntervention,
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaFactureSelect(cursor, idFacture):
    cursor.execute('SELECT idFacture, idIntervention, dateFacture, nombreFacture, datePaye FROM FACTURE WHERE idFacture=%s',(idFacture,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista = Facture(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
    return lista




def tablaLigneFactureFacture(cursor, idFacture):
    cursor.execute('SELECT idLigneFacture, idTravail, idFacture FROM LIGNEFACTURE WHERE idFacture=%s',(idFacture,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista        
        lista[indice] = LigneFacture(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class LigneFacture:
    def __init__(self, idLigneFacture=0, idTravail=0, idFacture=0):
        self.idLigneFacture = idLigneFacture
        self.idTravail = idTravail
        self.idFacture = idFacture
        


# ACCIONS DEL FORMULARI
##############################

class FactureNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idFacture = -2
            
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class FactureCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            dateFacture = novar(self.request.get('dateFacture'))
            nombreFacture = novar(self.request.get('nombreFacture'))
            datePaye = novar(self.request.get('datePaye'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO FACTURE (idIntervention, dateFacture, nombreFacture, datePaye) VALUES (%s, %s, %s, %s)', (idIntervention, dateFacture, nombreFacture, datePaye))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idFacture FROM FACTURE ORDER BY idFacture DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idFacture = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class FactureSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idFacture = novar(self.request.get('idFacture'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM FACTURE WHERE idFacture=%s', (idFacture,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 

class FactureSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idFacture = novar(self.request.get('idFacture'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM FACTURE WHERE idFacture=%s', (idFacture,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class FactureEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idFacture = novar(self.request.get('idFacture'))
            idIntervention = novar(self.request.get('idIntervention'))
            dateFacture = novar(self.request.get('dateFacture'))
            nombreFacture = novar(self.request.get('nombreFacture'))
            datePaye = novar(self.request.get('datePaye'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE FACTURE SET idIntervention=%s, dateFacture=%s, nombreFacture=%s, datePaye=%s WHERE idFacture=%s', (idIntervention, dateFacture, nombreFacture, datePaye, idFacture))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 


#--ELIMINA PASSAT PER LINK
class FactureElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idFacture = novar(self.request.get('idFacture'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM FACTURE WHERE idFacture=%s', (idFacture,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM FACTURE WHERE idFacture=%s', (idFacture,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))


###########################################################################################################################################################
# LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       LIGNEFACTURE       
###########################################################################################################################################################





# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariLigneFacture (usuari, idLigneFacture, idFacture, idIntervention):
    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idLigneFacture < 0:       #si es negatiu monta html preparat per a nou

        ligneFactureSelect = LigneFacture(idLigneFacture,'','')

    else:                  #sino monta html amb seleccionat
        ligneFactureSelect = tablaLigneFactureSelect(cursor, idLigneFacture)


    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'ligneFactureSelect': ligneFactureSelect,
            'travailleurSelect': travailleurSelect,
            'idIntervention': idIntervention,
            'idFacture': idFacture,
            'travailIntervention': travailIntervention,
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaLigneFactureSelect(cursor, idLigneFacture):
    cursor.execute('SELECT idLigneFacture, idTravail, idFacture FROM LIGNEFACTURE WHERE idLigneFacture=%s',(idLigneFacture,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista      
        lista = LigneFacture(i[0],i[1],i[2]) #Modificar si anyadim columna
    return lista


# ACCIONS DEL FORMULARI
##############################

class LigneFactureNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            idFacture = novar(self.request.get('idFacture'))
            idFacture = int(idFacture)
            
            idLigneFacture=-2
            
            #obtenim valors per al html
            values = formulariLigneFacture(usuari, idLigneFacture, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneFacture.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class LigneFactureCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idFacture = novar(self.request.get('idFacture'))
            idTravail = novar(self.request.get('idTravail'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO LIGNEFACTURE (idTravail, idFacture) VALUES (%s, %s)', (idTravail, idFacture))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idLigneFacture FROM LIGNEFACTURE ORDER BY idLigneFacture DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idLigneFacture = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariLigneFacture(usuari, idLigneFacture, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneFacture.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneFactureSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneFacture = novar(self.request.get('idLigneFacture'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idFacture FROM LIGNEFACTURE WHERE idLigneFacture=%s', (idLigneFacture,))
            dato = cursor.fetchall()
            idFacture = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM FACTURE WHERE idFacture=%s', (idFacture,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariLigneFacture(usuari, idLigneFacture, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneFacture.html') 
            self.response.out.write(template.render(path, values)) 

 

#--CAPTURA DADES DEL HTML I EDITA
class LigneFactureEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idLigneFacture = novar(self.request.get('idLigneFacture'))
            idIntervention = novar(self.request.get('idIntervention'))
            idFacture = novar(self.request.get('idFacture'))
            idTravail = novar(self.request.get('idTravail'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE LIGNEFACTURE SET idTravail=%s WHERE idLigneFacture=%s', (idTravail, idLigneFacture))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariLigneFacture(usuari, idLigneFacture, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneFacture.html') 
            self.response.out.write(template.render(path, values)) 
            
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneFactureElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneFacture = novar(self.request.get('idLigneFacture'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idFacture FROM LIGNEFACTURE WHERE idLigneFacture=%s', (idLigneFacture,))
            dato = cursor.fetchall()
            idFacture = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM FACTURE WHERE idFacture=%s', (idFacture,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            cursor.execute('DELETE FROM LIGNEFACTURE WHERE idLigneFacture=%s', (idLigneFacture,))
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariFacture(usuari, idFacture, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Facture.html') 
            self.response.out.write(template.render(path, values)) 
            
            
###########################################################################################################################################################
# PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       PROFORME       
###########################################################################################################################################################





# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariProforme (usuari, idProforme, idIntervention):
    
    #dataHui
    ara = datetime.datetime.today()
    dataHui = ara.strftime('%Y-%m-%d')

    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idProforme < 0:       #si es negatiu monta html preparat per a nou
        dateProforme=dataHui
        proformeSelect = Proforme(idProforme,idIntervention,dateProforme,'','')
        ligneProformeProforme=''
    else:                  #sino monta html amb seleccionat
        proformeSelect = tablaProformeSelect(cursor, idProforme)
        ligneProformeProforme = tablaLigneProformeProforme (cursor, idProforme)

    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    ultimProforme = tablaUltimProforme(cursor)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'proformeSelect': proformeSelect,
            'ligneProformeProforme': ligneProformeProforme,
            'travailleurSelect': travailleurSelect,
            'ultimProforme': ultimProforme,
            'idIntervention': idIntervention,
            'travailIntervention': travailIntervention,
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaProformeSelect(cursor, idProforme):
    cursor.execute('SELECT idProforme, idIntervention, dateProforme, nombreProforme, datePaye FROM PROFORME WHERE idProforme=%s',(idProforme,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista
        dataF=dataFormat(i[2]) 
        dataP=dataFormat(i[4])         
        lista = Proforme(i[0],i[1],dataF,i[3],dataP) #Modificar si anyadim columna
    return lista




def tablaLigneProformeProforme(cursor, idProforme):
    cursor.execute('SELECT idLigneProforme, idTravail, idProforme FROM LIGNEPROFORME WHERE idProforme=%s',(idProforme,))
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista        
        lista[indice] = LigneProforme(i[0],i[1],i[2])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class LigneProforme:
    def __init__(self, idLigneProforme=0, idTravail=0, idProforme=0):
        self.idLigneProforme = idLigneProforme
        self.idTravail = idTravail
        self.idProforme = idProforme
        


# ACCIONS DEL FORMULARI
##############################

class ProformeNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            #pasem parametre
            idProforme = -2
            
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class ProformeCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            dateProforme = novar(self.request.get('dateProforme'))
            nombreProforme = novar(self.request.get('nombreProforme'))
            datePaye = novar(self.request.get('datePaye'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO PROFORME (idIntervention, dateProforme, nombreProforme, datePaye) VALUES (%s, %s, %s, %s)', (idIntervention, dateProforme, nombreProforme, datePaye))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idProforme FROM PROFORME ORDER BY idProforme DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idProforme = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class ProformeSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idProforme = novar(self.request.get('idProforme'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM PROFORME WHERE idProforme=%s', (idProforme,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 

class ProformeSelectPost(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idProforme = novar(self.request.get('idProforme'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM PROFORME WHERE idProforme=%s', (idProforme,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 

#--CAPTURA DADES DEL HTML I EDITA
class ProformeEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idProforme = novar(self.request.get('idProforme'))
            idIntervention = novar(self.request.get('idIntervention'))
            dateProforme = novar(self.request.get('dateProforme'))
            nombreProforme = novar(self.request.get('nombreProforme'))
            datePaye = novar(self.request.get('datePaye'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE PROFORME SET idIntervention=%s, dateProforme=%s, nombreProforme=%s, datePaye=%s WHERE idProforme=%s', (idIntervention, dateProforme, nombreProforme, datePaye, idProforme))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 


#--ELIMINA PASSAT PER LINK
class ProformeElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #rep identificador del boto html
            idProforme = novar(self.request.get('idProforme'))
        
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idIntervention FROM PROFORME WHERE idProforme=%s', (idProforme,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            cursor.execute('DELETE FROM PROFORME WHERE idProforme=%s', (idProforme,))
            #tanca conexio
            db.commit()
            db.close()
            
            #pasem parametres
            idIntervention = idIntervention
            idDossier = idDossier              #filtro
            idSituation = -1            #filtro
            idProbleme = -1             #filtro
            idIndustriel = -1           #filtro

            
            #obtenim valors per al html
            values = formulariIntervention(usuari, idIntervention, idDossier, idSituation, idProbleme, idIndustriel)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Intervention.html') 
            self.response.out.write(template.render(path, values))


###########################################################################################################################################################
# LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       LIGNEPROFORME       
###########################################################################################################################################################





# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariLigneProforme (usuari, idLigneProforme, idProforme, idIntervention):
    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idLigneProforme < 0:       #si es negatiu monta html preparat per a nou

        ligneProformeSelect = LigneProforme(idLigneProforme,'','')

    else:                  #sino monta html amb seleccionat
        ligneProformeSelect = tablaLigneProformeSelect(cursor, idLigneProforme)


    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'ligneProformeSelect': ligneProformeSelect,
            'travailleurSelect': travailleurSelect,
            'idIntervention': idIntervention,
            'idProforme': idProforme,
            'travailIntervention': travailIntervention,
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaLigneProformeSelect(cursor, idLigneProforme):
    cursor.execute('SELECT idLigneProforme, idTravail, idProforme FROM LIGNEPROFORME WHERE idLigneProforme=%s',(idLigneProforme,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista      
        lista = LigneProforme(i[0],i[1],i[2]) #Modificar si anyadim columna
    return lista


# ACCIONS DEL FORMULARI
##############################

class LigneProformeNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            idProforme = novar(self.request.get('idProforme'))
            idProforme = int(idProforme)
            
            idLigneProforme=-2
            
            #obtenim valors per al html
            values = formulariLigneProforme(usuari, idLigneProforme, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneProforme.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class LigneProformeCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idProforme = novar(self.request.get('idProforme'))
            idTravail = novar(self.request.get('idTravail'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO LIGNEPROFORME (idTravail, idProforme) VALUES (%s, %s)', (idTravail, idProforme))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idLigneProforme FROM LIGNEPROFORME ORDER BY idLigneProforme DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idLigneProforme = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariLigneProforme(usuari, idLigneProforme, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneProforme.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneProformeSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneProforme = novar(self.request.get('idLigneProforme'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idProforme FROM LIGNEPROFORME WHERE idLigneProforme=%s', (idLigneProforme,))
            dato = cursor.fetchall()
            idProforme = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM PROFORME WHERE idProforme=%s', (idProforme,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariLigneProforme(usuari, idLigneProforme, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneProforme.html') 
            self.response.out.write(template.render(path, values)) 

 

#--CAPTURA DADES DEL HTML I EDITA
class LigneProformeEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idLigneProforme = novar(self.request.get('idLigneProforme'))
            idIntervention = novar(self.request.get('idIntervention'))
            idProforme = novar(self.request.get('idProforme'))
            idTravail = novar(self.request.get('idTravail'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE LIGNEPROFORME SET idTravail=%s WHERE idLigneProforme=%s', (idTravail, idLigneProforme))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariLigneProforme(usuari, idLigneProforme, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneProforme.html') 
            self.response.out.write(template.render(path, values)) 
            
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneProformeElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneProforme = novar(self.request.get('idLigneProforme'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idProforme FROM LIGNEPROFORME WHERE idLigneProforme=%s', (idLigneProforme,))
            dato = cursor.fetchall()
            idProforme = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM PROFORME WHERE idProforme=%s', (idProforme,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            cursor.execute('DELETE FROM LIGNEPROFORME WHERE idLigneProforme=%s', (idLigneProforme,))
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariProforme(usuari, idProforme, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Proforme.html') 
            self.response.out.write(template.render(path, values)) 









###########################################################################################################################################################
# LIGNEDEVIS       LIGNEDEVIS           LIGNEDEVIS        LIGNEDEVIS        LIGNEDEVIS        LIGNEDEVIS        LIGNEDEVIS        LIGNEDEVIS    
###########################################################################################################################################################





# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariLigneDevis (usuari, idLigneDevis, idDevis, idIntervention):
    
    #accions sobre bd
    db= get_db()
    cursor = db.cursor()        
        
    #tables per al html
    if idLigneDevis < 0:       #si es negatiu monta html preparat per a nou

        ligneDevisSelect = LigneDevis(idLigneDevis,'','')

    else:                  #sino monta html amb seleccionat
        ligneDevisSelect = tablaLigneDevisSelect(cursor, idLigneDevis)


    travailleurSelect=tablaTravailleurSelect(cursor,usuari)
    travailIntervention = tablaTravailIntervention(cursor, idIntervention)
   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'ligneDevisSelect': ligneDevisSelect,
            'travailleurSelect': travailleurSelect,
            'idIntervention': idIntervention,
            'idDevis': idDevis,
            'travailIntervention': travailIntervention,
            }
    return values   

# FUNCIO SECUNDARIES DEL FORMULARI
##############################

def tablaLigneDevisSelect(cursor, idLigneDevis):
    cursor.execute('SELECT idLigneDevis, idTravail, idDevis FROM LIGNEDEVIS WHERE idLigneDevis=%s',(idLigneDevis,))
    lista = cursor.fetchall()
    for i in lista: #cada fila es converteix en un objecte de lista      
        lista = LigneDevis(i[0],i[1],i[2]) #Modificar si anyadim columna
    return lista


# ACCIONS DEL FORMULARI
##############################

class LigneDevisNou(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):  
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idIntervention = int(idIntervention)
            
            idDevis = novar(self.request.get('idDevis'))
            idDevis = int(idDevis)
            
            idLigneDevis=-2
            
            #obtenim valors per al html
            values = formulariLigneDevis(usuari, idLigneDevis, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneDevis.html') 
            self.response.out.write(template.render(path, values)) 


#--CAPTURA DADES DEL HTML I CREA NOU
class LigneDevisCrea(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):          
            #captura camps del html)
            idIntervention = novar(self.request.get('idIntervention'))
            idDevis = novar(self.request.get('idDevis'))
            idTravail = novar(self.request.get('idTravail'))
     

       
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #inserta fila
            cursor.execute('INSERT INTO LIGNEDEVIS (idTravail, idDevis) VALUES (%s, %s)', (idTravail, idDevis))
            #obtenir el idEsquema de la fila que hem insertat
            cursor.execute('SELECT idLigneDevis FROM LIGNEDEVIS ORDER BY idLigneDevis DESC LIMIT 0,1')
            lista = cursor.fetchall()
            idLigneDevis = lista[0][0]
            #inserta fila en pressupost
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #parametres per a funcio principal del formulari

            
            #obtenim valors per al html
            values = formulariLigneDevis(usuari, idLigneDevis, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneDevis.html') 
            self.response.out.write(template.render(path, values)) 
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneDevisSelect(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneDevis = novar(self.request.get('idLigneDevis'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDevis FROM LIGNEDEVIS WHERE idLigneDevis=%s', (idLigneDevis,))
            dato = cursor.fetchall()
            idDevis = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM DEVIS WHERE idDevis=%s', (idDevis,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariLigneDevis(usuari, idLigneDevis, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneDevis.html') 
            self.response.out.write(template.render(path, values)) 

 

#--CAPTURA DADES DEL HTML I EDITA
class LigneDevisEdita(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):              
            #captura camps del html
            idLigneDevis = novar(self.request.get('idLigneDevis'))
            idIntervention = novar(self.request.get('idIntervention'))
            idDevis = novar(self.request.get('idDevis'))
            idTravail = novar(self.request.get('idTravail'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            #edita fila en tabla
            cursor.execute('UPDATE LIGNEDEVIS SET idTravail=%s WHERE idLigneDevis=%s', (idTravail, idLigneDevis))
            #tanca conexio
            db.commit()
            db.close()
            
            #obtenim valors per al html
            values = formulariLigneDevis(usuari, idLigneDevis, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'LigneDevis.html') 
            self.response.out.write(template.render(path, values)) 
            
            
#--MOSTRA EL FORMULARI AMB LA SELECCIO PASADA PER LINK
class LigneDevisElimina(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):         
            #rep identificador del link html
            idLigneDevis = novar(self.request.get('idLigneDevis'))
            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDevis FROM LIGNEDEVIS WHERE idLigneDevis=%s', (idLigneDevis,))
            dato = cursor.fetchall()
            idDevis = dato[0][0]
            
            cursor.execute('SELECT idIntervention FROM DEVIS WHERE idDevis=%s', (idDevis,))
            dato = cursor.fetchall()
            idIntervention = dato[0][0]

            cursor.execute('DELETE FROM LIGNEDEVIS WHERE idLigneDevis=%s', (idLigneDevis,))
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()
        
            #obtenim valors per al html
            values = formulariDevis(usuari, idDevis, idIntervention)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Devis.html') 
            self.response.out.write(template.render(path, values)) 
            
            
###########################################################################################################################################################
# IMPRIMIR     IMPRIMIR          IMPRIMIR         IMPRIMIR         IMPRIMIR         IMPRIMIR         IMPRIMIR         IMPRIMIR         IMPRIMIR        
###########################################################################################################################################################




#--CAPTURA DADES DEL HTML I IMPRIMEIX
class ImpFI(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):             
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idDossier = novar(self.request.get('idDossier'))

            
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            interventionSelect = tablaInterventionSelect(cursor, idIntervention)
            dossierSelect = tablaDossierSelect(cursor, idDossier)
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 

            
            #valors per al html
            values = {
              'interventionSelect': interventionSelect,
              'dossierSelect': dossierSelect,
                      }
            
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'ImpFImdmIB.html') 
            self.response.out.write(template.render(path, values))
            

#--CAPTURA DADES DEL HTML I IMPRIMEIX
class ImpDevis(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):            
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idDevis = novar(self.request.get('idDevis'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
            
            
            defImpDevis(self, idIntervention, idDossier, idDevis)
            

            



def defImpDevis (self, idIntervention, idDossier, idDevis):
    
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 

            
            cursor.execute('SELECT tiva FROM CONSTANT WHERE idConstant=%s', (1,))
            dato = cursor.fetchall()
            tiva= dato[0][0]


            cursor.execute('SELECT idClient FROM DOSSIER WHERE idDossier=%s', (idDossier,))
            dato = cursor.fetchall()
            idClient= dato[0][0]
            
            cursor.execute('SELECT tr.idTravail, tr.idIntervention, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail, tr.description, tr.materiel1, tr.unite1, tr.unitaire1, tr.quantite1, tr.materiel2, tr.unite2, tr.unitaire2, tr.quantite2, tr.materiel3, tr.unite3, tr.unitaire3, tr.quantite3, tr.materiel4, tr.unite4, tr.unitaire4, tr.quantite4, tr.materiel5, tr.unite5, tr.unitaire5, tr.quantite5, tr.unitaireMO, tr.quantiteMO, tr.unitaireMOA, tr.quantiteMOA, tr.unitaireDep, tr.quantiteDep, tr.ok FROM TRAVAIL tr INNER JOIN LIGNEDEVIS ld ON tr.idTravail=ld.idTravail WHERE idDevis=%s', (idDevis,))
            tabla = cursor.fetchall()
            
            interventionSelect = tablaInterventionSelect(cursor, idIntervention)
            dossierSelect = tablaDossierSelect(cursor, idDossier)
            devisSelect = tablaDevisSelect(cursor, idDevis)
            clientSelect = tablaClientSelect(cursor, idClient)
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
             
            conta=0
            indice=0
            for i in tabla: #conta el numero de files de la tabla
                conta=conta+1
            lista=[0]*conta #creem lista
            for i in tabla:
                materiel1 = i[7]
                unite1 = i[8]
                unitaire1a = i[9]
                quantite1a = i[10]
                if unitaire1a == 0:
                    total1 = ""
                    unitaire1 = ""
                    quantite1 = ""
                    total1a = 0
                else:
                    total1a = unitaire1a * quantite1a
                    total1a = round(total1a,2)
                    total1 = "{:.2f}".format(round(total1a, 2))
                    unitaire1 = "{:.2f}".format(round(unitaire1a, 2))
                    quantite1 = "{:.2f}".format(round(quantite1a, 2))
                
                materiel2 = i[11]
                unite2 = i[12]
                unitaire2a = i[13]
                quantite2a = i[14]
                if unitaire2a == 0:
                    total2 = ""
                    unitaire2 = ""
                    quantite2 = ""
                    total2a = 0
                else:
                    total2a = unitaire2a * quantite2a
                    total2a = round(total2a,2)
                    total2 = "{:.2f}".format(round(total2a, 2))
                    unitaire2 = "{:.2f}".format(round(unitaire2a, 2))
                    quantite2 = "{:.2f}".format(round(quantite2a, 2))
                
                materiel3 = i[15]
                unite3 = i[16]
                unitaire3a = i[17]
                quantite3a = i[18]
                if unitaire3a == 0:
                    total3 = ""
                    unitaire3 = ""
                    quantite3 = ""
                    total3a = 0
                else:
                    total3a = unitaire3a * quantite3a
                    total3a = round(total3a,2)
                    total3 = "{:.2f}".format(round(total3a, 2))
                    unitaire3 = "{:.2f}".format(round(unitaire3a, 2))
                    quantite3 = "{:.2f}".format(round(quantite3a, 2))
                
                materiel4 = i[19]
                unite4 = i[20]
                unitaire4a = i[21]
                quantite4a = i[22]
                if unitaire4a == 0:
                    total4 = ""
                    unitaire4 = ""
                    quantite4 = ""
                    total4a = 0
                else:
                    try:
                        total4a = unitaire4a * quantite4a
                        total4a = round(total4a,2)
                        total4 = "{:.2f}".format(round(total4a, 2))
                        unitaire4 = "{:.2f}".format(round(unitaire4a, 2))
                        quantite4 = "{:.2f}".format(round(quantite4a, 2))
                    except:
                        total4 = ""
                        unitaire4 = ""
                        quantite4 = ""
                        total4a = 0
                
                materiel5 = i[23]
                unite5 = i[24]
                unitaire5a = i[25]
                quantite5a = i[26]
                if unitaire5a == 0:
                    total5 = ""
                    unitaire5 = ""
                    quantite5 = ""
                    total5a = 0
                else:
                    try:
                        total5a = unitaire5a * quantite5a
                        total5a = round(total5a,2)
                        total5 = "{:.2f}".format(round(total5a, 2))
                        unitaire5 = "{:.2f}".format(round(unitaire5a, 2))
                        quantite5 = "{:.2f}".format(round(quantite5a, 2))
                    except:
                        total5 = ""
                        unitaire5 = ""
                        quantite5 = ""
                        total5a = 0

                unitaireMOa = i[27]
                quantiteMOa = i[28]
                if unitaireMOa == 0:
                    totalMO = ""
                    unitaireMO = ""
                    quantiteMO = ""
                    totalMOa = 0
                else:
                    totalMOa = unitaireMOa * quantiteMOa
                    totalMOa = round(totalMOa,2)
                    totalMO = "{:.2f}".format(round(totalMOa, 2))
                    unitaireMO = "{:.2f}".format(round(unitaireMOa, 2))
                    quantiteMO = "{:.2f}".format(round(quantiteMOa, 2))

                unitaireMOAa = i[29]
                quantiteMOAa = i[30]
                if unitaireMOAa == 0:
                    totalMOA = ""
                    unitaireMOA = ""
                    quantiteMOA = ""
                    totalMOAa = 0
                else:
                    try:
                        totalMOAa = unitaireMOAa * quantiteMOAa
                        totalMOAa = round(totalMOAa,2)
                        totalMOA = "{:.2f}".format(round(totalMOAa, 2))
                        unitaireMOA = "{:.2f}".format(round(unitaireMOAa, 2))
                        quantiteMOA = "{:.2f}".format(round(quantiteMOAa, 2))
                    except:
                        totalMOA = ""
                        unitaireMOA = ""
                        quantiteMOA = ""
                        totalMOAa = 0

                unitaireDepa = i[31]
                quantiteDepa = i[32]
                if unitaireDepa == 0:
                    totalDep = ""
                    unitaireDep = ""
                    quantiteDep = ""
                    totalDepa = 0
                else:
                    totalDepa = unitaireDepa * quantiteDepa
                    totalDepa = round(totalDepa,2)
                    totalDep = "{:.2f}".format(round(totalDepa, 2))
                    unitaireDep = "{:.2f}".format(round(unitaireDepa, 2))
                    quantiteDep = "{:.2f}".format(round(quantiteDepa, 2))
                
                totalTravail = total1a + total2a + total3a + total4a + total5a + totalMOa + totalMOAa + totalDepa
                if totalTravail == 0:
                    totalTravaila = ""
                else:
                    totalTravaila = "{:.2f}".format(round(totalTravail, 2))

                          
                lista[indice] = TravailSum(i[0],i[1],i[2],i[3],i[4],i[5],i[6],materiel1,unite1,unitaire1,quantite1,materiel2,unite2,unitaire2,quantite2,materiel3,unite3,unitaire3,quantite3,materiel4,unite4,unitaire4, quantite4,materiel5,unite5,unitaire5, quantite5, unitaireMO,quantiteMO,unitaireMOA,quantiteMOA,unitaireDep,quantiteDep, total1, total2, total3, total4, total5, totalMO, totalMOA, totalDep, totalTravail, totalTravaila) #Modificar si anyadim columna
                indice=indice+1
                
            if conta<2:
                travail1=lista[0]
                travail2=''
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail
            elif conta<3:
                travail1=lista[0]
                travail2=lista[1]
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail
            elif conta<4:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail
            elif conta<5:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail
            elif conta<6:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail
            else:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=lista[5]
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail+travail6.totalTravail
            

            
            iva = bruto*tiva
            iva = round(iva,2)
            neto = bruto+iva                       
            tiva=tiva*100
            
            neto = "{:.2f}".format(round(neto, 2))
            bruto = "{:.2f}".format(round(bruto, 2))
            iva = "{:.2f}".format(round(iva, 2))
            

            
            #valors per al html
            values = {
              'interventionSelect': interventionSelect,
              'dossierSelect': dossierSelect,
              'devisSelect': devisSelect,
              'clientSelect': clientSelect,
              'tiva': tiva,
              'iva': iva,
              'travail1':travail1,
              'travail2':travail2,
              'travail3': travail3,
              'travail4': travail4,
              'travail5': travail5,
              'travail6': travail6,
              'bruto': bruto,
              'neto': neto,
                      }
            
            #imprimim el arxiu html
            if conta <7:
                path = os.path.join(os.path.dirname(__file__), 'ImpDevis1.html')
                self.response.out.write(template.render(path, values)) 
            else:
                self.response.out.write("trop de taches de impression, au maximum 6")
            return   

class TravailSum:
    def __init__(self, idTravail=0, idIntervention=0, idProbleme=0, idIndustriel=0, coutIndustriel='', nomTravail='', description='', materiel1='', unite1='', unitaire1='', quantite1='', materiel2='', unite2='', unitaire2='', quantite2='', materiel3='', unite3='', unitaire3='', quantite3='', materiel4='', unite4='', unitaire4='', quantite4='', materiel5='', unite5='', unitaire5='', quantite5='', unitaireMO='', quantiteMO='', unitaireMOA='', quantiteMOA='', unitaireDep='', quantiteDep='', ok='', total1=0, total2=0, total3=0, total4=0, total5=0, totalMO=0, totalMOA=0, totalDep=0, totalTravail=0, totalTravaila=0):
        self.idTravail = idTravail
        self.idIntervention = idIntervention
        self.idProbleme = idProbleme
        self.idIndustriel = idIndustriel
        self.coutIndustriel = coutIndustriel
        self.nomTravail = nomTravail
        self.description = description
        self.materiel1 = materiel1
        self.unite1 = unite1
        self.unitaire1 = unitaire1
        self.quantite1 = quantite1
        self.materiel2 = materiel2
        self.unite2 = unite2
        self.unitaire2 = unitaire2
        self.quantite2 = quantite2
        self.materiel3 = materiel3
        self.unite3 = unite3
        self.unitaire3 = unitaire3
        self.quantite3  = quantite3
        self.materiel4 = materiel4
        self.unite4 = unite4
        self.unitaire4 = unitaire4
        self.quantite4  = quantite4
        self.materiel5 = materiel5
        self.unite5 = unite5
        self.unitaire5 = unitaire5
        self.quantite5  = quantite5
        self.unitaireMO = unitaireMO
        self.quantiteMO = quantiteMO
        self.unitaireMOA = unitaireMOA
        self.quantiteMOA = quantiteMOA
        self.unitaireDep = unitaireDep
        self.quantiteDep = quantiteDep
        self.ok = ok
        self.total1 = total1
        self.total2 = total2
        self.total3 = total3
        self.total4 = total4
        self.total5 = total5
        self.totalMO = totalMO
        self.totalMOA = totalMOA
        self.totalDep = totalDep
        self.totalTravail = totalTravail
        self.totalTravaila = totalTravaila
        
#--CAPTURA DADES DEL HTML I IMPRIMEIX
class ImpFacture(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):               
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idFacture = novar(self.request.get('idFacture'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
            
            defImpFacture(self, idIntervention, idDossier, idFacture)


            


def defImpFacture (self, idIntervention, idDossier, idFacture):
    
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 

            
            cursor.execute('SELECT tiva FROM CONSTANT WHERE idConstant=%s', (1,))
            dato = cursor.fetchall()
            tiva= dato[0][0]


            cursor.execute('SELECT idClient FROM DOSSIER WHERE idDossier=%s', (idDossier,))
            dato = cursor.fetchall()
            idClient= dato[0][0]
            
            cursor.execute('SELECT tr.idTravail, tr.idIntervention, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail, tr.description, tr.materiel1, tr.unite1, tr.unitaire1, tr.quantite1, tr.materiel2, tr.unite2, tr.unitaire2, tr.quantite2, tr.materiel3, tr.unite3, tr.unitaire3, tr.quantite3, tr.materiel4, tr.unite4, tr.unitaire4, tr.quantite4, tr.materiel5, tr.unite5, tr.unitaire5, tr.quantite5, tr.unitaireMO, tr.quantiteMO, tr.unitaireMOA, tr.quantiteMOA, tr.unitaireDep, tr.quantiteDep, tr.ok FROM TRAVAIL tr INNER JOIN LIGNEFACTURE lf ON tr.idTravail=lf.idTravail WHERE idFacture=%s', (idFacture,))
            tabla = cursor.fetchall()
            
            interventionSelect = tablaInterventionSelect(cursor, idIntervention)
            dossierSelect = tablaDossierSelect(cursor, idDossier)
            factureSelect = tablaFactureSelect(cursor, idFacture)
            clientSelect = tablaClientSelect(cursor, idClient)
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
             
            conta=0
            indice=0
            for i in tabla: #conta el numero de files de la tabla
                conta=conta+1
            lista=[0]*conta #creem lista
            for i in tabla:
                total1a = i[9] * i[10]
                total1a = round(total1a,2)
                total1 = "{:.2f}".format(round(total1a, 2)) if i[9] != 0 else ""
                unitaire1 = "{:.2f}".format(round(i[9], 2)) if i[9] != 0 else ""
                quantite1 = "{:.2f}".format(round(i[10], 2)) if i[10] != 0 else ""

                total2a = i[13] * i[14]
                total2a = round(total2a,2)
                total2 = "{:.2f}".format(round(total2a, 2)) if i[13] != 0 else ""
                unitaire2 = "{:.2f}".format(round(i[13], 2)) if i[13] != 0 else ""
                quantite2 = "{:.2f}".format(round(i[14], 2)) if i[14] != 0 else ""

                total3a = i[17] * i[18]
                total3a = round(total3a,2)
                total3 = "{:.2f}".format(round(total3a, 2)) if i[17] != 0 else ""
                unitaire3 = "{:.2f}".format(round(i[17], 2)) if i[17] != 0 else ""
                quantite3 = "{:.2f}".format(round(i[18], 2)) if i[18] != 0 else ""

                total4a = i[21] * i[22]
                total4a = round(total4a,2)
                total4 = "{:.2f}".format(round(total4a, 2)) if i[21] != 0 else ""
                unitaire4 = "{:.2f}".format(round(i[21], 2)) if i[21] != 0 else ""
                quantite4 = "{:.2f}".format(round(i[22], 2)) if i[22] != 0 else ""

                total5a = i[25] * i[26]
                total5a = round(total5a,2)
                total5 = "{:.2f}".format(round(total5a, 2)) if i[25] != 0 else ""
                unitaire5 = "{:.2f}".format(round(i[25], 2)) if i[25] != 0 else ""
                quantite5 = "{:.2f}".format(round(i[26], 2)) if i[26] != 0 else ""

                totalMOa = i[27] * i[28]
                totalMOa = round(totalMOa,2)
                totalMO = "{:.2f}".format(round(totalMOa, 2)) if i[27] != 0 else ""
                unitaireMO = "{:.2f}".format(round(i[27], 2)) if i[27] != 0 else ""
                quantiteMO = "{:.2f}".format(round(i[28], 2)) if i[28] != 0 else ""

                totalMOAa = i[29] * i[30]
                totalMOAa = round(totalMOAa,2)
                totalMOA = "{:.2f}".format(round(totalMOAa, 2)) if i[29] != 0 else ""
                unitaireMOA = "{:.2f}".format(round(i[29], 2)) if i[29] != 0 else ""
                quantiteMOA = "{:.2f}".format(round(i[30], 2)) if i[30] != 0 else ""

                totalDepa = i[31] * i[32]
                totalDepa = round(totalDepa,2)
                totalDep = "{:.2f}".format(round(totalDepa, 2)) if i[31] != 0 else ""
                unitaireDep = "{:.2f}".format(round(i[31], 2)) if i[31] != 0 else ""
                quantiteDep = "{:.2f}".format(round(i[32], 2)) if i[32] != 0 else ""

                totalTravail = total1a + total2a + total3a + total4a + total5a + totalMOa + totalMOAa + totalDepa
                totalTravaila = "{:.2f}".format(round(totalTravail, 2)) if totalTravail != 0 else ""


                          
                lista[indice] = TravailSum(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],unitaire1,quantite1,i[11],i[12],unitaire2,quantite2,i[15],i[16],unitaire3,quantite3,i[19],i[20],unitaire4,quantite4,i[23],i[24],unitaire5,quantite5,unitaireMO,quantiteMO,unitaireMOA,quantiteMOA,unitaireDep,quantiteDep,i[33], total1, total2, total3, total4, total5, totalMO, totalMOA, totalDep, totalTravail, totalTravaila) #Modificar si anyadim columna
                indice=indice+1
            if conta<2:
                travail1=lista[0]
                travail2=''
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail
            elif conta<3:
                travail1=lista[0]
                travail2=lista[1]
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail
            elif conta<4:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail
            elif conta<5:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail
            elif conta<6:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail
            else:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=lista[5]
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail+travail6.totalTravail
            

            
            
            iva = bruto*tiva
            iva = round(iva,2)
            neto = bruto+iva                   
            tiva=tiva*100
            
            neto = "{:.2f}".format(round(neto, 2))
            bruto = "{:.2f}".format(round(bruto, 2))
            iva = "{:.2f}".format(round(iva, 2))
            

            
            #valors per al html
            values = {
              'interventionSelect': interventionSelect,
              'dossierSelect': dossierSelect,
              'factureSelect': factureSelect,
              'clientSelect': clientSelect,
              'tiva': tiva,
              'iva': iva,
              'travail1':travail1,
              'travail2':travail2,
              'travail3': travail3,
              'travail4': travail4,
              'travail5': travail5,
              'travail6': travail6,
              'bruto': bruto,
              'neto': neto,
                      }
            
            #imprimim el arxiu html
            if conta <7:
                path = os.path.join(os.path.dirname(__file__), 'ImpFacture1.html')
                self.response.out.write(template.render(path, values)) 
            else:
                self.response.out.write("trop de taches de impression, au maximum 6")


#--CAPTURA DADES DEL HTML I IMPRIMEIX
class ImpProforme(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):               
            #captura camps del html
            idIntervention = novar(self.request.get('idIntervention'))
            idProforme = novar(self.request.get('idProforme'))

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 
            
            cursor.execute('SELECT idDossier FROM INTERVENTION WHERE idIntervention=%s',(idIntervention,))
            dato = cursor.fetchall()
            idDossier = dato[0][0]
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
            
            defImpProforme(self, idIntervention, idDossier, idProforme)


            


def defImpProforme (self, idIntervention, idDossier, idProforme):
    
            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 

            
            cursor.execute('SELECT tiva FROM CONSTANT WHERE idConstant=%s', (1,))
            dato = cursor.fetchall()
            tiva= dato[0][0]


            cursor.execute('SELECT idClient FROM DOSSIER WHERE idDossier=%s', (idDossier,))
            dato = cursor.fetchall()
            idClient= dato[0][0]
            
            cursor.execute('SELECT tr.idTravail, tr.idIntervention, tr.idProbleme, tr.idIndustriel, tr.coutIndustriel, tr.nomTravail, tr.description, tr.materiel1, tr.unite1, tr.unitaire1, tr.quantite1, tr.materiel2, tr.unite2, tr.unitaire2, tr.quantite2, tr.materiel3, tr.unite3, tr.unitaire3, tr.quantite3, tr.materiel4, tr.unite4, tr.unitaire4, tr.quantite4, tr.materiel5, tr.unite5, tr.unitaire5, tr.quantite5, tr.unitaireMO, tr.quantiteMO, tr.unitaireMOA, tr.quantiteMOA, tr.unitaireDep, tr.quantiteDep, tr.ok FROM TRAVAIL tr INNER JOIN LIGNEPROFORME lf ON tr.idTravail=lf.idTravail WHERE idProforme=%s', (idProforme,))
            tabla = cursor.fetchall()
            
            interventionSelect = tablaInterventionSelect(cursor, idIntervention)
            dossierSelect = tablaDossierSelect(cursor, idDossier)
            proformeSelect = tablaProformeSelect(cursor, idProforme)
            clientSelect = tablaClientSelect(cursor, idClient)
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close() 
             
            conta=0
            indice=0
            for i in tabla: #conta el numero de files de la tabla
                conta=conta+1
            lista=[0]*conta #creem lista
            for i in tabla:
                total1a = i[9] * i[10]
                total1 = "{:.2f}".format(round(total1a, 2)) if i[9] != 0 else ""
                unitaire1 = "{:.2f}".format(round(i[9], 2)) if i[9] != 0 else ""
                quantite1 = "{:.2f}".format(round(i[10], 2)) if i[10] != 0 else ""

                total2a = i[13] * i[14]
                total2 = "{:.2f}".format(round(total2a, 2)) if i[13] != 0 else ""
                unitaire2 = "{:.2f}".format(round(i[13], 2)) if i[13] != 0 else ""
                quantite2 = "{:.2f}".format(round(i[14], 2)) if i[14] != 0 else ""

                total3a = i[17] * i[18]
                total3 = "{:.2f}".format(round(total3a, 2)) if i[17] != 0 else ""
                unitaire3 = "{:.2f}".format(round(i[17], 2)) if i[17] != 0 else ""
                quantite3 = "{:.2f}".format(round(i[18], 2)) if i[18] != 0 else ""

                total4a = i[21] * i[22]
                total4 = "{:.2f}".format(round(total4a, 2)) if i[21] != 0 else ""
                unitaire4 = "{:.2f}".format(round(i[21], 2)) if i[21] != 0 else ""
                quantite4 = "{:.2f}".format(round(i[22], 2)) if i[22] != 0 else ""

                total5a = i[25] * i[26]
                total5 = "{:.2f}".format(round(total5a, 2)) if i[25] != 0 else ""
                unitaire5 = "{:.2f}".format(round(i[25], 2)) if i[25] != 0 else ""
                quantite5 = "{:.2f}".format(round(i[26], 2)) if i[26] != 0 else ""

                totalMOa = i[27] * i[28]
                totalMO = "{:.2f}".format(round(totalMOa, 2)) if i[27] != 0 else ""
                unitaireMO = "{:.2f}".format(round(i[27], 2)) if i[27] != 0 else ""
                quantiteMO = "{:.2f}".format(round(i[28], 2)) if i[28] != 0 else ""

                totalMOAa = i[29] * i[30]
                totalMOA = "{:.2f}".format(round(totalMOAa, 2)) if i[29] != 0 else ""
                unitaireMOA = "{:.2f}".format(round(i[29], 2)) if i[29] != 0 else ""
                quantiteMOA = "{:.2f}".format(round(i[30], 2)) if i[30] != 0 else ""

                totalDepa = i[31] * i[32]
                totalDep = "{:.2f}".format(round(totalDepa, 2)) if i[31] != 0 else ""
                unitaireDep = "{:.2f}".format(round(i[31], 2)) if i[31] != 0 else ""
                quantiteDep = "{:.2f}".format(round(i[32], 2)) if i[32] != 0 else ""

                totalTravail = total1a + total2a + total3a + total4a + total5a + totalMOa + totalMOAa + totalDepa
                totalTravaila = "{:.2f}".format(round(totalTravail, 2)) if totalTravail != 0 else ""
                          
                lista[indice] = TravailSum(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],unitaire1,quantite1,i[11],i[12],unitaire2,quantite2,i[15],i[16],unitaire3,quantite3,i[19],i[20],unitaire4,quantite4,i[23],i[24],unitaire5,quantite5,unitaireMO,quantiteMO,unitaireMOA,quantiteMOA,unitaireDep,quantiteDep,i[33], total1, total2, total3, total4, total5, totalMO, totalMOA, totalDep, totalTravail, totalTravaila) #Modificar si anyadim columna
                indice=indice+1
            if conta<2:
                travail1=lista[0]
                travail2=''
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail
            elif conta<3:
                travail1=lista[0]
                travail2=lista[1]
                travail3=''
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail
            elif conta<4:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=''
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail
            elif conta<5:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=''
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail
            elif conta<6:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=''
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail
            else:
                travail1=lista[0]
                travail2=lista[1]
                travail3=lista[2]
                travail4=lista[3]
                travail5=lista[4]
                travail6=lista[5]
                bruto = travail1.totalTravail+travail2.totalTravail+travail3.totalTravail+travail4.totalTravail+travail5.totalTravail+travail6.totalTravail
            

            
            
            iva = bruto*tiva
            neto = bruto+iva                    
            tiva=tiva*100
            
            neto = "{:.2f}".format(round(neto, 2))
            bruto = "{:.2f}".format(round(bruto, 2))
            iva = "{:.2f}".format(round(iva, 2))
            

            
            #valors per al html
            values = {
              'interventionSelect': interventionSelect,
              'dossierSelect': dossierSelect,
              'proformeSelect': proformeSelect,
              'clientSelect': clientSelect,
              'tiva': tiva,
              'iva': iva,
              'travail1':travail1,
              'travail2':travail2,
              'travail3': travail3,
              'travail4': travail4,
              'travail5': travail5,
              'travail6': travail6,
              'bruto': bruto,
              'neto': neto,
                      }
            
            #imprimim el arxiu html
            if conta <7:
                path = os.path.join(os.path.dirname(__file__), 'ImpProforme1.html')
                self.response.out.write(template.render(path, values)) 
            else:
                self.response.out.write("trop de taches de impression, au maximum 6")


###########################################################################################################################################################
# INTERVENTION TOUS              INTERVENTION TOUS                 INTERVENTION TOUS              INTERVENTION TOUS              INTERVENTION TOUS   
###########################################################################################################################################################

class InterventionTout(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):   

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 

            interventionTout = tablaInterventionTout(cursor)
            dossierTots = tablaDossierTots(cursor)
            values = {
                      'dossierTots': dossierTots,
                      'interventionTout': interventionTout}
                                                                                        
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()  

        #imprimim el arxiu html
        path = os.path.join(os.path.dirname(__file__), 'InterventionTout.html') 
        self.response.out.write(template.render(path, values))
        

class InterventionDern(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):   

            #conecta a base de datos
            db= get_db()
            cursor = db.cursor() 

            interventionTout = tablaInterventionDern(cursor)
            dossierTots = tablaDossierTots(cursor)
            values = {
                      'dossierTots': dossierTots,
                      'interventionTout': interventionTout}
                                                                                        
            
            #tanquem conexio a la base de datos
            db.commit()
            db.close()  

        #imprimim el arxiu html
        path = os.path.join(os.path.dirname(__file__), 'InterventionTout.html') 
        self.response.out.write(template.render(path, values))
        
        

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaInterventionTout(cursor):
    cursor.execute('SELECT idIntervention, idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait FROM INTERVENTION ORDER BY idIntervention DESC')        
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dateEntree=dataFormat(i[5])
        dateLimite=dataFormat(i[6])
        dateFait=dataFormat(i[7]) 
        lista[indice] = Intervention(i[0],i[1],i[2],i[3],i[4],dateEntree,dateLimite,dateFait,i[8],i[9],i[10],i[11],i[12],i[13])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 

def tablaInterventionDern(cursor):
    cursor.execute('SELECT idIntervention, idDossier, idSituation, numDi, priorite, dateEntree, dateLimite, dateFait, demandeEs, demandeFr, travailFaitEs, travailFaitFr, garantie, mailFait FROM INTERVENTION ORDER BY idIntervention DESC LIMIT 300')        
    tabla = cursor.fetchall()
    conta=0
    indice=0
    for i in tabla: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tabla: #cada fila es converteix en un objecte de lista
        dateEntree=dataFormat(i[5])
        dateLimite=dataFormat(i[6])
        dateFait=dataFormat(i[7]) 
        lista[indice] = Intervention(i[0],i[1],i[2],i[3],i[4],dateEntree,dateLimite,dateFait,i[8],i[9],i[10],i[11],i[12],i[13])  #Modificar si anyadim columna
        indice=indice+1   
    return lista 


###########################################################################################################################################################
# CALENDRIER          CALENDRIER          CALENDRIER          CALENDRIER          CALENDRIER          CALENDRIER          CALENDRIER          CALENDRIER
###########################################################################################################################################################

# FUNCIO PRINCIPAL DEL FORMULARI
################################

def formulariCalendrier (idTravailleur):
    
    #conecta a base de datos
    db= get_db()
    cursor = db.cursor() 
    
    tacheAnterior = tablaTacheAnterior(cursor, idTravailleur)
    tacheHui = tablaTacheHui(cursor, idTravailleur)
    tacheFutur = tablaTacheFutur(cursor, idTravailleur)
    travailleurTots = tablaTravailleurTots(cursor)
    travailleurActiu = tablaTravailleurActiu(cursor)
    travailleurSelect = tablaTravailleurSelect(cursor, idTravailleur)
    dossierTots = tablaDossierTots(cursor)
    typeTacheTots = tablaTypeTacheTots(cursor)
    travailleur = idTravailleur

   
    #tanca conexio bd
    db.commit()
    db.close()
    
    #pasem les llistes al arxiu html
    values = {
            'travailleurTots': travailleurTots,
            'travailleurActiu': travailleurActiu,
            'travailleur': travailleur,
            'dossierTots': dossierTots,
            'typeTacheTots': typeTacheTots,
            'tacheAnterior': tacheAnterior,
            'tacheHui': tacheHui,
            'tacheFutur': tacheFutur,
            'travailleurSelect': travailleurSelect,
            }
    return values  

# FUNCIONS SECUNDARIES DEL FORMULARI
####################################


def tablaTacheAnterior(cursor, idTravailleur):
    ok = 0
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')

    if idTravailleur == -1:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache<%s AND ta.ok=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok))
    else:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache<%s AND ta.ok=%s AND ta.idTravailleur=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok, idTravailleur))
    
    tacheCal = cursor.fetchall()
    conta=0
    indice=0
    for i in tacheCal: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tacheCal: #cada fila es converteix en un objecte de lista
        dateTache = dataFormat(i[3]) # data amb format
        dateEntree = dataFormat(i[10]) # data amb format
   
        lista[indice] = TacheCal(i[0],i[1],i[2],dateTache,i[4],i[5],i[6],i[7],i[8],i[9],dateEntree) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

def tablaTacheHui(cursor, idTravailleur):
    ok = 0
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')

    if idTravailleur == -1:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache=%s AND ta.ok=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok))
    else:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache=%s AND ta.ok=%s AND ta.idTravailleur=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok, idTravailleur))
    
    tacheCal = cursor.fetchall()
    conta=0
    indice=0
    for i in tacheCal: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tacheCal: #cada fila es converteix en un objecte de lista
        dateTache = dataFormat(i[3]) # data amb format
        dateEntree = dataFormat(i[10]) # data amb format
   
        lista[indice] = TacheCal(i[0],i[1],i[2],dateTache,i[4],i[5],i[6],i[7],i[8],i[9],dateEntree) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

def tablaTacheFutur(cursor, idTravailleur):
    ok = 0
    ara = datetime.datetime.today()
    hui = ara.strftime('%Y-%m-%d')

    if idTravailleur == -1:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache>%s AND ta.ok=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok))
    else:
        cursor.execute('SELECT ta.idTache, ta.idTravailleur, ta.idTypeTache, ta.dateTache, ta.commentTache, it.idIntervention, it.idDossier, it.idSituation, it.numDi, it.priorite, it.dateEntree FROM INTERVENTION it INNER JOIN TACHE ta ON it.idIntervention = ta.idIntervention WHERE ta.dateTache>%s AND ta.ok=%s AND ta.idTravailleur=%s ORDER BY  ta.idTravailleur, ta.idTypeTache, ta.dateTache',(hui,ok, idTravailleur))
    
    tacheCal = cursor.fetchall()
    conta=0
    indice=0
    for i in tacheCal: #conta el numero de files de la tabla
        conta=conta+1
    lista=[0]*conta #creem lista
    for i in tacheCal: #cada fila es converteix en un objecte de lista
        dateTache = dataFormat(i[3]) # data amb format
        dateEntree = dataFormat(i[10]) # data amb format
   
        lista[indice] = TacheCal(i[0],i[1],i[2],dateTache,i[4],i[5],i[6],i[7],i[8],i[9],dateEntree) #Modificar si anyadim columna
        indice=indice+1   
    return lista 

class TacheCal:
    def __init__(self, idTache=0, idTravailleur=0, idTypeTache=0, dateTache='', commentTache='', idIntervention=0, idDossier=0, idSituation=0, numDi='', priorite='', dateEntree=''):
        self.idTache = idTache
        self.idTravailleur = idTravailleur
        self.idTypeTache = idTypeTache 
        self.dateTache = dateTache
        self.commentTache = commentTache
        self.idIntervention = idIntervention
        self.idDossier = idDossier
        self.idSituation = idSituation
        self.numDi = numDi
        self.priorite = priorite
        self.dateEntree = dateEntree

# ACCIONS DEL FORMULARI
####################################

#MOSTRA FORMULARI DE FORMA INICIAL
class CalendrierInicial(webapp2.RequestHandler):
    def get(self):
        usuari = autentificacio(self, users)
        if (usuari != -1): 
            if usuari==7:
                idTravailleur = -1
            else:          
                idTravailleur = usuari
            #obtenim valors per al html
            values = formulariCalendrier(idTravailleur)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Calendrier.html') 
            self.response.out.write(template.render(path, values))

#--CAPTURA DADES DEL HTML I CREA NOU
class CalendrierTravailleur(webapp2.RequestHandler):
    def post(self):
        usuari = autentificacio(self, users)
        if (usuari != -1):           
            #captura camps del html
            idTravailleur = novar(self.request.get('idTravailleur'))
            idTravailleur = int(idTravailleur)
            if idTravailleur==7:
                idTravailleur = -1
            else:
                idTravailleur = idTravailleur

            #obtenim valors per al html
            values = formulariCalendrier(idTravailleur)
        
            #imprimim el arxiu html
            path = os.path.join(os.path.dirname(__file__), 'Calendrier.html') 
            self.response.out.write(template.render(path, values))


###########################################################################################################################################################
# REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO    REDIRECCIO
###########################################################################################################################################################
       
        
#redirigeix a les diferents class en funcio de les accions html
app = webapp2.WSGIApplication(
                                     [('/', MainPage),
                                      ('/Inicio', Inicio),                                                  #inici 
                                      ('/UltimDevisEdita', UltimDevisEdita), 
                                      ('/UltimFactureEdita', UltimFactureEdita),
                                      ('/UsuariTots', UsuariTots),
                                      ('/UsuariSelect', UsuariSelect),
                                      ('/UsuariNou', UsuariNou),
                                      ('/UsuariCrea', UsuariCrea),
                                      ('/UsuariEdita', UsuariEdita), 
                                      ('/UsuariElimina', UsuariElimina),
                                      ('/ClientInicial', ClientInicial),
                                      ('/ClientNou', ClientNou),
                                      ('/ClientCrea', ClientCrea),
                                      ('/ClientSelect', ClientSelect),
                                      ('/ClientEdita', ClientEdita),
                                      ('/ClientElimina', ClientElimina), 
                                      ('/DossierInicial', DossierInicial),
                                      ('/DossierNou', DossierNou),
                                      ('/DossierCrea', DossierCrea),
                                      ('/DossierSelect', DossierSelect),
                                      ('/DossierSelectPost', DossierSelectPost),
                                      ('/DossierEdita', DossierEdita),
                                      ('/DossierElimina', DossierElimina), 
                                      ('/InterventionInicial', InterventionInicial),
                                      ('/InterventionNou', InterventionNou),
                                      ('/InterventionCrea', InterventionCrea),
                                      ('/InterventionSelect', InterventionSelect),
                                      ('/InterventionSelectPost', InterventionSelectPost),
                                      ('/InterventionEdita', InterventionEdita),
                                      ('/InterventionElimina', InterventionElimina), 
                                      ('/InterventionTravailFiltro', InterventionTravailFiltro), 
                                      ('/ProfilNouDossier', ProfilNouDossier),
                                      ('/ProfilNouIndustriel', ProfilNouIndustriel),
                                      ('/ProfilCrea', ProfilCrea),
                                      ('/ProfilSelect', ProfilSelect),
                                      ('/ProfilEdita', ProfilEdita),
                                      ('/ProfilElimina', ProfilElimina),
                                      ('/IndustrielInicial', IndustrielInicial),
                                      ('/IndustrielNou', IndustrielNou),
                                      ('/IndustrielCrea', IndustrielCrea),
                                      ('/IndustrielSelect', IndustrielSelect),
                                      ('/IndustrielSelectPost', IndustrielSelectPost),
                                      ('/IndustrielEdita', IndustrielEdita),
                                      ('/IndustrielElimina', IndustrielElimina),
                                      ('/HistoireNou', HistoireNou),
                                      ('/HistoireCrea', HistoireCrea),
                                      ('/HistoireSelect', HistoireSelect),
                                      ('/HistoireEdita', HistoireEdita),
                                      ('/HistoireElimina', HistoireElimina),
                                      ('/TacheNou', TacheNou),
                                      ('/TacheCrea', TacheCrea),
                                      ('/TacheSelect', TacheSelect),
                                      ('/TacheEdita', TacheEdita),
                                      ('/TacheElimina', TacheElimina),
                                      ('/TravailInicial', TravailInicial),
                                      ('/TravailNou', TravailNou),
                                      ('/TravailCrea', TravailCrea),
                                      ('/TravailSelect', TravailSelect),
                                      ('/TravailEdita', TravailEdita),
                                      ('/TravailElimina', TravailElimina),
                                      ('/DevisNou', DevisNou),
                                      ('/DevisCrea', DevisCrea),
                                      ('/DevisSelect', DevisSelect),
                                      ('/DevisSelectPost', DevisSelectPost),
                                      ('/DevisEdita', DevisEdita),
                                      ('/DevisElimina', DevisElimina), 
                                      ('/FactureNou', FactureNou),
                                      ('/FactureCrea', FactureCrea),
                                      ('/FactureSelect', FactureSelect),
                                      ('/FactureSelectPost', FactureSelectPost),
                                      ('/FactureEdita', FactureEdita),
                                      ('/FactureElimina', FactureElimina), 
                                      ('/LigneFactureNou', LigneFactureNou),
                                      ('/LigneFactureCrea', LigneFactureCrea),
                                      ('/LigneFactureSelect', LigneFactureSelect),
                                      ('/LigneFactureEdita', LigneFactureEdita),                                      
                                      ('/LigneFactureElimina', LigneFactureElimina),
                                      ('/ProformeNou', ProformeNou),
                                      ('/ProformeCrea', ProformeCrea),
                                      ('/ProformeSelect', ProformeSelect),
                                      ('/ProformeSelectPost', ProformeSelectPost),
                                      ('/ProformeEdita', ProformeEdita),
                                      ('/ProformeElimina', ProformeElimina), 
                                      ('/LigneProformeNou', LigneProformeNou),
                                      ('/LigneProformeCrea', LigneProformeCrea),
                                      ('/LigneProformeSelect', LigneProformeSelect),
                                      ('/LigneProformeEdita', LigneProformeEdita),                                      
                                      ('/LigneProformeElimina', LigneProformeElimina),
                                      ('/LigneDevisNou', LigneDevisNou),
                                      ('/LigneDevisCrea', LigneDevisCrea),
                                      ('/LigneDevisSelect', LigneDevisSelect),
                                      ('/LigneDevisEdita', LigneDevisEdita),                                      
                                      ('/LigneDevisElimina', LigneDevisElimina),
                                      ('/ImpFI', ImpFI),
                                      ('/ImpFacture', ImpFacture),
                                      ('/ImpProforme', ImpProforme),
                                      ('/ImpDevis', ImpDevis),
                                      ('/InterventionTout', InterventionTout),
                                      ('/InterventionDern', InterventionDern),
                                      ('/CalendrierInicial', CalendrierInicial),
                                      ('/CalendrierTravailleur', CalendrierTravailleur),
                                      ('/UltimFactureEdita', UltimFactureEdita),
                                      ('/UltimDevisEdita', UltimDevisEdita),
                                      ('/UltimProformeEdita', UltimProformeEdita),
                                                                                                                                                                                                                   
                                      ],
                                      debug=True)