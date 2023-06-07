import sqlite3
import os
import json

print ("#5 python")

def calculate_value(value_place, total_values, results):
    if value_place['typelayer'] == "distrito":
        layer_totals = total_values['distritos']
    elif value_place['typelayer'] == "concelho":
        layer_totals = total_values['concelhos']
    elif value_place['typelayer'] == "freguesia":
        layer_totals = total_values['freguesias']

        

    result = {
              'typefeature': value_place['typefeature'] if value_place['typefeature'] else None,
              'typeLayer': value_place['typelayer'] if value_place['typelayer'] else None,
              'averagePrice_a': float(value_place['averagePrice_a']) if value_place['averagePrice_a'] else None,
              'averagePrice_c': float(value_place['averagePrice_c']) if value_place['averagePrice_c'] else None,
              'sum_area_a': float(value_place[f"sum_area_a"]) if value_place[f"sum_area_a"] else None,
              'sum_area_c': float(value_place[f"sum_area_c"]) if value_place[f"sum_area_c"] else None
            }


    if value_place['averagePrice_a'] is not None and value_place['sum_area_a'] is not None:
        average_price_per_area_a_l = float(value_place['averagePrice_a']) / float(value_place['sum_area_a'])
    else:
        average_price_per_area_a_l = 0.0
    if layer_totals['total_averagePrice_a'] is not None and layer_totals['total_sum_area_a'] is not None and layer_totals['total'] != 0:
        average_price_per_area_a_p = (float(layer_totals['total_averagePrice_a']) / float(layer_totals['total'])) / (float(layer_totals['total_sum_area_a']) / float(layer_totals['total']))
    else:
        average_price_per_area_a_p = 0.0
    
    if value_place['averagePrice_c'] is not None and value_place['sum_area_c'] is not None and value_place['sum_area_c'] != 0:
        average_price_per_area_c_l = float(value_place['averagePrice_c']) / float(value_place['sum_area_c'])
    else:
        average_price_per_area_c_l = 0.0
    
    if layer_totals['total_averagePrice_c'] is not None and layer_totals['total_sum_area_c'] is not None and layer_totals['total'] != 0:
        average_price_per_area_c_p = (float(layer_totals['total_averagePrice_c']) / float(layer_totals['total'])) / (float(layer_totals['total_sum_area_c']) / float(layer_totals['total']))
    else:   
        average_price_per_area_c_p = 0.0


    

    if average_price_per_area_c_l != 0 and average_price_per_area_c_p != 0 and average_price_per_area_a_l != 0 and average_price_per_area_a_p != 0:
        result['results_valuesRB2'] = ((((average_price_per_area_a_l/average_price_per_area_c_l)/(average_price_per_area_a_p/average_price_per_area_c_p))).real)
    else:
        result['results_valuesRB2'] = 0

    if average_price_per_area_c_p != 0:
        result['results_valuesB2'] = ((average_price_per_area_c_l/average_price_per_area_c_p).real)
    else:
        result['results_valuesB2'] = 0

    if average_price_per_area_a_p != 0:
        result['results_valuesR2'] = ((average_price_per_area_a_l/average_price_per_area_a_p).real)
    else:
        result['results_valuesR2'] = 0

    
    results.append(result)


