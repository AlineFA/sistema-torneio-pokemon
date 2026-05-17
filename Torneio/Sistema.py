from abc import ABC, abstractmethod
import random

# ==================== TIPOS ====================
class Tipo:
    """Representa o tipo de um Pokémon ou de um golpe."""

    def __init__(self, nome, efetividade):
        self.__nome = nome
        self.__efetividade = efetividade

    @property
    def nome(self):
        return self.__nome

    @property
    def efetividade(self):
        return self.__efetividade

    def multiplicador_efetividade(self, tipo_alvo):
        """Retorna o multiplicador de dano deste tipo contra o tipo alvo. 
        Se o tipo alvo não estiver definido, retorna 1 (neutro)."""

        if tipo_alvo is None:
            return 1

        nome_alvo = tipo_alvo.nome
    
        if nome_alvo in self.__efetividade:
            return self.__efetividade[nome_alvo]
    
        return 1


    def __str__(self):
        return self.__nome
    

# ==================== EFEITOS DE STATUS ====================

class EfeitoStatus(ABC):
    """Classe abstrata que serve de base para os efeitos gerados pelos status, 
    define o padrão que suas subclasses devem seguir usando o método aplicar()"""

    def __init__(self, nome):
        self.__nome = nome[:10]

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def aplicar(self, pokemon):
        pass

    def __str__(self):
        return self.nome


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


# ==================== GOLPE ====================

class Golpe():
    """Aplica um golpe a um Pokémon"""

    def __init__ (self, nome, tipo, poder, acuracia, efeito=None, chance=0):
        self.__nome = nome[:15]
        self.__tipo = tipo
        self.__poder = min(int(poder), 250)
        self.__acuracia = min(float(acuracia), 1)
        self.__efeito = efeito
        self.__chance = min(float(chance), 1)

    @property
    def nome(self):
        return self.__nome
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def poder(self):
        return self.__poder
    
    @property
    def acuracia(self):
        return self.__acuracia
    
    @property
    def efeito(self):
        return self.__efeito
    
    @property
    def chance(self):
        return self.__chance

    def calcular_dano(self, pokemon_alvo, pokemon_atacante):
        """Calcula o dano aplicado ao Pokémon através de um cálculo base e um multiplicador"""

        nivel = 50
        a = pokemon_atacante.ataque
        d = pokemon_alvo.defesa
        base = int(((2 * nivel) / 5) * self.__poder * (a / d) / 50) + 2
        modificador = random.uniform(0.85, 1) * self.__tipo.multiplicador_efetividade(pokemon_alvo.tipo)
        dano = base * modificador 
        return int(dano)

    def __str__(self):
        return f"Nome: {self.__nome} | Tipo: {self.__tipo} | Poder: {self.__poder} | Acuracia: {self.__acuracia} | Efeito: {self.__efeito} | Chance: {self.__chance}"


# ==================== POKEMON ====================
                
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

    @property
    def nome(self):
        return self.__nome

    @property    
    def tipo(self):
        return self.__tipo

    @property   
    def vida_maxima(self):
        return self.__vida_max

    @property    
    def vida_atual(self):
        return self.__vida_atual

    @property    
    def ataque(self):
        return self.__ataque 

    @property
    def defesa(self):
        return self.__defesa

    @property    
    def velocidade(self):
        return self.__velocidade

    @property    
    def golpes(self):
         return self.__golpes

    @property    
    def status(self):
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
        """Aplica todos os efeitos de status ativos no Pokémon, 
        causando dano ou outros efeitos a cada turno."""
        for efeito in self.__status:
            efeito.aplicar(self)
            
    def remover_status (self, status):
        """Remove um status, mas somente se ele estiver aplicado ao Pokémon.""" 

        if status in self.__status:
            self.__status.remove(status)
       
    def esta_desmaiado(self):
        """Retorna True se o Pokémon está sem vida e fora de combate."""

        return self.__vida_atual == 0
        
    def limpar_status(self):
        """Remove todos os efeitos de status do Pokémon."""
        self.__status.clear()

    def __str__(self):
        return f"{self.__nome} | Tipo: {self.__tipo} | Vida Máxima: {self.__vida_max} | Vida atual {self.__vida_atual}"


