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
        """
        Retorna o multiplicador de dano deste tipo contra o tipo alvo. 
        Se o tipo alvo não estiver definido, retorna 1 (neutro).
        """

        if tipo_alvo is None:
            return 1

        nome_alvo = tipo_alvo.get_nome()
    
        if nome_alvo in self.__efetividade:
            return self.__efetividade[nome_alvo]
    
        return 1


    def __str__(self):
        return self.__nome
    

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
        