def compare_geojson_values(typefeature, typelayer, results, total_values, values_places):
    if typelayer == "distrito":
        layer_totals = total_values['distritos']
    elif typelayer == "concelho":
        layer_totals = total_values['concelhos']
    elif typelayer == "freguesia":
        layer_totals = total_values['freguesias']
    
    # Keep track of the processed typefeatures for this typelayer
    processed_typefeatures = set()
    
    for result in results:
        if result[typelayer] and result[typelayer].replace('Ilha de ','').replace('Ilha do ','').replace('Ilha da ','').replace('Distrito de ','').replace('Distrito do ','').replace('Distrito da ','').replace(' ','').upper() == typefeature.replace(' ','').upper():
            
            # Check if this typefeature has already been processed for this typelayer
            if result[typelayer] in processed_typefeatures:
                continue
                
            if result[f"houses_in_group_{typelayer}_comprar"] is not None:
                layer_totals['total_averagePrice_c'] += float(result[f"houses_in_group_{typelayer}_comprar"])
            if result[f"houses_in_group_{typelayer}_alugar"] is not None:
                layer_totals['total_averagePrice_a'] += float(result[f"houses_in_group_{typelayer}_alugar"])
            if result[f"sum_area_{typelayer}_a"] is not None:
                layer_totals['total_sum_area_a'] += float(result[f"sum_area_{typelayer}_a"])
            if result[f"sum_area_{typelayer}_c"] is not None:
                layer_totals['total_sum_area_c'] += float(result[f"sum_area_{typelayer}_c"])
            layer_totals['total'] += 1
            
           

            value_place = {
              'typefeature': typefeature if typefeature else None,
              'typelayer': typelayer if typelayer else None,
              'averagePrice_a': float(result[f"houses_in_group_{typelayer}_alugar"]) if result[f"houses_in_group_{typelayer}_alugar"] else None,
              'averagePrice_c': float(result[f"houses_in_group_{typelayer}_comprar"]) if result[f"houses_in_group_{typelayer}_comprar"] else None,
              'sum_area_a': float(result[f"sum_area_{typelayer}_a"]) if result[f"sum_area_{typelayer}_a"] else None,
              'sum_area_c': float(result[f"sum_area_{typelayer}_c"]) if result[f"sum_area_{typelayer}_c"] else None
            }

            # Check if the typefeature has already been added
            existing_value_places = [vp for vp in values_places if vp['typefeature'] == typefeature and vp['typelayer'] == typelayer]
            if not existing_value_places:
                # If the feature doesn't exist yet, add it to the list
                values_places.append(value_place)
            else:
                existing_value_place = existing_value_places[0]
                # Compare the values and update if necessary
                if existing_value_place['averagePrice_a'] is None or (value_place['averagePrice_a'] is not None and value_place['averagePrice_a'] > existing_value_place['averagePrice_a']):
                    existing_value_place['averagePrice_a'] = value_place['averagePrice_a']
                if existing_value_place['averagePrice_c'] is None or (value_place['averagePrice_c'] is not None and value_place['averagePrice_c'] > existing_value_place['averagePrice_c']):
                    existing_value_place['averagePrice_c'] = value_place['averagePrice_c']
                if existing_value_place['sum_area_a'] is None or (value_place['sum_area_a'] is not None and value_place['sum_area_a'] > existing_value_place['sum_area_a']):
                    existing_value_place['sum_area_a'] = value_place['sum_area_a']
                if existing_value_place['sum_area_c'] is None or (value_place['sum_area_c'] is not None and value_place['sum_area_c'] > existing_value_place['sum_area_c']):
                    existing_value_place['sum_area_c'] = value_place['sum_area_c']



def read_geojson(filename):
    with open(filename, encoding='utf-8') as f:
        geojson_str = f.read()
    return json.loads(geojson_str)

def get_geojson_features(geojson_obj):
    return geojson_obj['features']

def get_average_price_area(db, situacao, location, identity):

    if location:
        location=location.replace('\'', '\'\'')
    query = f"SELECT AVG({identity}) FROM houses WHERE situacao = '{situacao}' AND Localizacao LIKE '%{location}%'"
    
    result = db.execute(query).fetchone()
    if result:
        get_average_price_area = result[0]
    else:
        get_average_price_area = None
    
    return get_average_price_area


def get_average_price_area_or_bruta(db, situacao, location):
    area_util_result = get_average_price_area(db, situacao, location, identity='Area_Util')
    return area_util_result if area_util_result is not None else get_average_price_area(db, situacao, location, identity='Area_Bruta')


# Connect to the second database
db2 = sqlite3.connect('db/db.sqlite3') 


# Retrieve the new values from the first database
new_houses = db2.execute('SELECT * FROM houses').fetchall()

# Define an empty dictionary to store the results
results = []

# Define a set to keep track of processed locations
processed_locations = set()

