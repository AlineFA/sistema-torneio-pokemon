import sys
import csv
from Torneio.Sistema import *
from Torneio.Erros import *

arquivo_entrada = sys.argv[1]

erros = []
log = [] 

tipos = {}
golpes = {} 
pokemons = {}
treinadores = {}
torneio_treinadores = []

with open(arquivo_entrada) as arq:

    for linha in arq:
        partes = linha.split(":",1) #separa só no primeiro : e para
        comando = partes[0].strip()

        if comando == "add_type":
            pass
        elif comando == "add_move":
            pass
        elif comando == "add_pokemon":
            pass
        elif comando == "add_trainer":
            pass
        elif comando == "add_tournament":
            pass