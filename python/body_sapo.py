import shutil
import csv
from bs4 import BeautifulSoup
import re
import sqlite3
import json
import os
from geopy.geocoders import Nominatim

print("#3 python")

divisoes = {
    'Alpendre: ',
    'Casa de Banho Partilhada: ',
    'Casa(s) de Banho: ',
    'Copa(s): ',
    'Cozinha(s): ',
    'Escritório(s): ',
    'Hall de Quartos: ',
    'Lavabo',
    'Marquise: ',
    'Open Space: ',
    'Quarto de hóspedes: ',
    'Sala(s) de Jantar: ',
    'Suite(s): ',
    'Total quarto(s): ',
    'Varandas: ',
    'Casa de banho de serviço: ',
    'Casa de Banho Privativa: ',
    'Closet: ',
    'Corredor: ',
    'Despensa(s): ',
    'Hall de Entrada: ',
    'Kitchenet: ',
    'Lavandaria: ',
    'Número de pisos: ',
    'Outra(s) Sala(s): ',
    'Sala(s): ',
    'Sotão: ',
    'Telhado Verde: ',
    'Total quarto(s) interiores: '
}

arrumos = {
    'Acesso Mobilidade Reduzida',
    'Arrecadação',
    'Elevador',
    'Garagem',
    'Estacionamento',
    'Jardim',
    'Lareira',
    'Recuperador de calor',
    'Vidros Duplos',
    'Varanda',
    'Terraço',
    'Suite',
    'Segurança',
    'Piscina',
    'Painéis Solares',
    'Mobília',
    'Logradouro'
}


# Create a new database
conn = sqlite3.connect('db_new.sqlite3')

# Create a table
conn.execute('''CREATE TABLE IF NOT EXISTS houses
             (Id INTEGER PRIMARY KEY,Url TEXT,Id_Link TEXT,Type TEXT,Referencia TEXT,Situacao TEXT,Condicao TEXT,Title TEXT,Price INTEGER,Certificacao_Energética TEXT,Localizacao TEXT,Latitude TEXT,Longitude TEXT,Area_Util TEXT,Area_Bruta TEXT,Price_Per_Area REAL,Ano_de_Construcao INTEGER,Data_Publicacao TEXT,Alpendre INTEGER,Casa_de_Banho_Partilhada INTEGER,Casas_de_Banho INTEGER,Copas INTEGER,Cozinhas INTEGER,Escritórios INTEGER,Hall_de_Quartos INTEGER,Lavabo INTEGER,Marquise INTEGER,Open_Space INTEGER,Quarto_de_hóspedes INTEGER,Salas_de_Jantar INTEGER,Suites INTEGER,Total_quartos INTEGER,Varandas INTEGER,Casa_de_banho_de_serviço INTEGER,Casa_de_Banho_Privativa INTEGER,Closet INTEGER,Corredor INTEGER,Despendas INTEGER,Hall_de_Entrada INTEGER,Kitchenet INTEGER,Lavandaria INTEGER,Número_de_pisos INTEGER,Outras_Salas INTEGER,Salas INTEGER,Sotão INTEGER,Telhado_Verde INTEGER,Total_quartos_interiores INTEGER,Acesso_Mobilidade_Reduzida TEXT,Arrecadação TEXT,Elevador TEXT,Garagem TEXT,Estacionamento TEXT,Jardim TEXT,Lareira TEXT,Recuperador_de_calor TEXT,Vidros_Duplos TEXT,Varanda TEXT,Terraço TEXT,Suite TEXT,Segurança TEXT,Piscina TEXT,Painéis_Solares TEXT,Mobília TEXT,Logradouro TEXT)''')


directory = 'html_sapo'
txt_files = [f for f in os.listdir(directory) if f.endswith('.html')]
first_time = True

id_houses = 1;

