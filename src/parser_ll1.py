# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Analisador sintático LL(1) — definição da gramática.
#
# Neste commit: construirGramatica() com cálculo de FIRST, FOLLOW e tabela LL(1).
# O parser com pilha (parsear) e a construção da AST (gerarArvore)
# serão adicionados nos próximos commits.

from __future__ import annotations

from .lexer_fsm import (
    Token,
    Erros,
    TIPO_ABRE,
    TIPO_FECHA,
    TIPO_IDENT,
    TIPO_KEYWORD,
    TIPO_NUMERO,
    TIPO_OPERADOR,
)


# --------------------------------------------------------------
# Símbolos terminais (vocabulário do parser)
# --------------------------------------------------------------

T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"
T_NUMERO = "NUMERO"
T_IDENT = "IDENT"
T_RES = "RES"
T_START = "START"
T_END = "END"
T_IF = "IF"
T_WHILE = "WHILE"
T_IFELSE = "IFELSE"
T_EOF = "$"

# operadores binários aceitos em (A B op)
BINOPS = {"+", "-", "*", "/", "|", "%", "^", ">", "<", "==", "!=", ">=", "<="}


def _token_para_terminal(token: Token) -> str:
    """Converte um Token do lexer no terminal equivalente na gramática."""
    if token.tipo == TIPO_ABRE:
        return T_LPAREN
    if token.tipo == TIPO_FECHA:
        return T_RPAREN
    if token.tipo == TIPO_NUMERO:
        return T_NUMERO
    if token.tipo == TIPO_IDENT:
        return T_IDENT
    if token.tipo == TIPO_KEYWORD:
        if token.valor == "RES":
            return T_RES
        if token.valor == "START":
            return T_START
        if token.valor == "END":
            return T_END
        if token.valor == "IF":
            return T_IF
        if token.valor == "WHILE":
            return T_WHILE
        if token.valor == "IFELSE":
            return T_IFELSE
    if token.tipo == TIPO_OPERADOR and token.valor in BINOPS:
        return token.valor
    raise Erros(f"Token não mapeado para terminal: {token.tipo}:{token.valor}")


# --------------------------------------------------------------
# Gramática como lista de produções
# --------------------------------------------------------------
EPSILON = "ε"


def _definicao_gramatica() -> list[tuple[str, list[str]]]:
    producoes: list[tuple[str, list[str]]] = []

    # 0: ponto de entrada do programa
    producoes.append(("program", [T_LPAREN, T_START, T_RPAREN, "body"]))
    # 1: body sempre começa consumindo o LPAREN (fatoração à esquerda)
    producoes.append(("body", [T_LPAREN, "body_tail"]))
    # 2,3: body_tail decide se encontramos o END ou mais um statement
    producoes.append(("body_tail", [T_END, T_RPAREN]))
    producoes.append(("body_tail", ["expr_body", T_RPAREN, "body"]))
    # 4: toda expressão é um item seguido de resto
    producoes.append(("expr_body", ["item", "rest1"]))
    # 5,6: rest1
    producoes.append(("rest1", []))  # ε
    producoes.append(("rest1", ["item", "rest2"]))
    # 7-10: rest2
    producoes.append(("rest2", []))  # ε
    producoes.append(("rest2", ["binop"]))
    producoes.append(("rest2", ["kw_ctrl3"]))
    producoes.append(("rest2", ["item", "item_tail"]))
    # 11: item_tail
    producoes.append(("item_tail", ["kw_ctrl4"]))
    # 12-15: os tipos possíveis de item
    producoes.append(("item", [T_NUMERO]))
    producoes.append(("item", [T_IDENT]))
    producoes.append(("item", [T_RES]))
    producoes.append(("item", [T_LPAREN, "expr_body", T_RPAREN]))
    # uma produção por operador binário
    for op in ("+", "-", "*", "/", "|", "%", "^", ">", "<", "==", "!=", ">=", "<="):
        producoes.append(("binop", [op]))
    # palavras-chave de controle
    producoes.append(("kw_ctrl3", [T_IF]))
    producoes.append(("kw_ctrl3", [T_WHILE]))
    producoes.append(("kw_ctrl4", [T_IFELSE]))

    return producoes


# --------------------------------------------------------------
# FIRST / FOLLOW
# --------------------------------------------------------------


def _eh_terminal(simbolo: str, nao_terminais: set[str]) -> bool:
    return simbolo not in nao_terminais


