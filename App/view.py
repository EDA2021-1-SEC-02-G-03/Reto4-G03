"""
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
    print("8- Ancho de banda máximo que se puede garantizar para la transmisión\n   a un servidor ubicado en el país") #REQUERIMIENTO-6
    print("====================================================================")
    print("9- Ruta mínima en número de saltos para enviar inforamción entre dos\n   direcciones IP dadas") #REQUERIMIENTO-7
    print("====================================================================")
    print("10- Graficar resultados") #REQUERIMIENTO-8
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
        #controller.first_landingP(cont)
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
        #print('-------------------------------')
        print('Landing Point id: '+first_landing_point[0]+'| nombre: '+first_landing_point[1]
        +'| latitud: '+first_landing_point[2]+'| longitud: '+first_landing_point[3])
        print('-------------------------------')
        print('Ultimo País Cargado')
        #print('-------------------------------')
        print('País: '+last_country[0]+'| Población: '+last_country[1]+ ' | Número de usuarios: '+last_country[2])
        print('-------------------------------')
        print('')
   

    elif int(inputs[0]) == 3:
        #TODO: Hay que hacerle algo a los landing points para que se revisen todos los landing points con la string de id.
        #Idea: crear un mapa que relacione landing point sin id con todos los landing points con ids y realizar el algoritmo
        # para cada uno de ellos.


        
        landing_point1 = input('Ingrese el nombre del landing point 1: ')
        landing_point2 = input('Ingrese el nombre del landing point 2: ')

        tupla_res=controller.req1(cont,landing_point1,landing_point2)

        if tupla_res[1]:
            print('El número total de clústeres presentes en la red es '+str(tupla_res[0])+' clústeres. Los dos landing points SI están en el mismo cluster.')
        elif not tupla_res[1]:
            print('El número total de clústeres presentes en la red es '+str(tupla_res[0])+' clústeres. Los dos landing points NO están en el mismo cluster.')
    elif int(inputs[0]) == 4:
        '''
        keys=mp.valueSet(cont['name_landing_id_hash'])
        for i in lt.iterator(keys):
            print(i)
        '''

        print("Los landing points que sirven como punto de interconexión a más cables en la red son: ")
        keys=mp.keySet(cont['interconnections'])
        for key in lt.iterator(keys):
            resultado=controller.req2(cont,key)
            if resultado is not None:
                print(resultado)

        pass

    elif int(inputs[0]) == 5:
        
        paisA=input('Ingrese el país A: ')
        paisB=input('Ingrese el país B: ')
        resultado=controller.req3(cont,paisA,paisB)
        if resultado is None:
            print('No se encontró camino entre los dos países ingresados.')
        else:
            print(resultado)

        '''
        keys=mp.keySet(cont['country-landing_points'])
        for i in lt.iterator(keys):
            print(i)
        '''
        
        pass

    elif int(inputs[0]) == 6:
        #Árbol de Recubrimiento de Costo Mínimo
        controller.req4(cont)
        
        pass

    elif int(inputs[0]) == 7:
        pass

    elif int(inputs[0]) == 8:
        pass

    elif int(inputs[0]) == 9:
        pass

    elif int(inputs[0]) == 10:
        pass

    else:
        sys.exit(0)
sys.exit(0)