for filename in txt_files:
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        # Do something with the file
        contents = file.read()
        soup = BeautifulSoup(contents, 'html.parser')

        state = ""
        estate_id = ""
        area_util = ""
        area_bruta = ""
        year = ""

        distrito = ""
        concelho = ""
        freguesia = ""
        zona = ""
        latitude = ""
        longitude= ""


        substrings = []
        words = filename.split('-')

        for word in words:
            substrings.append(word)

        # Find the status of the apartment
        status = substrings[0]

        # Find the id to the apartment
        estate_id_link = ""
        length = len(substrings)
        for i in range(length-5, length, 1):
            estate_id_link += (substrings[i]) + "-"

        end_index = estate_id_link.find('.html')
        estate_id_link = estate_id_link[:end_index]

        # Find the title of the apartment
        title = soup.find('h1').text.strip()
        # Find the price of the apartment
        price = soup.find("span", class_="detail-title-price-value").text
        # Find the description of the apartment
        if (soup.find("div", class_="detail-description-text")):
            description = soup.find(
                "div", class_="detail-description-text").text
        # Find the location of the apartment
        location = soup.find("div", class_="detail-title-location").text

        # Find the data of the apartment
        data = soup.find_all("div", class_="detail-main-features-item")

        for apartment in data:
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Estado"):
                state = apartment.find(
                    "div", class_="detail-main-features-item-value").text
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Ano de construção"):
                year = apartment.find(
                    "div", class_="detail-main-features-item-value").text
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Referência"):
                estate_id = apartment.find(
                    "div", class_="detail-main-features-item-value").text
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Área útil"):
                area_util = apartment.find(
                    "div", class_="detail-main-features-item-value").text
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Área bruta"):
                area_bruta = apartment.find(
                    "div", class_="detail-main-features-item-value").text
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Certificação Energética"):
                certi_ener_str = ""
                certi_ener = apartment.find(
                    "div", class_="detail-main-features-item-value").text
                certi_ener = certi_ener.split()
                certi_ener_str = certi_ener_str.join(certi_ener)
                if (certi_ener_str == "Avaliaçãoemcurso"):
                    certi_ener_str = "Avaliação em curso"
            if (apartment.find("div", class_="detail-main-features-item-title").text == "Publicado em"):
                publicacao = apartment.find(
                    "div", class_="detail-main-features-item-value").text

        # Find number divions around the house

        data = soup.find_all("div", class_='detail-features-item')

        division_counts = {d: 0 for d in divisoes}

        for apartment in data:
            for d in divisoes:
                if (d in apartment):
                    if(apartment.text.find('<strong>')):
                        apartment_1 = apartment.text.split('<strong>')[0]
                    else:
                        apartment_1 = data.div.text
                    if (re.search('\d', apartment_1)):
                        num_div_apart = apartment_1.split(':')[1].strip()
                        text = apartment_1.split(':')[0] + ': '
                        if text in division_counts:
                            division_counts[text] = int(num_div_apart)
                        else:
                            division_counts[text] = 0
                    elif ("Não" in apartment_1):
                        text = apartment_1.split(':')[0] + ': '
                        if text in division_counts:
                            division_counts[text] = 0
                    else:
                        if apartment_1 in division_counts:
                            division_counts[apartment_1] = 1
                else:
                    text = d
                    if text not in division_counts:
                        division_counts[text] = 0

        arrumos_counts = {d: 0 for d in arrumos}
        
        for apartment in data:
            for a in arrumos:
                if (a in apartment):
                    if a in arrumos_counts:
                        arrumos_counts[a] = True
                else:
                    if a not in arrumos_counts:
                        arrumos_counts[a] = False

        modified_string = filename.replace('.html.html', '.html')

        # Add the prefix to create the final URL
        final_url = 'https://casa.sapo.pt/' + modified_string

        script = soup.find('script', type='application/ld+json').text
        script_json = json.loads(script)
        category = script_json['category']
        category=category.lower()


        if location is not None:
            # Create a geolocator object using Nominatim
            geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
            location_2 = geolocator.geocode(location)

            if location_2 is not None:
                latitude = location_2.latitude
                longitude = location_2.longitude
            else:
                latitude = None
                longitude = None 

        if price and (area_bruta or area_util):
            if " / " in price:
                price = price.split(" / ")[0]
                if not price:
                    price = 0
            price = str(price).replace("€", "").replace(".", "").replace("\xa0", "") # Remove euro symbol and decimal point
            if area_bruta:
                area_bruta = area_bruta.replace("m²", "").replace(",", ".").replace("\xa0", "")
                area_bruta = float(area_bruta)
                price_per_area = float(price) / area_bruta # Convert price to int and divide by area  
            elif area_util:
                area_util = area_util.replace("m²", "").replace(",", ".").replace("\xa0", "")
                area_util = float(area_util)
                price_per_area = float(price) / area_util # Convert price to int and divide by area
            else:
                price_per_area = None
        else:
            price_per_area = None

        if area_bruta and area_util:
            area_util = area_util.replace("m²", "").replace(",", ".").replace("\xa0", "")

        if price_per_area is not None:
            price_per_area = round(price_per_area, 2) # Round to 2 decimal places



       # Write a row to the database
        data_row = [id_houses, final_url, estate_id_link, category, estate_id, status, state, title, price, certi_ener_str, location, latitude, longitude, area_util, area_bruta, price_per_area, year, publicacao]
        for key, value in division_counts.items():
            data_row.append(value)
        for key, value in arrumos_counts.items():
            data_row.append(value)
    
    conn.execute('INSERT INTO houses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,? ,? ,? ,? ,?)', data_row)
    # Commit changes to database and close connection
    id_houses+=1

conn.commit()
conn.close()
shutil.rmtree(directory)
print("DONE")