# ==================== ITEM ====================

class Item(ABC):
    """Classe abstrata que serve como base para os itens utilizados nas batalhas. 
    Possui os métodos pode_usar() e usar() que serão implementados pelas subclasses"""

    def __init__(self, cura_status):
        self.__cura_status = cura_status

    @property
    def cura_status(self):
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
        return pokemon.vida_atual < 0.8 * pokemon.vida_maxima
        
    def usar(self, pokemon):
        if self.pode_usar(pokemon):
            pokemon.receber_cura(20)


class SuperPocao(Item):
    """Subclasse de Item que verifica se o Pokémon pode usar 
    a super poção de cura e aplica ela adicionando 50 pontos de vida
    caso o Pokémon esteja com menos de 50% da sua vida"""

    def __init__(self):
        super().__init__(False)

    def pode_usar(self, pokemon):
        return pokemon.vida_atual < 0.5 * pokemon.vida_maxima
    
    def usar(self, pokemon):
        if self.pode_usar(pokemon):
            pokemon.receber_cura(50)


class Antidoto(Item): 
    """Subclasse de Item que permite que o Pokémon use o Antídoto
     caso esteja sob o efeito de Envenenamento"""

    def __init__(self):
        super().__init__(True)

    def pode_usar(self, pokemon):
        for efeito in pokemon.status:
            if isinstance(efeito, Envenenado):
                return True
        return False 
    
    def usar(self, pokemon):
        if self.pode_usar(pokemon):
            for efeito in pokemon.status:
                if isinstance(efeito, Envenenado):
                    pokemon.remover_status(efeito)
                    break


class Antiqueimadura(Item): 
    """Subclasse de Item que permite que o Pokémon use a 
    Anti Queimadura caso esteja sob o efeito de Queimadura"""

    def __init__(self):
        super().__init__(True)

    def pode_usar(self, pokemon):
        for efeito in pokemon.status:
            if isinstance(efeito, Queimadura):
                return True
        return False 
    
    def usar(self, pokemon):
        if self.pode_usar(pokemon):
            for efeito in pokemon.status:
                if isinstance(efeito, Queimadura):
                    pokemon.remover_status(efeito)
                    break


class CuraTotal(Item):
    """Subclasse de Item que verifica se o Pokémon está sob o
     efeito de algum status e caso sim, remove todos eles"""

    def __init__(self):
        super().__init__(True)

    def pode_usar(self, pokemon):
        return len(pokemon.status) > 0
        
    def usar(self, pokemon):
        if self.pode_usar(pokemon):
             pokemon.limpar_status() 


# ==================== ACAO ====================

class Acao(ABC):
    """Classe abstrata que representa uma ação
    realizada durante a batalha."""

    @abstractmethod
    def executar(self):
        pass


class AcaoAtq(Acao):
    """Subclasse de Acao que representa um ataque com um golpe."""

    def __init__ (self, golpe):
        self.__golpe = golpe

    @property
    def golpe(self):
        return self.__golpe

    def executar(self, pokemon):
        pass


class AcaoItem(Acao):
    """Subclasse de Acao que representa o uso de um item."""

    def __init__ (self, item):
        self.__item = item

    @property
    def item(self):
        return self.__item

    def executar(self, pokemon):
        pass


# ==================== TREINADOR ====================

