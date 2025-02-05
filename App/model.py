﻿"""
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
from DISClib.Algorithms.Sorting import mergesort as mgs
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk 
from DISClib.Utils import error as error
from DISClib.ADT import stack as stk
from DISClib.ADT import queue as qu
from DISClib.Algorithms.Graphs import prim
from DISClib.DataStructures import bst
assert cf


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

def addLandingPointNormal(analyzer,connections):
    try:
        origin = connections['origin']
        destination = connections['destination']
        distance = convert_distance(connections['cable_length'])
        addLandPointNormal(analyzer, origin)
        addLandPointNormal(analyzer, destination)
        addConnectionNormal(analyzer, origin, destination, distance)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandConnectionNormal')


def addInterconnection(analyzer,connection):
    if not mp.contains(analyzer['interconnections'], connection['origin']):
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

def addConnectionNormal(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['connections_normal'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections_normal'], origin, destination, distance)
    return analyzer 

def addLandPoint(analyzer, LandPoint):
    try:
        if not gr.containsVertex(analyzer['connections'], LandPoint):
            gr.insertVertex(analyzer['connections'], LandPoint)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandPoint')

def addLandPointNormal(analyzer,LandPoint):
    try:
        if not gr.containsVertex(analyzer['connections_normal'], LandPoint):
            gr.insertVertex(analyzer['connections_normal'], LandPoint)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandPointNormal')

def convert_distance(cable_length):
   dato=cable_length.replace(',', '').split(' ')[0]
   if dato=='n.a.':
       return 0
   else:
       return float(dato)

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

def req1(analyzer,landingp1,landingp2):
    kosaraju=scc.KosarajuSCC(analyzer['connections_normal'])
    num_clusters=kosaraju['components']
    origin=str(cityname_to_id(analyzer,landingp1))
    destination=str(cityname_to_id(analyzer,landingp2))
    estan_o_no=scc.stronglyConnected(kosaraju,origin,destination)
    return (num_clusters,estan_o_no)

def req2(analyzer,key):
    entry=mp.get(analyzer['interconnections'],key)
    lista=me.getValue(entry)
    numero=lt.removeFirst(lista)
    if numero > 1:
        entry1=mp.get(analyzer['name_landing_id_hash'],key)
        lt.addFirst(lista,numero)
        return me.getValue(entry1)+'. ID: '+key+'. Total de cables conectados: '+str(numero)

def req3(analyzer,paisA,paisB):

    menor_distancia=-150
    menor_origin=''
    menor_destination=''

    landingpointsA=get_landing_points_by_country(analyzer,paisA)
    landingpointsB=get_landing_points_by_country(analyzer,paisB)
    
    #Iteración: Se tienen en cuenta todos los landingpoints del pais A y del pais B.
    for landingpointA in lt.iterator(landingpointsA):
        verticesA=get_list_of_vertices(analyzer,landingpointA)
        for landingpointB in lt.iterator(landingpointsB):
            verticesB=get_list_of_vertices(analyzer,landingpointB)
    #Fin de iteración de landingpoints de ambos países. 
            for origin in lt.iterator(verticesA):
                busqueda=djk.Dijkstra(analyzer['connections'],origin)
                for destination in lt.iterator(verticesB):
                    dist=float(djk.distTo(busqueda,destination))
                    if (dist<menor_distancia or menor_distancia==-150) and dist!='inf':
                        menor_distancia=dist
                        menor_origin=origin
                        menor_destination=destination
                        pathTo=djk.pathTo(busqueda,destination)
    cadena=None
    distanciatotal=0
    if pathTo is not None:
        cadena=''
        while not stk.isEmpty(pathTo):
            dicti=stk.pop(pathTo)
            vertexA_origin=dicti['vertexA'].split('_')[0]
            vertexB_origin=dicti['vertexB'].split('_')[0]
            weight=str(dicti['weight'])
            distanciatotal+=float(weight)
            vertexA=get_landingpointname_by_id(analyzer,vertexA_origin)
            vertexB=get_landingpointname_by_id(analyzer,vertexB_origin)
            cadena+='De '+vertexA+' a '+vertexB+'. Distancia entre los landing points: '+weight+' km. \n'
    
        return cadena+'\nLa distancia total es de '+str(distanciatotal)+' km.'
    else:
        return None

def req4(analyzer):
    search=prim.PrimMST(analyzer['connections_normal'])
    distance=prim.weightMST(analyzer['connections_normal'],search)
    mst=search['mst']
    numberofnodes=qu.size(mst)
    return(distance,numberofnodes)

def req5(analyzer,landingP):
    ident=cityname_to_id(analyzer,landingP)
    list_of_vertices=get_list_of_vertices(analyzer,ident)
    affected_countries=lt.newList('ARRAY_LIST')
    for vertex in lt.iterator(list_of_vertices):
        adjacents=gr.adjacentEdges(analyzer['connections'],vertex)
        for adjacent in lt.iterator(adjacents):
            ident1=adjacent['vertexB'].split('_')[0]
            aux=get_landingpointname_by_id(analyzer,ident1).split(',')
            if len(aux)>2:
                country=aux[2][1:]
            else:
                country=aux[1][1:]
            distance=adjacent['weight']
            dato={'distance':distance,'country':country}
            esta=False
            for t in lt.iterator(affected_countries):
                if t==dato:
                    esta=True
            if not esta:
                lt.addLast(affected_countries,dato)
    affected=mgs.sort(affected_countries,cmp_function_req5)
    return (lt.size(affected),affected)

    
def cmp_function_req5(dato1,dato2):
    return(dato1['distance']>dato2['distance'])



def country_to_capital(analyzer,country_name):
    entry=mp.get(analyzer['countries_map'],country_name)
    hash_t=me.getValue(entry)
    entry=mp.get(hash_t,'Capital')
    return me.getValue(entry)
   
def cityname_to_id(analyzer,city_name):
    entry=mp.get(analyzer['landing_name_id_hash_no_country'],city_name)
    return me.getValue(entry)

def get_list_of_vertices(analyzer,vertex):
    entry=mp.get(analyzer['id_name+id_hash'],vertex)
    return me.getValue(entry)

def get_landing_points_by_country(analyzer,country_name):
    entry=mp.get(analyzer['country-landing_points'],country_name)
    return me.getValue(entry)

def get_landingpointname_by_id(analyzer,landingpointid):
    entry=mp.get(analyzer['name_landing_id_hash'],landingpointid)
    return me.getValue(entry)

def compareLandingPoints(value, keyValue):
    value_land = keyValue['key']
    if (value == value_land):
        return 0
    elif (value > value_land):
        return 1
    else:
        return -1

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

        analyzer['landing_name_id_hash_no_country']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['name_landing_id_hash']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['id_name+id_hash']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['country-landing_points']=mp.newMap(numelements=20000,maptype='PROBING')

        analyzer['landing_points_data'] = lt.newList('ARRAY_LIST')
        
        analyzer['countries'] = lt.newList('ARRAY_LIST')

        analyzer['countries_map'] = mp.newMap(numelements=500,maptype='PROBING')

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size = 20000,
                                              comparefunction=compareLandingPoints
                                              )
        analyzer['connections_normal']=gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size = 20000,
                                              comparefunction=compareLandingPoints
                                              )
        #Los vértices del grafo connections son landing point id + _ + cable id
        

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def addCountryMap(analyzer,country):
    if not mp.contains(analyzer['countries_map'],country['CountryName']):
        datos=mp.newMap(numelements=10,maptype='PROBING')
        mp.put(datos,'Capital',country['CapitalName'])
        mp.put(datos,'Latitude',country['CapitalLatitude'])
        mp.put(datos,'Longitude',country['CapitalLongitude'])
        mp.put(analyzer['countries_map'], country['CountryName'], datos)

def addLandingPCountry(analyzer,landingP):
    country1=landingP['name'].split(',')
    if len(country1)>2:
        country=country1[2][1:]
        if not mp.contains(analyzer['country-landing_points'],country):
            lista=lt.newList('ARRAY_LIST')
            lt.addLast(lista,landingP['landing_point_id'])
            mp.put(analyzer['country-landing_points'],country,lista)
        else:
            entry=mp.get(analyzer['country-landing_points'],country)
            lista=me.getValue(entry)
            lt.addLast(lista,landingP['landing_point_id'])
            mp.put(analyzer['country-landing_points'],country,lista)
    elif len(country1)>1:
        country=country1[1][1:]
        if not mp.contains(analyzer['country-landing_points'],country):
            lista=lt.newList('ARRAY_LIST')
            lt.addLast(lista,landingP['landing_point_id'])
            mp.put(analyzer['country-landing_points'],country,lista)
        else:
            entry=mp.get(analyzer['country-landing_points'],country)
            lista=me.getValue(entry)
            lt.addLast(lista,landingP['landing_point_id'])
            mp.put(analyzer['country-landing_points'],country,lista)
    


def landing_points_hash_table(analyzer,landing_point):
    name=landing_point['name']
    land_id=landing_point['landing_point_id']
    if not mp.contains(analyzer['landing_name_id_hash'],name):
        mp.put(analyzer['landing_name_id_hash'],name,land_id)

def landing_points_hash_no_country(analyzer,landing_point):
    name=landing_point['name'].split(',')[0]
    land_id=landing_point['landing_point_id']
    if not mp.contains(analyzer['landing_name_id_hash_no_country'],name):
        mp.put(analyzer['landing_name_id_hash_no_country'],name,land_id)
    

def origin_hash_table(analyzer,landing_point):
    name=landing_point['name']
    land_id=landing_point['landing_point_id']
    if not mp.contains(analyzer['name_landing_id_hash'],land_id):
        mp.put(analyzer['name_landing_id_hash'],land_id,name)

    


