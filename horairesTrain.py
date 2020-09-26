#!/usr/bin/env python3
# -*- coding: latin-1 -*-

token_auth = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
baseUrl = 'https://api.sncf.com/v1/coverage/sncf/'

import requests
from requests.exceptions import RequestException
import json
from datetime import datetime, timedelta
import pprint
import pandas

def substr(string, start, length = None):
    if start < 0:
        start = start + len(string)
    if not length:
        return string[start:]
    elif length > 0:
        return string[start:start + length]
    else:
        return string[start:length]
        
        
def convertir_en_chaine(dt) :
    ''' on convertit en chaîne de caractères un datetime'''
    return datetime.strftime(dt, '%Y%m%dT%H%M%S')
def convertir_en_temps(chaine) :
    ''' on convertit en date la chaine de caractères de l API'''
    return datetime.strptime(chaine.replace('T',''),'%Y%m%d%H%M%S')

def requetGet(command, param):
    try:         
        ret = requests.get(baseUrl + command, params=param, auth = (token_auth, ''))
        # return ret
        return json.loads(ret.content.decode()) 
    except RequestException as e:
        print(e)
        return None
        
param={'from' : 'admin:fr:30189', 'to' : 'admin:fr:34172', 'datetime' : convertir_en_chaine(datetime.now()), 'datetime_represents' : 'departure', 'min_nb_journeys' : 10, 'timeout' : 3} 
resultats = requetGet('journeys', param)     

result = ''

for trains in resultats['journeys']:
    # print(trains)
    dateDepart = trains['departure_date_time']
    HeuredeDepart = substr(dateDepart,9,4)
    print('Heure de depart: ' + substr(HeuredeDepart,0,2) + 'h' + substr(HeuredeDepart,2,2))

    dateArrive = trains['arrival_date_time']
    heuredarrive = substr(dateArrive,9,4)
    print("Heure d'arrive: " + substr(heuredarrive,0,2) + 'h' + substr(heuredarrive,2,2))
    
    duree = trains['durations']['total']
    print('Durée : ' + str(int(duree/60)) + 'mn')
    
    numtrain = trains['sections'][1]['display_informations']['headsign']
    print('Numero de train: ' + numtrain)
    
    typetrain = trains['sections'][1]['display_informations']['commercial_mode']
    print('Type de train: ' + typetrain)
    
    directrain = trains['sections'][1]['display_informations']['direction']
    print('Direction du train: ' + directrain)
    
    
    
    if trains['status'] != "" :
        retard = ''
        text = ''
        print('Statut du train: ' + trains['status'])
        if trains['status'] == 'NO_SERVICE':
            print("************TRAINS*************")
            continue
        
        numdisrup = trains['sections'][1]['display_informations']['links'][0]['id']
        # print('ID de retard: ' + numdisrup)
        
        retards = resultats['disruptions']

        for retard in retards:
            # print('ID de retard dans les retards: ' + retard['disruption_id'])
        
            if retard['disruption_id'] == numdisrup:			
                for impactStop in retard['impacted_objects'][0]['impacted_stops']:
                    if substr(impactStop['base_departure_time'],0,4) == HeuredeDepart:
  
                        updatetime = impactStop['amended_departure_time']
                        print('Nouvelle heure de depart: ' + substr(updatetime,0,2) + 'h' + substr(updatetime,2,2))
                        
                        retard =  (int(substr(updatetime,0,2)) * 60 + int(substr(updatetime,2,2))) - (int(substr(HeuredeDepart,0,2)) * 60 + int(substr(HeuredeDepart,2,2)))
                       
                        print('Retard : ' + str(retard) + 'mn')
                        text = '-' + str(retard) + 'mn, '; 
                        break;
    else:
        text = ', ' 
    print()
    result = result + substr(HeuredeDepart,0,2) + 'h' + substr(HeuredeDepart,2,2) + text
    print("************TRAINS*************")
	
	
result = substr(result,0,-2)
print("Resultat: " + result)

param2 = {'headsign' : '876554', 'since' : '20200915', 'until' : '20200916', 'timeout' : 3} 
resultats = requetGet('trips', param2)
print(resultats)
    
