﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import sys
import controller
import model
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import graph as gp
import time
import tracemalloc
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():

    print("Bienvenido")
    print("1- Inicializar el Analyzer")
    print("====================================================================")
    print("2- Cargar información en el Analyzer")
    print("====================================================================")
    print("3- Cantidad de clústers dentro de la red de cables submarinos") #REQUERIMIENTO-1
    print("====================================================================")
    print("4- Los landing points que sirven como ppunto de interconexión\n   a más cables en la red") #REQUERIMIENTO-2
    print("====================================================================")
    print("5- Ruta mínima en distancia para enviar inforamción entre dos países") #REQUERIMIENTO-3
    print("====================================================================")
    print("6- Identificar la infraestructura crítica para poder pgarantiar\n   el mantenimiento preventivo del mismo") #REQUERIMIENTO-4
    print("====================================================================")
    print("7- Impacto que podria tener el fallo de un determinado landing\n   point que afecta a todos los cables conectados al mismo") #REQUERIMIENTO-5
    print("====================================================================")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        cont = controller.init()

    elif int(inputs[0]) == 2:
        file_connections='connections.csv'
        file_countries='countries.csv'
        file_landing_points='landing_points.csv'
        
        print("Cargando información de los archivos ...")
        print('')

        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()

        controller.loadConnections(cont, file_connections)
        controller.loadCountries(cont, file_countries)
        controller.loadLandingPoints(cont, file_landing_points)
        last_country = controller.last_country_info(cont)
        total_landingPoints = controller.totalLandingPoints(cont)
        total_ConnectionsLP = controller.totalConnectionsLP(cont)
        first_landing_point = controller.first_landingP(cont)
        total_countries = controller.totalCountries(cont)

        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")

        print('-------------------------------')
        print('total de Landing Points: '+str(total_landingPoints))
        print('-------------------------------')
        print('total de conexiones entre Landing Points: '+str(total_ConnectionsLP))
        print('-------------------------------')
        print('El total de paises es: ' + str(total_countries))
        print('-------------------------------')
        print('Primer Landing Point Cargado')
        print('Landing Point id: '+first_landing_point[0]+'| nombre: '+first_landing_point[1]
        +'| latitud: '+first_landing_point[2]+'| longitud: '+first_landing_point[3])
        print('-------------------------------')
        print('Ultimo País Cargado')
        print('País: '+last_country[0]+'| Población: '+last_country[1]+ ' | Número de usuarios: '+last_country[2])
        print('-------------------------------')
        print('')
   

    elif int(inputs[0]) == 3:

        landing_point1 = input('Ingrese el nombre del landing point 1: ')
        landing_point2 = input('Ingrese el nombre del landing point 2: ')

        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()

        tupla_res=controller.req1(cont,landing_point1,landing_point2)
        
        if tupla_res[1]:
            print('El número total de clústeres presentes en la red es '+str(tupla_res[0])+' clústeres. Los dos landing points SI están en el mismo cluster.')
        elif not tupla_res[1]:
            print('El número total de clústeres presentes en la red es '+str(tupla_res[0])+' clústeres. Los dos landing points NO están en el mismo cluster.')
        
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")
    elif int(inputs[0]) == 4:
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        print("Los landing points que sirven como punto de interconexión a más cables en la red son: ")
        keys=mp.keySet(cont['interconnections'])
        for key in lt.iterator(keys):
            resultado=controller.req2(cont,key)
            if resultado is not None:
                print(resultado)
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")

        pass

    elif int(inputs[0]) == 5:
        
        paisA=input('Ingrese el país A: ')
        paisB=input('Ingrese el país B: ')
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()
        resultado=controller.req3(cont,paisA,paisB)
        if resultado is None:
            print('No se encontró camino entre los dos países ingresados.')
        else:
            print(resultado)
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")
        pass

    elif int(inputs[0]) == 6:
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()

        resultado=controller.req4(cont)
        print('Hay '+str(resultado[1])+' nodos conectados a la red de expansión mínima. La distancia total de la red de expansión mínima es de '+str(resultado[0])+' km.')
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")
        pass

    elif int(inputs[0]) == 7:
        
        landing_point=input('Teclee el landing point que tendría el fallo: ')
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = controller.getTime()
        start_memory = controller.getMemory()

        tupla=controller.req5(cont,landing_point)
        size=tupla[0]
        lista=tupla[1]
        print('Si el landing point ingresado falla, habrían '+str(size)+' países afectados. Estos serían: ')
        impresos=[]
        for i in lt.iterator(lista):
            cadena=i['country']+'. '+str(i['distance'])+' km de distancia del landing point ingresado.'
            pais=i['country']
            if pais not in impresos:
                print(cadena)
                impresos.append(pais)
        stop_memory = controller.getMemory()
        stop_time = controller.getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = controller.deltaMemory(start_memory, stop_memory)
        print('Tiempo[ms]: ', f"{delta_time:.3f}", "-", "Memoria [kB]: ", f"{delta_memory:.3f}")



        pass
    else:
        sys.exit(0)
sys.exit(0)
