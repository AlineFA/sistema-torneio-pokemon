class ErroNomeMuitoLongo(Exception):
    """Classe que administra o sistema caso seja inserido nomes 
    com mais caracteres do que os limites estabelecidos"""
    pass

class ErroPokemonExcedido(Exception):
    """Classe que administra erro caso sejam inseridos mais pokémons
    do que o permitido pelo sistema"""
    pass


class ErroValorInvalido(Exception):
    """
    Classe que administra o erro caso seja inserido um valor 
    inválido em algum campo. 
    Exemplo: vida do pokémon ultrapassar 255
    """
    pass


class ErroElementoDuplicado(Exception):
    """
    Classe que adminsitra o erro caso o elemento já tenha sido cadastrado.
    Exemplo: golpe já existente
    """
    pass


class ErroEntradaInvalida(Exception):
    """
    Erro para entradas inválidas fornecidas ao sistema.

    Exemplos:
    string em campo numérico
    tipo inexistente
    golpe não cadastrado
    item não implementado
    """
    pass