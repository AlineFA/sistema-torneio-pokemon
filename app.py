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
            args = partes[1].strip()
            info = args.split(",")
            nome_golpe = info[0].strip()
            tipo_golpe = info[1].strip()
            poder_golpe = info[2].strip()
            acuracia_golpe = info[3].strip()

            if len(info) > 4:
                efeito_golpe = info[4].strip()
            else:
                efeito_golpe = None
            
            if len(info) > 5:
                chance_efeito = info[5].strip()
            else:
                chance_efeito = 0

            if efeito_golpe == "Burn":
                efeito_objeto = Queimadura()
            elif efeito_golpe == "Poison":
                efeito_objeto = Envenenado()
            elif efeito_golpe is None:
                efeito_objeto = None
            else:
                erros.append(f"Golpe '{nome_golpe}': efeito '{efeito_golpe}' não implementado.")
                efeito_objeto = None

            if nome_golpe in golpes:
                erros.append(f"Golpe '{nome_golpe}' já cadastrado — ignorado.") #nao pode ter dois golpes iguais?
            else:
                if tipo_golpe not in tipos:
                    erros.append(f"Tipo '{tipo_golpe}' não existe — ignorado.")
                else:
                    try:
                        poder = int(poder_golpe)
                        if poder <= 0:
                            erros.append(f"{poder_golpe} é menor que 0 - ignorado")
                        else:
                            if poder > 250:
                                erros.append(f"{poder_golpe} é maior que o limite de 250 - valor redefinido para 250")
        
                            try:
                                acuracia = float(acuracia_golpe)
                                if acuracia > 1:
                                    erros.append(f"Golpe '{nome_golpe}': acurácia > 1 — reduzida para 1.")
                                
                                golpes[nome_golpe] = Golpe(nome_golpe, tipos[tipo_golpe], poder, acuracia, efeito_objeto, float(chance_efeito))
                            except ValueError:
                                erros.append(f"Golpe '{nome_golpe}': acurácia inválida — ignorado.")
                            
                    except ValueError:
                        erros.append(f"Golpe '{nome_golpe}': poder inválido — ignorado.")
                                    
                
        

                

        elif comando == "add_pokemon":
            pass
        elif comando == "add_trainer":
            pass
        elif comando == "add_tournament":
            pass