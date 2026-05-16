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
            args = partes[1].strip()
            info = args.split(",", 1)
            nome_tipo = info[0].strip()
            caminho_csv = info[1].strip()
            
            if nome_tipo in tipos:
                erros.append(f"Tipo '{nome_tipo}' já cadastrado — ignorado.")
            else:
                with open(caminho_csv) as arq_csv:
                    leitor = csv.DictReader(arq_csv)
                    for linha_csv in leitor:
                        if linha_csv["Attacking"] == nome_tipo:
                            efetividade = {}
                            for tipo_alvo, multiplicador in linha_csv.items():
                                if tipo_alvo != "Attacking":
                                    efetividade[tipo_alvo] = float(multiplicador)
                tipos[nome_tipo] = Tipo(nome_tipo, efetividade)

        
        elif comando == "add_move":
            pass
        elif comando == "add_pokemon":
            pass
        elif comando == "add_trainer":
            pass
        elif comando == "add_tournament":
            pass