def _calcular_first(
    producoes: list[tuple[str, list[str]]],
    nao_terminais: set[str],
) -> dict[str, set[str]]:
    first: dict[str, set[str]] = {nt: set() for nt in nao_terminais}

    mudou = True
    while mudou:
        mudou = False
        for lhs, rhs in producoes:
            if not rhs:
                if EPSILON not in first[lhs]:
                    first[lhs].add(EPSILON)
                    mudou = True
                continue

            anulavel = True
            for sim in rhs:
                if _eh_terminal(sim, nao_terminais):
                    if sim not in first[lhs]:
                        first[lhs].add(sim)
                        mudou = True
                    anulavel = False
                    break
                antes = len(first[lhs])
                first[lhs].update(first[sim] - {EPSILON})
                if len(first[lhs]) != antes:
                    mudou = True
                if EPSILON not in first[sim]:
                    anulavel = False
                    break
            if anulavel:
                if EPSILON not in first[lhs]:
                    first[lhs].add(EPSILON)
                    mudou = True
    return first


def _first_de_sequencia(
    seq: list[str],
    first: dict[str, set[str]],
    nao_terminais: set[str],
) -> set[str]:
    """FIRST de uma cadeia de símbolos."""
    resultado: set[str] = set()
    if not seq:
        resultado.add(EPSILON)
        return resultado
    for sim in seq:
        if _eh_terminal(sim, nao_terminais):
            resultado.add(sim)
            return resultado
        resultado.update(first[sim] - {EPSILON})
        if EPSILON not in first[sim]:
            return resultado
    resultado.add(EPSILON)
    return resultado


def _calcular_follow(
    producoes: list[tuple[str, list[str]]],
    nao_terminais: set[str],
    first: dict[str, set[str]],
    inicial: str,
) -> dict[str, set[str]]:
    follow: dict[str, set[str]] = {nt: set() for nt in nao_terminais}
    follow[inicial].add(T_EOF)

    mudou = True
    while mudou:
        mudou = False
        for lhs, rhs in producoes:
            for i, sim in enumerate(rhs):
                if sim not in nao_terminais:
                    continue
                cauda = rhs[i + 1:]
                first_cauda = _first_de_sequencia(cauda, first, nao_terminais)
                antes = len(follow[sim])
                follow[sim].update(first_cauda - {EPSILON})
                if EPSILON in first_cauda or not cauda:
                    follow[sim].update(follow[lhs])
                if len(follow[sim]) != antes:
                    mudou = True
    return follow


def _construir_tabela_ll1(
    producoes: list[tuple[str, list[str]]],
    nao_terminais: set[str],
    first: dict[str, set[str]],
    follow: dict[str, set[str]],
) -> dict[tuple[str, str], int]:
    tabela: dict[tuple[str, str], int] = {}
    conflitos: list[str] = []

    for idx, (lhs, rhs) in enumerate(producoes):
        first_rhs = _first_de_sequencia(rhs, first, nao_terminais)
        for term in first_rhs - {EPSILON}:
            chave = (lhs, term)
            if chave in tabela and tabela[chave] != idx:
                conflitos.append(
                    f"Conflito LL(1) em [{lhs}, {term}]: produções {tabela[chave]} e {idx}"
                )
            tabela[chave] = idx
        if EPSILON in first_rhs:
            for term in follow[lhs]:
                chave = (lhs, term)
                if chave in tabela and tabela[chave] != idx:
                    conflitos.append(
                        f"Conflito LL(1) em [{lhs}, {term}]: produções {tabela[chave]} e {idx}"
                    )
                tabela[chave] = idx

    if conflitos:
        raise Erros("Gramática não é LL(1):\n  " + "\n  ".join(conflitos))
    return tabela


# --------------------------------------------------------------
# API pública: construirGramatica
# --------------------------------------------------------------


def construirGramatica() -> dict:
    """Cria as produções, calcula FIRST/FOLLOW e monta a tabela LL(1)."""
    producoes = _definicao_gramatica()

    nao_terminais: set[str] = set()
    terminais: set[str] = {T_EOF}
    for lhs, rhs in producoes:
        nao_terminais.add(lhs)
    for lhs, rhs in producoes:
        for sim in rhs:
            if sim not in nao_terminais:
                terminais.add(sim)

    inicial = producoes[0][0]
    first = _calcular_first(producoes, nao_terminais)
    follow = _calcular_follow(producoes, nao_terminais, first, inicial)
    tabela = _construir_tabela_ll1(producoes, nao_terminais, first, follow)

    return {
        "producoes": producoes,
        "nao_terminais": nao_terminais,
        "terminais": terminais,
        "inicial": inicial,
        "first": first,
        "follow": follow,
        "tabela": tabela,
    }
