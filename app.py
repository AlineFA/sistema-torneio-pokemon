import sys
import csv
from Torneio.Sistema import *
from Torneio.Erros import *

"""
→ Arquivo principal do sistema.

→ Responsável por:
✔︎ ler os arquivos de entrada
✔︎ criar os objetos do sistema
✔︎ executar o torneio
✔︎ gerar os arquivos de saída
"""

arquivo_entrada = sys.argv[1]

erros = []
log = [] #tirar

tipos = {}
golpes = {} 
pokemons = {}
treinadores = {}
torneio_treinadores = []

with open(arquivo_entrada) as arq:

    for linha in arq:
        partes = linha.split(":",1)
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
                erros.append(f"Golpe '{nome_golpe}' já cadastrado — ignorado.") 
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

            args = partes[1].strip()
            info = args.split(",")
            nome_pokemon = info[0].strip()
            tipo_pokemon = info[1].strip()
            hp_pokemon = info[2].strip()
            ataque_pokemon = info[3].strip()
            defesa_pokemon = info[4].strip()
            velocidade_pokemon = info[5].strip()
            golpes_str = info[6].strip()
            golpes_str = golpes_str.strip("[]")
            lista_golpes = golpes_str.split(";")

            if nome_pokemon in pokemons:
                erros.append(f"{nome_pokemon} já exite - ignorado")
            else:
                if tipo_pokemon not in tipos:
                    erros.append(f"{tipo_pokemon} não existe - ignorado")
                else:
                    try:
                        hp = int(hp_pokemon)
                        ataque = int(ataque_pokemon)
                        defesa = int(defesa_pokemon)
                        velocidade = int(velocidade_pokemon)
                        
                        valido = True

                        if hp > 255:
                            erros.append(f"hp maior que o limite de 255 - redefinida para 255")

                        if hp <= 0:
                            erros.append("hp inválido - ignorado")
                            valido = False

                        if ataque <= 0:
                            erros.append("ataque menor ou igual a 0 - ignorado")
                            valido = False

                        if ataque > 255:
                            erros.append("ataque ultrapassou o limite de 255 - valor redefinido para 255")

                        if defesa <= 0:
                            erros.append("defesa menor ou igual a 0 - ignorada")
                            valido = False

                        if defesa > 255:
                            erros.append("defesa ultrapassou o limite de 255 - valor redefinido para 255")

                        if velocidade > 255:
                            erros.append("velocidade ultrapassou o limite de 255 - valor redefinido para 255")
                        
                        if velocidade <=0:
                            erros.append(f"velocidade menor ou igual a 0 - ignorada")
                            valido = False

                        if valido:
                            pokemons[nome_pokemon] = Pokemon(nome_pokemon, tipos[tipo_pokemon], hp, ataque, defesa, velocidade)
                            for nome_golpe in lista_golpes:
                                nome_golpe = nome_golpe.strip()
                                if nome_golpe not in golpes:
                                    erros.append(f"Golpe '{nome_golpe}' não existe - ignorado")
                                else:
                                    pokemons[nome_pokemon].adicionar_golpe(golpes[nome_golpe])

                            if not pokemons[nome_pokemon].golpes:
                                erros.append(f"Pokemon '{nome_pokemon}': nenhum golpe válido — ignorado.")
                                del pokemons[nome_pokemon]
                                                                
                    except ValueError:
                        erros.append(f"Pokemon '{nome_pokemon}': stat inválido — ignorado.")



        elif comando == "add_trainer":
            args = partes[1].strip()
            pos = args.find("[")
            nome_treinador = args[:pos].strip().strip(",")
            resto = args[pos:]
            pos2 = resto.find("[(")
            lista_pokemons = resto[:pos2].strip()
            lista_pokemons = lista_pokemons.strip("[], ")
            lista_pokemons = lista_pokemons.split(";")
            lista_itens = resto[pos2:].strip()

            if nome_treinador in treinadores:
                erros.append(f"Treinador já adicionado - ignorado")
            else:
                if len(nome_treinador) > 20:
                    erros.append(f"Nome do treinador com mais de 20 caracteres - redefinido para 20 caracteres cortando os demais")
        
                pokemons_validos =[]
                for nome_pokemon in lista_pokemons:
                    nome_pokemon = nome_pokemon.strip()
                    if nome_pokemon not in pokemons:
                        erros.append(f"Pokemon '{nome_pokemon}' não existe - ignorado")
                    else:
                        pokemons_validos.append(pokemons[nome_pokemon])
                                
                if not pokemons_validos:
                    erros.append("O treinador não possui pokémons válidos - treinador ignorado")
                else:
                    treinadores[nome_treinador] = Treinador(nome_treinador, pokemons_validos)

                    lista_itens = lista_itens.strip("[]")
                    lista_itens = lista_itens.split(";")
                    
                    itens_suportados = ["Potion", "SuperPotion", "HyperPotion", "FullRestore", "Antidote", "BurnHeal", "FullHeal", "ParalyzeHeal"]
                    
                    for item in lista_itens:
                        nome_item = item.strip().strip("()").split(":")[0].strip()
                        if nome_item not in itens_suportados:
                            erros.append(f"Item '{nome_item}' não implementado - ignorado")


        elif comando == "add_tournament":
            args = partes[1].strip()
            args = args.strip("[]")
            torneio_treinadores = [nome.strip() for nome in args.split(";")]


treinadores_validos = []
nomes_usados = []
for nome in torneio_treinadores:
    nome = nome.strip()
    if nome in nomes_usados:
        erros.append(f"Treinador '{nome}' duplicado no torneio - ignorado")
    elif nome not in treinadores:
        erros.append(f"Treinador '{nome}' não cadastrado - ignorado")
    else:
        nomes_usados.append(nome)
        treinadores_validos.append(treinadores[nome])

if len(treinadores_validos) < 2:
    erros.append("Torneio precisa de pelo menos 2 treinadores válidos!")
else:
    torneio = Torneio(treinadores_validos)
    torneio.executar()

    with open("outputs/Torneio.out", "w") as saida:
        for batalha in torneio.historico:
            for mensagem in batalha.registro:
                saida.write(mensagem + "\n")
        saida.write(f"\nVencedor do torneio: {torneio.vencedor.nome}\n")

    with open("outputs/Torneio.err", "w") as erros_saida:
        for erro in erros:
            erros_saida.write(erro + "\n")

