# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Analisador léxico usando AFD (autômato finito determinístico).
# Implementado só com funções de estado, sem usar regex.
# Cada estado do autômato é uma função que recebe um caractere e decide
# pra qual estado ir.
#
# FASE 2: adicionamos as palavras reservadas START, END, IF, IFELSE, WHILE.
# Os operadores relacionais e o operador | serão adicionados no próximo commit.
#
# Estados: inicial, numero, numero_decimal, identificador, barra
#
# Tokens: NUMERO, OPERADOR (+,-,*,/,//,%,^), PARENTESE_ABRE,
#         PARENTESE_FECHA, IDENTIFICADOR (nomes de memória), KEYWORD

from dataclasses import dataclass


class Erros(Exception):
    pass


@dataclass
class Token:
    """Um token com tipo, valor e posição na linha."""
    tipo: str
    valor: str
    linha: int
    coluna: int


TIPO_NUMERO = "NUMERO"
TIPO_OPERADOR = "OPERADOR"
TIPO_ABRE = "PARENTESE_ABRE"
TIPO_FECHA = "PARENTESE_FECHA"
TIPO_IDENT = "IDENTIFICADOR"
TIPO_KEYWORD = "KEYWORD"

# Palavras reservadas — adicionamos START, END, IF, IFELSE, WHILE para a Fase 2.
# Antes só tinha RES; agora checamos a set completa.
PALAVRAS_RESERVADAS = {"RES", "START", "END", "IF", "IFELSE", "WHILE"}


def _eh_digito(char: str) -> bool:
    return "0" <= char <= "9"


def _eh_maiuscula(char: str) -> bool:
    return "A" <= char <= "Z"


def _eh_minuscula(char: str) -> bool:
    return "a" <= char <= "z"


def _adicionar_token(contexto: dict, tipo: str, valor: str) -> None:
    """Cria um Token e joga na lista."""
    contexto["tokens"].append(
        Token(tipo=tipo, valor=valor, linha=contexto["linha"], coluna=contexto["inicio_token"] + 1)
    )


def estado_inicial(char: str, contexto: dict) -> tuple[str, bool]:
    if char in (" ", "\t", "\r", "\n"):
        return "inicial", True

    if char == "(":
        contexto["inicio_token"] = contexto["i"]
        _adicionar_token(contexto, TIPO_ABRE, "(")
        contexto["paren"] += 1
        return "inicial", True

    if char == ")":
        contexto["inicio_token"] = contexto["i"]
        if contexto["paren"] <= 0:
            raise Erros(f"Linha {contexto['linha']}: ')' sem '(' correspondente")
        contexto["paren"] -= 1
        _adicionar_token(contexto, TIPO_FECHA, ")")
        return "inicial", True

    if _eh_digito(char):
        contexto["buffer"] = char
        contexto["inicio_token"] = contexto["i"]
        return "numero", True

    if _eh_maiuscula(char):
        contexto["buffer"] = char
        contexto["inicio_token"] = contexto["i"]
        return "identificador", True

    if char in "+-*%^":
        contexto["inicio_token"] = contexto["i"]
        _adicionar_token(contexto, TIPO_OPERADOR, char)
        return "inicial", True

    if char == "/":
        contexto["buffer"] = "/"
        contexto["inicio_token"] = contexto["i"]
        return "barra", True

    if char == ".":
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"número malformado — ponto sem dígito antes"
        )

    if _eh_minuscula(char):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"identificadores devem usar apenas letras maiúsculas, encontrado '{char}'"
        )

    raise Erros(f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: caractere inválido '{char}'")


def estado_numero(char: str, contexto: dict) -> tuple[str, bool]:
    if _eh_digito(char):
        contexto["buffer"] += char
        return "numero", True

    if char == ".":
        contexto["buffer"] += char
        return "numero_decimal", True

    if _eh_maiuscula(char) or _eh_minuscula(char):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"número malformado '{contexto['buffer'] + char}' — letra após número"
        )

    _adicionar_token(contexto, TIPO_NUMERO, contexto["buffer"])
    contexto["buffer"] = ""
    return "inicial", False


