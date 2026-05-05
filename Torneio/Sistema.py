class Tipo:

    def __init__(self, nome, efetividade):
        self.__nome = nome
        self.__efetividade = efetividade

    def get_nome(self):
        return self.__nome

    def get_efetividade(self):
        return self.__efetividade

    def multiplicador_efetividade(self, tipo_alvo):
        nome_alvo = tipo_alvo.get_nome()
    
        if nome_alvo in self.__efetividade:
            return self.__efetividade[nome_alvo]
    
        return 1