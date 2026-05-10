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

        def remover_status (self, status):
            """Remove um status, mas somente se ele estiver aplicado ao Pokémon.""" 
            if status in self.__status:
                self.__status.remove(status)
       
        def esta_desmaiado(self):
            """Retorna True se o Pokémon está sem vida e fora de combate."""
            return self.__vida_atual == 0
