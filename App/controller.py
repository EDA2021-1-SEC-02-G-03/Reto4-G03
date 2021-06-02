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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# def newAnalyzer():
#     model.newAnalyzer()



# Inicialización del Catálogo de libros

def init():

    analyzer = model.newAnalyzer()
    return analyzer

def loadConnections(analyzer, connections_file):

    connections_file = cf.data_dir + connections_file
    input_file = csv.DictReader(open(connections_file, encoding='utf-8-sig'), delimiter=',')
    #lastLandPoint = None
    for connection in input_file:
        #if lastLandPoint is not None:
            # samePointOrigin = lastLandPoint['origin'] == landPoint['origin']
            # samePointDestination = lastLandPoint['destination'] == landPoint['destination']
            # LandingPointId = lastLandPoint['']
        model.addLandingPoint(analyzer, connection)
    return analyzer

def loadCountries(analyzer, countries_file):
    countries_file = cf.data_dir + countries_file
    input_file = csv.DictReader(open(countries_file, encoding='utf-8-sig'), delimiter=',')
    for country in input_file:
        model.addCountry(analyzer, country)
    return analyzer

#########
#TESTING#
#########

# def Manual_testing(countries_file):
#     checker = {}
#     countries_file = cf.data_dir + countries_file
#     input_file = csv.DictReader(open(countries_file, encoding='utf-8-sig'), delimiter=',')
#     for landing_point in input_file:
#         data = landing_point['name'].split(',')[0]
#         print(data)
#         try:
#             checker[data] = 1
#         except:
#             checker[data] = 0

#     print(len(checker))
        
    
#Manual_testing('landing_points.csv')

def loadLandingPoints(analyzer, landingPoints_file):
    landingPoints_file = cf.data_dir + landingPoints_file
    input_file = csv.DictReader(open(landingPoints_file, encoding='utf-8-sig'), delimiter=',')
    for landingP in input_file:
        model.addLandingPoint_data(analyzer, landingP)
    return analyzer


def totalLandingPoints(analyzer):
    return model.totalLandPoints(analyzer)

def totalConnectionsLP(analyzer):
    return model.totalConnectionsLP(analyzer)

def totalCountries(analyzer):
    return model.total_countries(analyzer)

def last_country_info(analyzer):
    return model.last_country_info(analyzer)

def first_landingP(analyzer):
    return model.first_landingP(analyzer)

def connectedComponents(analyzer):
    return model.find_connectedComponents(analyzer)

def paths_landingPoint1(analyzer, origin_landingP):
    return model.paths_landingPoint1(analyzer, origin_landingP)

def exist_path_landingPoint2(analyzer, dest_landingP):
    return model.exist_path_landingPoint2(analyzer, dest_landingP)

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
