
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import datetime

from tkinter import *
from tkinter import ttk
from tkinter import filedialog   #* ventanas emergentes
import json
from tkinter import messagebox  #* ventanas emergentes



def extraer_datos(archivo_json, hora):
    '''Importa la base de datos completa y devuelve los
    datos de potencia a la hora indicada en un
    array de valores.
    '''
    
    # Cargar el "DataFrame"
    df = pd.read_json(archivo_json) 
    
    # Convertir en un array de NumPy
    datos = np.array(df)                

    # Crear vector con los valores demanda en una hora
    demanda = []

    # Extraer la demanda en la hora seleccionada
    for i in range(len(datos)):
        instante = datetime.fromisoformat(datos[i][0]['fechaHora'])
        if instante.hour == hora:
            demanda.append(datos[i][0]['MW'])

    return demanda



def evaluar_modelos(datos, distribuciones, divisiones, hora):
    '''Evalúa la bondad de ajuste de los datos con los 
    modelos utilizados y grafica cada modelo.
    '''
    
    # Distribución de frecuencia relativa
    ocurrencias_exp, limites = np.histogram(datos, bins=divisiones)
    
    # Eliminar los ceros de la frecuencia relativa
    for i in range(divisiones):
        if ocurrencias_exp[i] == 0:
            ocurrencias_exp[i] = 1
    
    # Encontrar el valor central de las divisiones
    bins_centrados = (limites + np.roll(limites, -1))[:-1] / 2.0 
    escala = len(datos) * (max(datos) - min(datos)) / len(bins_centrados)
    
    # Crear subfiguras para visualización (1 x 2)
    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    # Información de la figura 1
    ax[0].set_title('Ajuste de las distribuciones')
    ax[0].set_ylabel('Frecuencia')
    ax[0].set_xlabel('Potencia [MW]')
    # Información de la figura 3
    ax[1].set_title('Distribución con mejor criterio de bondad de ajuste')
    ax[1].set_ylabel('Frecuencia')
    ax[1].set_xlabel('Potencia [MW]')
    
    # Visualizar datos
    ax[0].hist(datos, bins=divisiones, histtype='bar', color='palevioletred', rwidth=0.8)
    ax[1].hist(datos, bins=divisiones, histtype='bar', color='b')
    
    # Condiciones iniciales de las pruebas de ajuste
    rmse_min = np.inf  # el mayor índice de error
    p_max = 0          # el mejor p en chisqr test (0 es el "peor")
    kspmax = 0         # el mejor p en KStest (0 es el "peor")
    np.seterr(all='ignore') # ignorar errores con números de punto flotante

    # Evaluar las distribuciones, extraer parámetros y visualizar
    for distribucion in distribuciones:
        # Extraer de scipy.stats la distribución ("get attribute")
        dist = getattr(stats, distribucion) 
        
        # Parámetros de mejor ajuste para la distribución
        param = dist.fit(datos)
        
        # Evaluar la PDF en el valor central de las divisiones
        pdf = dist.pdf(bins_centrados, *param)
        
        # Convertir frecuencia relativa en ocurrencias (número absoluto)
        ocurrencias_teo = [int(round(i)) for i in escala*pdf]
        
        # Soporte para la gráfica
        d = np.arange(min(datos)*0.96, max(datos)*1.04, 1)
        
        # Graficar en ax[1]
        pdf_plot = dist.pdf(d, *param)
        ax[0].plot(d, escala*pdf_plot, lw=3.5, label='{}'.format(distribucion))

        # Prueba de bondad de ajuste por chi-cuadrado
        coef_chi, p = stats.chisquare(f_obs=ocurrencias_teo, f_exp=ocurrencias_exp)
        if p > p_max:  # si el p actual es mayor
            p_max = p  # designarlo como el máximo
            dist_chi = distribucion # elegir la distribución como la de mejor ajuste
            mod_chi = dist, param, pdf

        # Bondad de ajuste por RMSE (Root-Mean-Square Error)
        diferencia = (ocurrencias_teo - ocurrencias_exp)**2
        rmse = np.sqrt(np.mean(diferencia))
        if rmse < rmse_min:
            rmse_min = rmse
            dist_rmse = distribucion
            mod_rmse = dist, param, pdf

        # Bondad de ajuste por Kolgomorov - Smirnov
        D, ksp = stats.kstest(datos, distribucion, args=param)
        if ksp > kspmax:
            kspmax = ksp
            dist_ks = distribucion

    # Decidir el mejor modelo
    if dist_chi == dist_rmse or dist_chi == dist_ks:
        params = mod_chi[1]
        mejor_ajuste = dist_chi
        ax[1].hist(datos, bins=divisiones, color='cornflowerblue', label='Distribución observada')
        ax[1].bar(bins_centrados, mod_chi[2] * escala, width=6, color='r', label='Mejor ajuste: {}'.format(dist_chi))
        m, v, s, k = mod_chi[0].stats(*params, moments='mvsk') 

    elif dist_rmse == dist_ks:
        params = mod_rmse[1]
        mejor_ajuste = dist_rmse
        ax[1].hist(datos, bins = divisiones, color='cornflowerblue', label='Distribución observada')
        ax[1].bar(bins_centrados, mod_rmse[2] * escala, width=6, color='r', label='Mejor ajuste: {}'.format(dist_rmse))
        m, v, s, k = mod_rmse[0].stats(*params, moments='mvsk')

    # Imprimir resumen y resultados
    print('-------\nResumen\n-------')
    print('Cantidad de muestras:', len(datos), 'días a las', hora, 'horas')
    print('Máximo:', max(datos), 'MW')
    print('Mínimo:', min(datos), 'MW')
    print('Tipo: Demanda energética horaria')
    print('------\nAjuste\n------')
    print('Menor error RMS es:', dist_rmse)
    print('Mejor bondad de ajuste en la prueba de chi-cuadrado es:', dist_chi)
    print('Mejor bondad de ajuste en la prueba de Kolmogorov–Smirnov es:', dist_ks)
    print('Distribución elegida:', mejor_ajuste)
    print('--------\nMomentos\n--------')
    print('Media:', m, '\nVarianza:', v, '\nDesviación estándar:', np.sqrt(v), '\nCoeficiente simetría:', s, '\nKurtosis:', k)
    print('--------\nGráficas\n--------')
    
    ax[0].legend()
    ax[1].legend()
    plt.show()



