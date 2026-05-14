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