class Treinador():
    """Representa um treinador no sistema, possuindo 
    até 6 Pokémons e itens para uso durante as batalhas."""

    def __init__ (self, nome, pokemons):
        self.__nome = nome[:20]
        self.__pokemons = pokemons[:6]
        self.__itens = [Pocao(), Pocao(), SuperPocao(), Antidoto(), Antiqueimadura(), CuraTotal()]

    @property
    def nome(self):
        return self.__nome

    @property      
    def pokemons(self):
        return self.__pokemons

    @property       
    def itens(self):
        return self.__itens
    
    def tem_pokemon_disponivel(self):
        """Verifica se tem pelo menos um Pokémon não desmaiado"""
        for pokemon in self.pokemons:
            if not pokemon.esta_desmaiado():
                return True
        return False
        
    def escolher_pokemon(self):
        """Escolhe aleatoriamente um Pokémon não desmaiado"""

        pokemons_acordados = []
        for pokemon in self.pokemons:
            if not pokemon.esta_desmaiado():
                pokemons_acordados.append(pokemon)

        if pokemons_acordados:
            return random.choice(pokemons_acordados)
        return None
    

    def escolher_acao(self, pokemon):
        """Escolhe aleatoriamente uma ação, com 70% de chance 
        de atacar com um golpe e 30% de usar um item, priorizando 
        itens de cura."""

        if random.random() < 0.7:
            golpe = random.choice(pokemon.golpes)
            return AcaoAtq(golpe)
        else:
            itens_cura = [item for item in self.__itens if not item.cura_status and item.pode_usar(pokemon)]
    
            if itens_cura:
                item = random.choice(itens_cura)
                return AcaoItem(item)
            else:
                itens_disponiveis = [item for item in self.__itens if item.pode_usar(pokemon)]
                if itens_disponiveis:
                    item = random.choice(itens_disponiveis)
                    return AcaoItem(item)
                else:
                    golpe = random.choice(pokemon.golpes)
                    return AcaoAtq(golpe)


# ==================== BATALHA ====================