##################### INICIO DE LA INTERFAZ #########33###########


global ventana
global nombreDelArchivo



nombreDelArchivo = ""
ventana = Tk()
cuadro = Frame(ventana)
cuadro.grid()
ventana.geometry("750x550")
ventana.title("Análisis de datos de consumo de energía ")


def abrirFichero():
    global fichero
    fichero=filedialog.askopenfilename(title='Abrir', #initialdir='/home/juanmanuel/Downloads',
    filetypes=(('Ficheros de demanda','*.json'),('Ficheros de Excel','*.xlsx'),('Ficheros de texto','*.txt'),('Todos los fichero','*.*')))  #* poner direccion del directorio
    
    
    print(fichero)


botondias = Button(ventana, text='Abrir fichero', width = "15", height = "1", font = ("Calibri", 13), command=abrirFichero)
botondias.grid(column = 0, row = 0, padx = 7, pady = 10)



################### LEER LOS DOCUMENTOS .JSON ##########################3

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


foto=PhotoImage(file="large.png")


Label(ventana,image=foto).grid(column = 0, row = 1, padx = 7, pady = 10)




Label(ventana,text='ELIGE LAS DISTRIBUIONES DESEADAS', width = "50", height = "1", font = ("Calibri", 13)).grid(column = 0, row = 1, padx = 7, pady = 10)

textoFinal=Label(ventana)
textoFinal.grid(column = 0, row = 8, padx = 7, pady = 10)



Checkbutton(ventana, text='Norm ',variable=Norm,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 2, padx = 7, pady = 10)
Checkbutton(ventana, text='Rayleigh ',variable=Rayleigh,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 3, padx = 7, pady = 10)
Checkbutton(ventana, text='Burr12 ',variable=Burr12,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 4, padx = 7, pady = 10)
Checkbutton(ventana, text='Alpha ',variable=Alpha,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 5, padx = 7, pady = 10)
Checkbutton(ventana, text='Gamma ',variable=Gamma,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 6, padx = 7, pady = 10)
Checkbutton(ventana, text='Beta ',variable=Beta,onvalue=1, offvalue=0,command=opcionesdistribuciones).grid(column = 0, row = 7, padx = 7, pady = 10)



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


ventana.mainloop()



#################SOLICITUDES USUARIO ###########

# Hora, en el intervalo [0, 23] (tipo int)


hora = 12



# Distribuciones a evaluar
distribuciones = ['norm', 'rayleigh', 'burr12', 'alpha', 'gamma', 'beta']

# Llamar a las funciones
demandas = extraer_datos('demanda_2019.json', hora)
evaluar_modelos(demandas, distribuciones, 25, hora)



