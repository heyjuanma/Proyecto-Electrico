### Primer bloque de la construccion:

## Parte Lógica

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime
import pandas as pd
import numpy as np
from datetime import datetime

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

#################SOLICITUDES USUARIO ###########

# Hora, en el intervalo [0, 23] (tipo int)


hora = 12



# Distribuciones a evaluar
distribuciones = ['norm', 'rayleigh', 'burr12', 'alpha', 'gamma', 'beta']

# Llamar a las funciones
demandas = extraer_datos('demanda_2019.json', hora)
evaluar_modelos(demandas, distribuciones, 25, hora)

