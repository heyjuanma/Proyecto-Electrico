#######  LLAMADO A LA PARTE LOGICA ################


from Parte_logica import function 


from tkinter import *
from tkinter import ttk
from tkinter import filedialog   #* ventanas emergentes
import json
from tkinter import messagebox  #* ventanas emergentes


### Constructor con labels, botones, cajitas de texto   ##############




class MyFirstGUI():
    '''A sample how to link front and back'''

    '''Programar el GUI en una clase'''

    def __init__(self, ventana):


        """ LABELS """
        
        self.ventana = ventana
        self.label = Label(ventana, text="This is our first GUI!")
        self.label.pack()
        
        
        self.foto=PhotoImage(file="large.png")


        self.Label(ventana,image=foto).grid(column = 0, row = 1, padx = 7, pady = 10)
        self.Label(ventana,text='ELIGE LAS DISTRIBUIONES DESEADAS', width = "50", height = "1", font = ("Calibri", 13)).grid(column = 0, row = 1, padx = 7, pady = 10)
        self.textoFinal=Label(ventana)
        self.textoFinal.grid(column = 0, row = 8, padx = 7, pady = 10)
        
        
        
        
        self.label = Label(ventana, text= "Ingrese un numero entero entre 0 y 23")
        self.label.grid(column = 1, row = 0, padx = 7, pady = 10)


        """ Entrys """
        self.box = Entry(ventana) #textvariable= numeropantalla)
        self.box.grid(column = 1, row = 1, padx = 7, pady = 10)
        
        
        '''Botones'''


        self.botondias = Button(ventana, text='Abrir fichero', width = "15", height = "1", font = ("Calibri", 13), command=abrirFichero)
        self.botondias.grid(column = 0, row = 0, padx = 7, pady = 10)

        self.boton = Button(ventana,text="Verificar el numero ingresado",command=number)
        self.boton.grid(column = 1, row = 2, padx = 7, pady = 10)
        self.answer = Label(ventana,text="")
        self.answer.grid(column = 1, row = 3, padx = 7, pady = 10)


        """ Checkbutton """""
        
        self.Checkbutton(ventana, text='Norm ',variable=Norm,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 2, padx = 7, pady = 10)
        self.Checkbutton(ventana, text='Rayleigh ',variable=Rayleigh,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 3, padx = 7, pady = 10)
        self.Checkbutton(ventana, text='Burr12 ',variable=Burr12,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 4, padx = 7, pady = 10)
        self.Checkbutton(ventana, text='Alpha ',variable=Alpha,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 5, padx = 7, pady = 10)
        self.Checkbutton(ventana, text='Gamma ',variable=Gamma,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 6, padx = 7, pady = 10)
        self.Checkbutton(ventana, text='Beta ',variable=Beta,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 7, padx = 7, pady = 10)
        
        ### """ MENU """"
        
        self.barraMenu=Menu(ventana)
        self.ventana.config(menu=barraMenu, width=300,height=300) #* dar tamaño

        self.archivoMenu=Menu(barraMenu,tearoff=0) #* quitar pestañá de defecto

######### sub elementos a las pestañas
        #!-------------------Archivo--------------

        self.archivoMenu.add_command(label='Nuevo')
        self.archivoMenu.add_command(label='Guardar')
        self.archivoMenu.add_command(label='Guardar como')

        
        #* separar de submenus 
        self.archivoMenu.add_separator()

        self.archivoMenu.add_command(label='Cerrar', command=cerrarDocumento)
        self.archivoMenu.add_command(label='Salir',command=salirAplicacion)

        #!-------------------Edicion--------------

        self.archivoEdicion=Menu(barraMenu, tearoff=0)
        self.archivoEdicion.add_command(label='Copiar')
        self.archivoEdicion.add_command(label='Pegar')
        self.archivoEdicion.add_command(label='Cortar')
        self.archivoEdicion.add_command(label='Editar')
        self.archivoEdicion.add_command(label='Marcar')

#!-------------------Herramientas--------------

        self.archivoHerramientas=Menu(barraMenu,tearoff=0)


