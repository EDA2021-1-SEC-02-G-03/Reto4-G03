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
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk 
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


def addLandingPoint(analyzer, connections):
    
    try:
        origin = connections['origin']+'_'+connections['cable_id']
        destination = connections['destination']+'_'+connections['cable_id']
        distance = convert_distance(connections['cable_length'])
        addLandPoint(analyzer, origin)
        addLandPoint(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        if not mp.contains(analyzer['id_name+id_hash'],connections['origin']):
            lista=lt.newList('ARRAY_LIST')
            lt.addLast(lista, origin)
            mp.put(analyzer['id_name+id_hash'],connections['origin'],lista)
        else:
            entry=mp.get(analyzer['id_name+id_hash'],connections['origin'])
            lista=me.getValue(entry)
            if not lt.isPresent(lista,origin):
                lt.addLast(lista,origin)
                mp.put(analyzer['id_name+id_hash'],connections['origin'],lista)

        if not mp.contains(analyzer['id_name+id_hash'],connections['destination']):
            lista=lt.newList('ARRAY_LIST')
            lt.addLast(lista, destination)
            mp.put(analyzer['id_name+id_hash'],connections['destination'],lista)
        else:
            entry=mp.get(analyzer['id_name+id_hash'],connections['destination'])
            lista=me.getValue(entry)
            if not lt.isPresent(lista,destination):
                lt.addLast(lista,destination)
                mp.put(analyzer['id_name+id_hash'],connections['destination'],lista)
        addInterconnection(analyzer,connections)


        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandConnection')

def addInterconnection(analyzer,connection):
    if not mp.contains(analyzer['interconnections'], connection['origin']):
        #El primer elemento de la lista contiene la cantidad de cables. Los demás elementos son los cables.
        lista=lt.newList('ARRAY_LIST')
        lt.addLast(lista,1)
        lt.addLast(lista,connection['cable_id'])
        mp.put(analyzer['interconnections'],connection['origin'],lista)
    elif mp.contains(analyzer['interconnections'], connection['origin']):
        entry=mp.get(analyzer['interconnections'],connection['origin'])
        lista=me.getValue(entry)
        esta=False
        for i in lt.iterator(lista):
            if i==connection['cable_id']:
                esta=True
        if not esta:
            numero=lt.removeFirst(lista)
            numero+=1
            lt.addFirst(lista,numero)

def addCountry(analyzer, country):
    lt.addLast(analyzer['countries'], country)

def addLandingPoint_data(analyzer, LandingPoint):
    lt.addLast(analyzer['landing_points_data'], LandingPoint)

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

def total_countries(analyzer):
    return lt.size(analyzer['countries'])

def last_country_info(analyzer):
    info = lt.getElement(analyzer['countries'], lt.size(analyzer['countries']))
    return info['CountryName'], info['Population'], info['Internet users']

def first_landingP(analyzer):
    info = lt.getElement(analyzer['landing_points_data'], 1)
    return info['landing_point_id'], info['name'], info['latitude'], info['longitude']

def find_connectedComponents(analyzer):

    analyzer['connections'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.sccCount(analyzer['connections'])

def paths_landingPoint1(analyzer, origin_landingP):
    #Llamar a la funcion paths landing point 1 con todos los vertices de dicho landing point
    analyzer['clusters']=[]
    landingpoints=mp.keySet(analyzer['landing_name_id_hash'])
    origin_landingP=lt.getElement(landingpoints,1)
    entry=mp.get(analyzer['landing_name_id_hash'],origin_landingP)
    origin_id=me.getValue(entry)
    entry=mp.get(analyzer['id_name+id_hash'],origin_id)
    lista=me.getValue(entry)
    for origin in lt.iterator(lista):
        print(origin)
        analyzer['clusters'].append(djk.Dijkstra(analyzer['connections'], origin))
    return analyzer

def exist_path_landingPoint2(analyzer, dest_landingP):
    return djk.hasPathTo(analyzer['connections'], dest_landingP)

def req2(analyzer,key):
    #keys=mp.keySet(analyzer['interconnections'])
    #for key in lt.iterator(keys):
    entry=mp.get(analyzer['interconnections'],key)
    lista=me.getValue(entry)
    numero=lt.removeFirst(lista)
    if numero > 1:
        entry1=mp.get(analyzer['name_landing_id_hash'],key)
        lt.addFirst(lista,numero)
        return me.getValue(entry1)+'. ID: '+key+'. Total de cables conectados: '+str(numero)
   
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


#Funciones Creadas por Juan Andrés
def newAnalyzer():
    try:
        analyzer = {
                    'connections':None,
                    'landing points':None,
                    'countries':None,
                    'clusters':None
                    }
        
        analyzer['interconnections']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['landing_name_id_hash']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['name_landing_id_hash']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['id_name+id_hash']=mp.newMap(numelements=20000,maptype='PROBING')

        #TODO: Este mapa de 'LandPoints_Vertex' esta vacio
        analyzer['LandPoints_Vertex'] = mp.newMap(numelements=20000,
                                           maptype='PROBING'
                                           )
        analyzer['landing_points_data'] = lt.newList('ARRAY_LIST')
        
        analyzer['countries'] = lt.newList('ARRAY_LIST')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size = 20000,
                                              comparefunction=compareLandingPoints
                                              )
        #Los vértices del grafo connections son landing point id + _ + cable id
        #TODO: Crear mapa que relacione landing point name con todos los posibles vertices de dicho landing point para el grafo.

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

def landing_points_hash_table(analyzer,landing_point):
    name=landing_point['name']
    land_id=landing_point['landing_point_id']
    if not mp.contains(analyzer['landing_name_id_hash'],name):
        mp.put(analyzer['landing_name_id_hash'],name,land_id)

def origin_hash_table(analyzer,landing_point):
    name=landing_point['name']
    land_id=landing_point['landing_point_id']
    if not mp.contains(analyzer['name_landing_id_hash'],land_id):
        mp.put(analyzer['name_landing_id_hash'],land_id,name)

    


