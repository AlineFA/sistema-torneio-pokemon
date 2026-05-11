from abc import ABC, abstractmethod
import random

class Tipo:
    """Representa o tipo de um Pokémon ou de um golpe."""

    def __init__(self, nome, efetividade):
        self.__nome = nome
        self.__efetividade = efetividade

    def get_nome(self):
        return self.__nome

    def get_efetividade(self):
        return self.__efetividade

    def multiplicador_efetividade(self, tipo_alvo):
        """Retorna o multiplicador de dano deste tipo contra o tipo alvo. 
        Se o tipo alvo não estiver definido, retorna 1 (neutro)."""

        if tipo_alvo is None:
            return 1

        nome_alvo = tipo_alvo.get_nome()
    
        if nome_alvo in self.__efetividade:
            return self.__efetividade[nome_alvo]
    
        return 1


    def __str__(self):
        return self.__nome
    

class EfeitoStatus(ABC):
    """Classe abstrata que serve de base para os efeitos gerados pelos status, 
    define o padrão que suas subclasses devem seguir usando o método aplicar()"""

    def __init__(self, nome):
        self.__nome = nome[:10]

    def get_nome(self):
        return self.__nome

    @abstractmethod
    def aplicar(self, pokemon):
        pass

    def __str__(self):
        return self.get_nome()


class Queimadura(EfeitoStatus):
    """Subclasse de EfeitoStatus que aplica 3 pontos de dano por turno ao Pokémon afetado"""
    
    def __init__(self):
        super().__init__("Queimadura")

    def aplicar(self, pokemon):
        pokemon.receber_dano(3)


class Envenenado(EfeitoStatus):
    """Subclasse de EfeitoStatus que aplica 5 pontos de dano por turno ao Pokémon afetado"""

    def __init__(self):
        super().__init__("Envenenado")

    def aplicar(self, pokemon):
        pokemon.receber_dano(5)


class Golpe():
    """Aplica um golpe a um Pokémon"""

    def __init__ (self, nome, tipo, poder, acuracia, efeito=None, chance=0):
        self.__nome = nome[:15]
        self.__tipo = tipo
        self.__poder = min(int(poder), 250)
        self.__acuracia = min(float(acuracia), 1)
        self.__efeito = efeito
        self.__chance = min(float(chance), 1)

    def get_nome(self):
        return self.__nome
    
    def get_tipo(self):
        return self.__tipo
    
    def get_poder(self):
        return self.__poder
    
    def get_acuracia(self):
        return self.__acuracia
    
    def get_efeito(self):
        return self.__efeito
    
    def get_chance(self):
        return self.__chance

    def calcular_dano(self, pokemon_alvo, pokemon_atacante):
        """Calcula o dano aplicado ao Pokémon através de um cálculo base e um multiplicador"""

        nivel = 50
        a = pokemon_atacante.get_ataque()
        d = pokemon_alvo.get_defesa()
        base = int(((2 * nivel) / 5) * self.__poder * (a / d) / 50) + 2
        modificador = random.uniform(0.85, 1) * self.__tipo.multiplicador_efetividade(pokemon_alvo.get_tipo())
        dano = base * modificador 
        return int(dano)

    def __str__(self):
        return f"Nome: {self.__nome} | Tipo: {self.__tipo} | Poder: {self.__poder} | Acuracia: {self.__acuracia} | Efeito: {self.__efeito} | Chance: {self.__chance}"


class Item(ABC):
    """Classe abstrata que serve como base para os itens utilizados nas batalhas. 
    Possui os métodos pode_usar() e usar() que serão implementados pelas subclasses"""

    def __init__(self, cura_status):
        self.__cura_status = cura_status

    def get_cura_status(self):
        return self.__cura_status

    @abstractmethod
    def pode_usar(self, pokemon):
        pass

    @abstractmethod
    def usar(self, pokemon):
        pass


class Pocao(Item):
    """Subclasse de Item que verifica se o Pokémon pode usar 
    a poção de cura e aplica ela adicionando 20 pontos de vida
    caso o Pokémon esteja com menos de 80% da sua vida"""

    def __init__(self):
        super().__init__(False)

    def pode_usar(self, pokemon):
        return pokemon.get_vida_atual() < 0.8 * pokemon.get_vida_maxima()
        
    def usar(self,pokemon):
        if self.pode_usar(pokemon):
            pokemon.receber_cura(20)


class Pokemon:
    """Representa um Pokémon no sistema."""

    def __init__(self, nome, tipo, hp, ataque, defesa, velocidade):
        nivel = 50

        self.__nome = nome[:15]
        self.__tipo = tipo

        vida_calculada = int(((2 * hp) * nivel) / 100) + nivel + 10
        self.__vida_max = min(vida_calculada, 255)
        self.__vida_atual = self.__vida_max

        self.__ataque = min(int(((2 * ataque) * nivel) / 100) + 5, 255)
        self.__defesa = min(int(((2 * defesa) * nivel) / 100) + 5, 255)
        self.__velocidade = min(int(((2 * velocidade) * nivel) / 100) + 5, 255)

        self.__golpes = []
        self.__status = []

    def get_nome(self):
        return self.__nome
        
    def get_tipo(self):
        return self.__tipo
        
    def get_vida_maxima(self):
        return self.__vida_max
        
    def get_vida_atual(self):
        return self.__vida_atual
        
    def get_ataque(self):
        return self.__ataque 

    def get_defesa(self):
        return self.__defesa
        
    def get_velocidade(self):
        return self.__velocidade
        
    def get_golpes(self):
         return self.__golpes
        
    def get_status(self):
        return self.__status
        
    def receber_dano(self, dano):
        """Reduz a vida atual pelo dano recebido. A vida nunca fica abaixo de zero."""

        self.__vida_atual -= dano
        if self.__vida_atual < 0:
            self.__vida_atual = 0

    def receber_cura(self, cura):
        """Adiciona na vida atual a cura recebida. A vida nunca fica acima do máximo."""

        self.__vida_atual += cura
        if self.__vida_atual > self.__vida_max:
            self.__vida_atual = self.__vida_max

    def adicionar_golpe(self, golpe):
        """Adiciona um golpe. A quantidade de golpes nunca é maior que 4."""

        if len(self.__golpes) < 4:
            self.__golpes.append(golpe)
         
    def adicionar_status (self, status):
        """Adiciona um status, mas somente se o Pokémon não estiver com o mesmo.""" 

        if status not in self.__status:
            self.__status.append(status)

    def aplicar_status(self):
        for efeito in self.__status:
            efeito.aplicar(self)
            
    def remover_status (self, status):
        """Remove um status, mas somente se ele estiver aplicado ao Pokémon.""" 

        if status in self.__status:
            self.__status.remove(status)
       
    def esta_desmaiado(self):
        """Retorna True se o Pokémon está sem vida e fora de combate."""

        return self.__vida_atual == 0
        
    def __str__(self):
        return f"{self.__nome} | Tipo: {self.__tipo} | Vida Máxima: {self.__vida_max} | Vida atual {self.__vida_atual}"