#!-------------------Ayuda--------------

        self.archivoAyuda=Menu(barraMenu,tearoff=0)

        self.archivoAyuda.add_command(label='Acerca de',command=infoAdicional)
        self.archivoAyuda.add_command(label='Docum')
        self.archivoAyuda.add_command(label='Licencia',command=avisoLicencia)



        self.barraMenu.add_cascade(label='Archivo',menu=archivoMenu)
        self.barraMenu.add_cascade(label='Edicion',menu=archivoEdicion)
        self.barraMenu.add_cascade(label='Herramiendas',menu=archivoHerramientas)
        self.barraMenu.add_cascade(label='Ayuda',menu=archivoAyuda)








        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.BROWSE = Button(master, text="browse")
        self.BROWSE.pack()

        self.DISPLAY = Button(master, text="display")
        self.DISPLAY.pack()

        '''aca termina'''

    def greet(self):
        function()
    
    def extraer_archivos(self):
        pass

    def abrir_fichero(self):
        pass

    def number(self):
        pass
    
    def opciones_distribuciones(self):
        pass


botondias = Button(ventana, text='Abrir fichero', width = "15", height = "1", font = ("Calibri", 13), command=abrirFichero)
botondias.grid(column = 0, row = 0, padx = 7, pady = 10)



################### LEER LOS DOCUMENTOS .JSON ##########################3

"""
abrirFichero()
myjsonfile = open(fichero)
jsondata = myjsonfile.read()
json.loads(jsondata)
"""



def number(self):
    
    global hora
    try:
        int(box.get())
        hora = box.get()
        answer.config(text="Es un numero valido")
    except ValueError:
        answer.config(text= "No es un numero valido")
    print("El numero indicado es", hora)


label = Label(ventana, text= "Ingrese un numero entero entre 0 y 23")
label.grid(column = 1, row = 0, padx = 7, pady = 10)


#numeropantalla=StringVar()

box = Entry(ventana) #textvariable= numeropantalla)
box.grid(column = 1, row = 1, padx = 7, pady = 10)


boton = Button(ventana,text="Verificar el numero ingresado",command=number)
boton.grid(column = 1, row = 2, padx = 7, pady = 10)
answer = Label(ventana,text="")
answer.grid(column = 1, row = 3, padx = 7, pady = 10)



################ CHECK BUTTONS #############################33





def opcionesdistribuciones(self):
    
    opcionEscogida=''

    if(Norm.get()==1):
        opcionEscogida+='Norm   '

    if (Rayleigh.get()==1):
        opcionEscogida+='Rayleigh   '

    if (Burr12).get()==1:
        opcionEscogida+='Burr12   '
    
    if (Alpha).get()==1:
        opcionEscogida+='Alpha   '

    if (Gamma).get()==1:
            opcionEscogida+='Gamma   '
    if (Beta).get()==1:
            opcionEscogida+='Beta   '


    textoFinal.config(text=opcionEscogida)


#*agregar imagen 


foto=PhotoImage(file="large.png")


Label(ventana,image=foto).grid(column = 0, row = 1, padx = 7, pady = 10)

Label(ventana,text='ELIGE LAS DISTRIBUIONES DESEADAS', width = "50", height = "1", font = ("Calibri", 13)).grid(column = 0, row = 1, padx = 7, pady = 10)

textoFinal=Label(ventana)
textoFinal.grid(column = 0, row = 8, padx = 7, pady = 10)


#! FUNCION VENTANAS EMERGENTES

def infoAdicional(self):
    messagebox.showinfo('Procesador de Juan', 'Procesador de textos version 2020') #*primer y segundo parametro

def avisoLicencia(self):
    messagebox.showwarning('Licencia','Producto bajo licencia GNU')   #* cambia el icono del aviso

#? venta de salir con opciones si o no

def salirAplicacion(self):
    #  valor= messagebox.askquestion('Salir', 'Deseas salir de la aplicacion') #? botones de si o no 

    valor= messagebox.askokcancel('Salir', 'Deseas salir de la aplicacion')
    if valor==True:
        ventana.destroy()

'''
    if valor=='yes':
        root.destroy()
'''

#? Cerrar o reintentar un documento


def cerrarDocumento(self):
    valor= messagebox.askretrycancel('Reintentar', 'No es posible cerrar') 
    if valor==False:
        ventana.destroy()



#!--------------MENUS------------------

barraMenu=Menu(ventana)
ventana.config(menu=barraMenu, width=300,height=300) #* dar tamaño