def estado_numero_decimal(char: str, contexto: dict) -> tuple[str, bool]:
    if _eh_digito(char):
        contexto["buffer"] += char
        return "numero_decimal", True

    if char == ".":
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"número malformado '{contexto['buffer'] + char}' — múltiplos pontos decimais"
        )

    if contexto["buffer"].endswith("."):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i']}: "
            f"número malformado '{contexto['buffer']}' — ponto sem dígitos depois"
        )

    if _eh_maiuscula(char) or _eh_minuscula(char):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"número malformado '{contexto['buffer'] + char}' — letra após número"
        )

    _adicionar_token(contexto, TIPO_NUMERO, contexto["buffer"])
    contexto["buffer"] = ""
    return "inicial", False


def estado_identificador(char: str, contexto: dict) -> tuple[str, bool]:
    if _eh_maiuscula(char):
        contexto["buffer"] += char
        return "identificador", True

    if _eh_minuscula(char):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"identificador '{contexto['buffer'] + char}' contém letra minúscula"
        )

    if _eh_digito(char):
        raise Erros(
            f"Linha {contexto['linha']}, coluna {contexto['i'] + 1}: "
            f"identificador '{contexto['buffer'] + char}' contém dígito"
        )

    valor = contexto["buffer"]
    # agora checamos a set completa (inclui todas as palavras-chave da Fase 2)
    if valor in PALAVRAS_RESERVADAS:
        _adicionar_token(contexto, TIPO_KEYWORD, valor)
    else:
        _adicionar_token(contexto, TIPO_IDENT, valor)
    contexto["buffer"] = ""
    return "inicial", False


def estado_barra(char: str, contexto: dict) -> tuple[str, bool]:
    if char == "/":
        _adicionar_token(contexto, TIPO_OPERADOR, "//")
        contexto["buffer"] = ""
        return "inicial", True
    _adicionar_token(contexto, TIPO_OPERADOR, "/")
    contexto["buffer"] = ""
    return "inicial", False


def _finalizar(contexto: dict, estado: str) -> None:
    if estado == "numero":
        _adicionar_token(contexto, TIPO_NUMERO, contexto["buffer"])
    elif estado == "numero_decimal":
        if contexto["buffer"].endswith("."):
            raise Erros(f"Linha {contexto['linha']}: número malformado '{contexto['buffer']}'")
        _adicionar_token(contexto, TIPO_NUMERO, contexto["buffer"])
    elif estado == "identificador":
        valor = contexto["buffer"]
        if valor in PALAVRAS_RESERVADAS:
            _adicionar_token(contexto, TIPO_KEYWORD, valor)
        else:
            _adicionar_token(contexto, TIPO_IDENT, valor)
    elif estado == "barra":
        _adicionar_token(contexto, TIPO_OPERADOR, "/")

    if contexto["paren"] != 0:
        raise Erros(f"Linha {contexto['linha']}: parênteses desbalanceados")


def tokenizar_linha(linha: str, numero_linha: int = 1) -> list[Token]:
    contexto = {
        "tokens": [],
        "buffer": "",
        "i": 0,
        "inicio_token": 0,
        "linha": numero_linha,
        "paren": 0,
    }

    estado = "inicial"
    maquina = {
        "inicial": estado_inicial,
        "numero": estado_numero,
        "numero_decimal": estado_numero_decimal,
        "identificador": estado_identificador,
        "barra": estado_barra,
    }

    chars = linha + "\n"
    while contexto["i"] < len(chars):
        char = chars[contexto["i"]]
        proximo_estado, avancar = maquina[estado](char, contexto)
        estado = proximo_estado
        if avancar:
            contexto["i"] += 1

    _finalizar(contexto, estado)
    return contexto["tokens"]


def tokenizar_programa(linhas: list[str]) -> list[Token]:
    """Tokeniza todas as linhas preservando a numeração de linha."""
    todos: list[Token] = []
    for idx, linha in enumerate(linhas, start=1):
        todos.extend(tokenizar_linha(linha, numero_linha=idx))
    return todos