class Batalha():
    """Representa uma batalha entre dois treinadores,
    simulando os turnos e registrando os acontecimentos."""

    def __init__(self, treinador1, treinador2):
        self.__treinador1 = treinador1
        self.__treinador2 = treinador2 
        self.__registro = []
    
    @property
    def treinador1(self):
        return self.__treinador1
    
    @property
    def treinador2(self):
        return self.__treinador2
    
    @property 
    def registro(self):
        return self.__registro
    
    def registrar(self, mensagem):
        """Adiciona uma mensagem ao registro da batalha"""

        self.__registro.append(mensagem)
    
    def simular(self):
        """Simula a batalha turno a turno entre os dois treinadores, 
        aplicando efeitos de status, executando ações e verificando 
        desmaiados até que um dos treinadores não tenha mais Pokémons 
        disponíveis."""

        self.registrar(f"Batalha: {self.__treinador1.nome} vs {self.__treinador2.nome}")
        pokemon1 = self.__treinador1.escolher_pokemon()
        pokemon2 = self.__treinador2.escolher_pokemon()
        turno = 0 # ← perguntar se pode 

        while self.__treinador1.tem_pokemon_disponivel() and self.__treinador2.tem_pokemon_disponivel():
            turno += 1 # ← adiciona contagem dos turnos 
            if turno > 200: # ← limita os turnos
                break
            if pokemon1 is None or pokemon2 is None:  
                break
            if pokemon1.velocidade > pokemon2.velocidade:
                primeiro = pokemon1
                segundo = pokemon2
            elif pokemon2.velocidade > pokemon1.velocidade:
                primeiro = pokemon2
                segundo = pokemon1
            else:
                primeiro, segundo = random.choice([(pokemon1, pokemon2), (pokemon2, pokemon1)])
            
            primeiro.aplicar_status()
            segundo.aplicar_status()

            if primeiro == pokemon1:
                treinador_primeiro = self.__treinador1
                treinador_segundo = self.__treinador2
            else:
                treinador_primeiro = self.__treinador2
                treinador_segundo = self.__treinador1

            acao1 = treinador_primeiro.escolher_acao(primeiro)
            acao2 = treinador_segundo.escolher_acao(segundo)

            if isinstance(acao1, AcaoAtq):
                if random.random() <= acao1.golpe.acuracia: 
                    dano = acao1.golpe.calcular_dano(segundo, primeiro)
                    segundo.receber_dano(dano)
                    self.registrar(f"{primeiro.nome} usou {acao1.golpe.nome} e causou {dano} de dano!")
                    if acao1.golpe.efeito is not None:
                        if random.random() <= acao1.golpe.chance:
                            segundo.adicionar_status(acao1.golpe.efeito)
                    if segundo.esta_desmaiado():
                        segundo = treinador_segundo.escolher_pokemon()
                        if segundo is None:
                            break
                        continue    
                else:
                    self.registrar(f"{primeiro.nome} errou o golpe!")
            elif isinstance(acao1, AcaoItem):
                acao1.item.usar(primeiro)
                self.registrar(f"{primeiro.nome} usou um item!")


            if isinstance(acao2, AcaoAtq):
                if random.random() <= acao2.golpe.acuracia: 
                    dano = acao2.golpe.calcular_dano(primeiro, segundo)
                    primeiro.receber_dano(dano)
                    self.registrar(f"{segundo.nome} usou {acao2.golpe.nome} e causou {dano} de dano!")
                    if acao2.golpe.efeito is not None:
                        if random.random() <= acao2.golpe.chance:
                            primeiro.adicionar_status(acao2.golpe.efeito)
                    if primeiro.esta_desmaiado():
                        primeiro = treinador_primeiro.escolher_pokemon()
                        if primeiro is None:
                            break
                        continue     
                else:
                    self.registrar(f"{segundo.nome} errou o golpe!")
            elif isinstance(acao2, AcaoItem):
                acao2.item.usar(segundo)
                self.registrar(f"{segundo.nome} usou um item!")

            if segundo.esta_desmaiado():
                self.registrar(f"{segundo.nome} desmaiou!")
                segundo = treinador_segundo.escolher_pokemon()
                if segundo is None:
                    break
            if primeiro.esta_desmaiado():
                self.registrar(f"{primeiro.nome} desmaiou!")
                primeiro = treinador_primeiro.escolher_pokemon()
                if primeiro is None:
                    break

        if self.__treinador1.tem_pokemon_disponivel():
            self.registrar(f"Vencedor: {self.__treinador1.nome}")
        else:
            self.registrar(f"Vencedor: {self.__treinador2.nome}")

    @property
    def vencedor(self):
        """Retorna o treinador vencedor da batalha,
        ou seja, o que ainda possui Pokémons disponíveis."""
        if self.__treinador1.tem_pokemon_disponivel():
            return self.__treinador1
        return self.__treinador2
    
    
# ==================== TORNEIO ====================

class Torneio:
    """Representa um torneio entre treinadores, gerenciando as
     batalhas, o histórico e determinando o vencedor final."""
    
    def __init__ (self, treinadores):
        self.__treinadores = treinadores
        self.__historico = []
        self.__vencedor = None

    @property
    def treinadores(self):
        return self.__treinadores
    
    @property
    def historico(self):
        return self.__historico
    
    @property
    def vencedor(self):
        return self.__vencedor
    
    def executar(self):
        """Executa o torneio realizando batalhas entre os treinadores, 
        eliminando os perdedores até restar apenas um vencedor."""

        while len(self.treinadores) > 1:
            treinador1 = random.choice(self.treinadores)
            treinador2 = random.choice(self.treinadores)
            while treinador1 == treinador2:
                treinador2 = random.choice(self.treinadores)
            batalha = Batalha(treinador1, treinador2)
            batalha.simular()
            vencedor = batalha.vencedor
            self.historico.append(batalha)
            if vencedor == treinador1:
                perdedor = treinador2
            else:
                perdedor = treinador1
            self.__treinadores.remove(perdedor)
        self.__vencedor = self.__treinadores [0]
        
            


    