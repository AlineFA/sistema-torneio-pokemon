class ErroNomeMuitoLongo(Exception):
    """Classe que administra o sistema caso seja inserido nomes 
    com mais caracteres do que os limites estabelecidos"""
    pass

class ErroPokemonExcedido(Exception):
    """Classe que administra erro caso sejam inseridos mais pokémons
    do que o permitido pelo sistema"""
    pass

class ErroTreinadorDuplicado(Exception):
    """Classe que administra o erro caso um mesmo treinador seja 
    inserido numa mesma batalha mais de uma vez"""
    pass

class ErroValorInvalido(Exception):
    """Classe que administra o erro caso seja inserido um valor 
    inválido em algum campo, exemplo: vida do pokémon ultrapassar
    255"""
    pass

class ErroTipoDadoInvalido(Exception):
    """Classe que admnistra o erro caso o dado inserido seja inválido.
    Exemplo: se o dado precisar ser um inteiro e for inserida uma
    string"""
    pass

