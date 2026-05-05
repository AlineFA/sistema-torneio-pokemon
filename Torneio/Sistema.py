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