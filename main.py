from bs4 import BeautifulSoup
import requests
import os
import unicodedata
import sys

args = sys.argv[1:]

gens = 8 # gens to search upto
# paths with files to rename
file_paths=["/home/bc7/projects/gen-v-style-sprites/gen-vi/normal/back","/home/bc7/projects/gen-v-style-sprites/gen-vi/normal/front","/home/bc7/projects/gen-v-style-sprites/gen-vi/normal/back/female","/home/bc7/projects/gen-v-style-sprites/gen-vi/normal/front/female"]

def normalize_string(inp_str):
    """ Normalise (normalize) unicode data in Python to remove umlauts, accents etc. """
    normal = unicodedata.normalize('NFKD', inp_str).encode('ASCII', 'ignore')
    return normal.decode()

# get data from bulbapedia
url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
r = requests.get(url)
if r.status_code != 200:
    print(f"Error {r.status_code}")
    exit
s = BeautifulSoup(r.content, 'html.parser')

# convert data to readable form
POKEMONS = []
for gen in range(1, gens+1):
    poke_table = s.find_all("table")[gen]
    for mon in poke_table.find_all("tr")[1:]:
        data = mon.find_all("td")
        number = data[1].text.strip()[1:]
        name = data[2].text.strip()
        POKEMONS.append((number, name))

if "r" in args:
    for file_path in file_paths:
        files = os.listdir(file_path)
        for file in files:
            filename, ext = os.path.splitext(file)
            for pokemon in POKEMONS:
                if pokemon[0] == filename.lower():
                    new_filename = f"{normalize_string(pokemon[1])}{ext}"
                    if os.path.isfile(os.path.join(file_path, new_filename)):
                        print(f"{pokemon} already exists")
                        break
                    os.rename(os.path.join(file_path, file), os.path.join(file_path,
                        new_filename))
                    break
else:
    for file_path in file_paths:
        files = os.listdir(file_path)
        for file in files:
            filename, ext = os.path.splitext(file)
            for pokemon in POKEMONS:
                if normalize_string(pokemon[1].lower()) in file.lower():
                    new_filename = f"{pokemon[0]}{ext}"
                    if os.path.isfile(os.path.join(file_path, new_filename)):
                        print(f"{pokemon} already exists")
                        break
                    os.rename(os.path.join(file_path, file), os.path.join(file_path,
                        new_filename))
                    break

