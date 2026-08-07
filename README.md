# AlineAcevedo

# Sistema de Torneio Pokémon

> Projeto desenvolvido para a disciplina de Programação Orientada a Dados (POD) na PUCRS.

Sistema desenvolvido em Python para simular batalhas e torneios Pokémon a partir de arquivos de entrada. O sistema realiza leitura dos dados, executa as batalhas e gera arquivos de saída contendo o histórico e resultado do torneio e possíveis erros que ocorreram.

## Como usar

No terminal, execute: 

```bash
python app.py inputs/NomeDoArquivo.txt
```

## Estrutura do projeto

- `Torneio/Sistema.py` — classes do sistema (Tipo, Golpe, Pokemon, Treinador, Batalha, Torneio)
- `Torneio/Erros.py` — classes de erro
- `app.py` — aplicação principal
- `inputs/` — arquivos de entrada (.txt e typeChart.csv)
- `outputs/` — arquivos de saída gerados

## Formato do arquivo de entrada

O arquivo de entrada deve seguir o formato:
- `add_type` — adiciona um tipo
- `add_move` — adiciona um golpe
- `add_pokemon` — adiciona um Pokémon
- `add_trainer` — adiciona um treinador
- `add_tournament` — define o torneio
- `run_tournament()` — executa o torneio

## Arquivos de saída

- `Torneio.out` — log completo das batalhas e vencedor
- `Torneio.err` — erros encontrados durante a execução
