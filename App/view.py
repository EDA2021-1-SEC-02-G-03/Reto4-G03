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

#from App.model import total_countries
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    # print("Bienvenido")
    # print("1- Inicializar el analizador")
    # print("2- Cargar información en el analizador")
    # print('3- Determinar si dos landing points están conectados')
    # print('4- Landing points que sirven como punto de interconexión')
    # print('5- Ruta mínima para enviar información entre dos países')
    # print('6- Identificar red de expansión mínima')
    # print('7- Países afectados con la caída de un landing point')
    # print('8- Ancho de banda máximo')
    # print('9- Ruta mínima entre dos direcciones IP')
    # print('10- Gráfica de resultados')

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
        controller.loadConnections(cont, file_connections)
        controller.loadCountries(cont, file_countries)
        controller.loadLandingPoints(cont, file_landing_points)
        last_country = controller.last_country_info(cont)
        total_landingPoints = controller.totalLandingPoints(cont)
        total_ConnectionsLP = controller.totalConnectionsLP(cont)
        first_landing_point = controller.first_landingP(cont)
        #controller.first_landingP(cont)
        total_countries = controller.totalCountries(cont)
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
        pass

    elif int(inputs[0]) == 4:
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
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
