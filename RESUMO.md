# Reflexão sobre o desenvolvimento do projeto

O projeto aprofundou bastante minhas habilidades de orientação a objetos em Python, já que, para resolver os vários desafios que foram surgindo, foi necessário pesquisar bastante e "quebrar" a cabeça. Além disso, precisei recorrer à ajuda de pessoas com conhecimento em programação, principalmente quando fiz as primeiras execuções, que não funcionaram, pois o `app.py` não estava totalmente correto.

## Leitura e manipulação dos arquivos

Uma das dificuldades dentro do `app.py`, foi em relação à leitura e manipulação dos arquivos de entrada, especialmente na leitura dos treinadores, pois o formato das linhas possuía vírgulas dentro das listas de pokémons e itens, o que dificultava a separação correta dos dados.

Para resolver isso, utilizei o método `find()` para localizar os colchetes e separar corretamente essas informações antes de realizar o `split`.

## Tratamento de casos sem Pokémon disponível

Nas execuções seguintes, após corrigir a leitura, encontrei um problema relacionado ao encerramento das batalhas. Em alguns casos, quando um pokémon desmaiava e o treinador não possuía mais pokémons disponíveis, o método responsável por selecionar o próximo retornava `None`, porém o programa continuava tentando utilizar esse valor como se fosse um pokémon válido.

Para resolver isso, adicionei verificações para interromper corretamente a execução nesses casos, evitando que o sistema continuasse operando com valores inválidos.

## Otimização das batalhas e correção do fluxo da simulação

Outro desafio foi na velocidade de execução dos arquivos. Mesmo após corrigir os primeiros problemas, a partir do `Torneio2.txt` a execução ficou lenta.

Como tentativa inicial para acelerar os testes, limitei os turnos das batalhas. Apesar disso, os arquivos de output continuaram grandes.

Ao questionar o professor, recebi a orientação de que a saída estava muito maior que o esperado (mesmo com limite de turnos), e que, a princípio, limitar turnos não era a solução esperada.

Após analisar melhor o código, identifiquei que o problema estava na função `simular()` da classe `Batalha`. Quando um pokémon desmaiava durante o ataque do segundo pokémon, o código não reiniciava o turno corretamente, fazendo com que o pokémon desmaiado continuasse participando da batalha. 

Após fazer a correção, os outputs do `Torneio5.txt` passaram de uma média de mais de 5000 linhas para menos de 1000, sem necessidade de limitar o número de turnos.

## Reflexão final

Ao analisar o projeto, percebo evolução tanto no código quanto no raciocínio.

Por vezes, parecia que o que eu estava implementando não fazia muito sentido, mas à medida que as etapas foram se conectando, fui compreendendo como tudo se relaciona e como cada decisão tomada impacta diretamente o funcionamento do sistema.