# Iterate over the new houses and process each one
for house in new_houses:
    # Access the values of each column using indexing
    localization = house[10]

        # Check if the location has already been processed
    if localization in processed_locations:
        continue  # Skip this location

    parts = localization.split(',')
    reversed_parts = list(reversed(parts))  # Reverse the order of the list and create a new list
    distrito = reversed_parts[0]
    concelho = reversed_parts[1]
    freguesia = reversed_parts[2] if len(reversed_parts) >= 3 else None

    houses_in_group_distrito_alugar = get_average_price_area(db2, 'alugar', distrito, 'Price')
    houses_in_group_concelho_alugar = get_average_price_area(db2, 'alugar', concelho, 'Price')
    houses_in_group_freguesia_alugar = get_average_price_area(db2, 'alugar', freguesia, 'Price') if freguesia else None

    houses_in_group_distrito_comprar = get_average_price_area(db2, 'comprar', distrito, 'Price')
    houses_in_group_concelho_comprar = get_average_price_area(db2, 'comprar', concelho, 'Price')
    houses_in_group_freguesia_comprar = get_average_price_area(db2, 'comprar', freguesia, 'Price') if freguesia else None

    # Calculate sum of Area_Util for each location
    sum_area_distrito_a = get_average_price_area_or_bruta(db2, 'alugar', distrito)
    sum_area_concelho_a = get_average_price_area_or_bruta(db2, 'alugar', concelho)
    sum_area_freguesia_a = get_average_price_area_or_bruta(db2, 'alugar', freguesia) if freguesia else None

    sum_area_distrito_c = get_average_price_area_or_bruta(db2, 'comprar', distrito)
    sum_area_concelho_c = get_average_price_area_or_bruta(db2, 'comprar', concelho)
    sum_area_freguesia_c = get_average_price_area_or_bruta(db2, 'comprar', freguesia) if freguesia else None

    # Store the results in the dictionary
    result = {
        'distrito': distrito,
        'concelho': concelho,
        'freguesia': freguesia,
        'houses_in_group_distrito_alugar': round(float(houses_in_group_distrito_alugar), 2) if houses_in_group_distrito_alugar else None,
        'houses_in_group_concelho_alugar': round(float(houses_in_group_concelho_alugar), 2) if houses_in_group_concelho_alugar else None,
        'houses_in_group_freguesia_alugar': round(float(houses_in_group_freguesia_alugar), 2) if houses_in_group_freguesia_alugar else None,
        'houses_in_group_distrito_comprar': round(float(houses_in_group_distrito_comprar), 2) if houses_in_group_distrito_comprar else None,
        'houses_in_group_concelho_comprar': round(float(houses_in_group_concelho_comprar), 2) if houses_in_group_concelho_comprar else None,
        'houses_in_group_freguesia_comprar': round(float(houses_in_group_freguesia_comprar), 2) if houses_in_group_freguesia_comprar else None,
        'sum_area_distrito_a': sum_area_distrito_a,
        'sum_area_concelho_a':  sum_area_concelho_a,
        'sum_area_freguesia_a':  sum_area_freguesia_a,
        'sum_area_distrito_c': sum_area_distrito_c,
        'sum_area_concelho_c':  sum_area_concelho_c,
        'sum_area_freguesia_c':  sum_area_freguesia_c
    }

    # Append the result to the list of results
    results.append(result)

        
    # Add the location to the set of processed locations
    processed_locations.add(localization)


db2.close()


# Parse the GeoJSON string into a Python object
geojson_obj_distrito = read_geojson('public/geojson/ContinenteDistritos.geojson')
geojson_obj_concelho = read_geojson('public/geojson/ContinenteConcelhos.geojson')
geojson_obj_freguesia = read_geojson('public/geojson/ContinenteFreguesias.geojson')

# Access the features of the GeoJSON
features_distrito = get_geojson_features(geojson_obj_distrito)
features_concelho = get_geojson_features(geojson_obj_concelho)
features_freguesia = get_geojson_features(geojson_obj_freguesia)

features_list = [    {'features': features_distrito, 'property': 'NAME_1', 'layer': 'distrito'},    {'features': features_concelho, 'property': 'NAME_2', 'layer': 'concelho'},    {'features': features_freguesia, 'property': 'NAME_3', 'layer': 'freguesia'}]

total_values = {
    'distritos': {'typelayer': 'distrito', 'total_averagePrice_c': 0, 'total_averagePrice_a': 0, 'total_sum_area_a': 0, 'total_sum_area_c': 0, 'total': 0},
    'concelhos': {'typelayer': 'concelho', 'total_averagePrice_c': 0, 'total_averagePrice_a': 0, 'total_sum_area_a': 0, 'total_sum_area_c': 0, 'total': 0},
    'freguesias': {'typelayer': 'freguesia', 'total_averagePrice_c': 0, 'total_averagePrice_a': 0, 'total_sum_area_a': 0, 'total_sum_area_c': 0, 'total': 0}
}

values_places = []

for features_dict in features_list:
    for feature in features_dict['features']:
        typefeature = feature['properties'][features_dict['property']]
        typelayer = features_dict['layer']
        compare_geojson_values(typefeature, typelayer, results, total_values, values_places)


results = []
for value_place in values_places:
  result = calculate_value(value_place, total_values, results)

b2r2_values = [result['results_valuesRB2'] for result in results]
average_B2R2 = sum(b2r2_values) / len(b2r2_values) if b2r2_values else 0

b2_values = [result['results_valuesB2'] for result in results]
average_B2 = sum(b2_values) / len(b2_values) if b2_values else 0

r2_values = [result['results_valuesR2'] for result in results]
average_R2 = sum(r2_values) / len(r2_values) if r2_values else 0

# Apply scaling based on the averages
b2r2_scaling = 10 if average_B2R2 < 0.1 else (0.1 if average_B2R2 > 2 else 1)
b2_scaling = 10 if average_B2 < 0.1 else (0.1 if average_B2 > 2 else 1)
r2_scaling = 10 if average_R2 < 0.1 else (0.1 if average_R2 > 2 else 1)

for result in results:
    result['results_valuesRB2'] *= b2r2_scaling
    result['results_valuesB2'] *= b2_scaling
    result['results_valuesR2'] *= r2_scaling




# Open the file in write mode with UTF-8 encoding
with open('values_places.json', 'w', encoding='utf-8') as f:
    # Dump the data into the JSON file
    json.dump(results, f, ensure_ascii=False)

print ('DONE')