archivoMenu=Menu(barraMenu,tearoff=0) #* quitar pestañá de defecto

#? sub elementos a las pestañas

#!-------------------Archivo--------------

archivoMenu.add_command(label='Nuevo')
archivoMenu.add_command(label='Guardar')
archivoMenu.add_command(label='Guardar como')

#* separar de submenus 
archivoMenu.add_separator()

archivoMenu.add_command(label='Cerrar', command=cerrarDocumento)
archivoMenu.add_command(label='Salir',command=salirAplicacion)


#!-------------------Edicion--------------

archivoEdicion=Menu(barraMenu, tearoff=0)
archivoEdicion.add_command(label='Copiar')
archivoEdicion.add_command(label='Pegar')
archivoEdicion.add_command(label='Cortar')
archivoEdicion.add_command(label='Editar')
archivoEdicion.add_command(label='Marcar')

#!-------------------Herramientas--------------

archivoHerramientas=Menu(barraMenu,tearoff=0)


#!-------------------Ayuda--------------

archivoAyuda=Menu(barraMenu,tearoff=0)

archivoAyuda.add_command(label='Acerca de',command=infoAdicional)
archivoAyuda.add_command(label='Docum')
archivoAyuda.add_command(label='Licencia',command=avisoLicencia)



barraMenu.add_cascade(label='Archivo',menu=archivoMenu)
barraMenu.add_cascade(label='Edicion',menu=archivoEdicion)
barraMenu.add_cascade(label='Herramiendas',menu=archivoHerramientas)
barraMenu.add_cascade(label='Ayuda',menu=archivoAyuda)




#! FUNCIONES DEL GUI   #############



########### FUNCIONES DE LA INTERFAZ ################

def abrirFichero(self):
    global fichero
    fichero=filedialog.askopenfilename(title='Abrir', #initialdir='/home/juanmanuel/Downloads',
    filetypes=(('Ficheros de demanda','*.json'),('Ficheros de Excel','*.xlsx'),('Ficheros de texto','*.txt'),('Todos los fichero','*.*')))  #* poner direccion del directorio
    
    
    print(fichero)
    
"""
abrirFichero()
myjsonfile = open(fichero)
jsondata = myjsonfile.read()
json.loads(jsondata)
"""
def number():
    
    global hora
    try:
        int(box.get())
        hora = box.get()
        answer.config(text="Es un numero valido")
    except ValueError:
        answer.config(text= "No es un numero valido")
    print("El numero indicado es", hora)


Norm=IntVar()
Rayleigh=IntVar()
Burr12=IntVar()
Alpha=IntVar()
Gamma=IntVar()
Beta=IntVar()


def opcionesdistribuciones():
    
    opcionEscogida=''

    if(Norm.get()==1):
        opcionEscogida+='Norm   '

    if (Rayleigh.get()==1):
        opcionEscogida+='Rayleigh   '

    if (Burr12).get()==1:
        opcionEscogida+='Burr12   '
    
    if (Alpha).get()==1:
        opcionEscogida+='Alpha   '

    if (Gamma).get()==1:
            opcionEscogida+='Gamma   '
    if (Beta).get()==1:
            opcionEscogida+='Beta   '


    textoFinal.config(text=opcionEscogida)


#*agregar imagen 

####################### MENU ###############



#! FUNCION VENTANAS EMERGENTES

def infoAdicional():
    messagebox.showinfo('Procesador de Juan', 'Procesador de textos version 2020') #*primer y segundo parametro

def avisoLicencia():
    messagebox.showwarning('Licencia','Producto bajo licencia GNU')   #* cambia el icono del aviso

#? venta de salir con opciones si o no

def salirAplicacion():
    #  valor= messagebox.askquestion('Salir', 'Deseas salir de la aplicacion') #? botones de si o no 

    valor= messagebox.askokcancel('Salir', 'Deseas salir de la aplicacion')
    if valor==True:
        ventana.destroy()

'''
    if valor=='yes':
        root.destroy()
'''

#? Cerrar o reintentar un documento


def cerrarDocumento():
    valor= messagebox.askretrycancel('Reintentar', 'No es posible cerrar') 
    if valor==False:
        ventana.destroy()





ventana.mainloop()


