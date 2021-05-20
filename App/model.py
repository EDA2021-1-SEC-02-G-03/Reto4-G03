"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT.graph import gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def newAnalyzer():
    try:
        analyzer = {
                    'connections':None,
                    'landing points':None,
                    'countries':None
                    }

        analyzer['LandPoints_Vertex'] = mp.newMap(numelements=20000,
                                           maptype='PROBING'
                                           )

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size = 20000,
                                              comparefunction=compareLandingPoints
                                              )

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def addLandingPoint(analyzer, connections):
    
    try:
        origin = connections['origin']
        destination = connections['destination']
        distance = convert_distance(connections['cable_length'])
        addLandPoint(analyzer, origin)
        addLandPoint(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        # addLandPointVertex(analyzer, origin)
        # addLandPointVertex(analyzer, destination)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandConnection')

# def addLandPointVertex(analyzer, LandPoint):
#     entry = mp.get(analyzer['LandPoints_Vertex'], LandPoint)
#     if entry is None:
#         lstConnections = lt.newList('ARRAY_LIST')
#         lt.addLast(lstConnections, )
#     pass

def addConnection(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer 

def addLandPoint(analyzer, LandPoint):
    try:
        if not gr.containsVertex(analyzer['connections'], LandPoint):
            gr.insertVertex(analyzer['connections'], LandPoint)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandPoint')

def convert_distance(cable_length):
   return cable_length.replace(',', '').split(' ')[0]

def totalLandPoints(analyzer):
    return gr.numVertices(analyzer['connections'])

def totalConnectionsLP(analyzer):
    return gr.numEdges(analyzer['connections'])

# Construccion de modelos
#print(convert_distance('31,000 km'))

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareLandingPoints(value, keyValue):
    value_land = keyValue['key']
    if (value == value_land):
        return 0
    elif (value > value_land):
        return 1
    else:
        return -1

# Funciones de ordenamiento
