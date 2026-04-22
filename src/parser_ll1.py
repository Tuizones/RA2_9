# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Analisador sintático LL(1) — parser com pilha e saídas de derivação.
#
# Neste commit adicionamos:
#   parsear(tokens, gram)              — roda o parser LL(1) com pilha explícita
#   _descreve(token, terminal)         — formata um token para mensagens de erro
#   derivacao_para_texto(derivacao)    — lista numerada das produções aplicadas
#   derivacao_para_texto_tabela(...)   — tabela markdown passo a passo
#
# A função gerarArvore (que constrói a AST semântica) será adicionada
# pelo Arthur no próximo commit.

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
# Símbolos terminais
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

BINOPS = {"+", "-", "*", "/", "|", "%", "^", ">", "<", "==", "!=", ">=", "<="}


def _token_para_terminal(token: Token) -> str:
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


EPSILON = "ε"


def _definicao_gramatica() -> list[tuple[str, list[str]]]:
    producoes: list[tuple[str, list[str]]] = []
    producoes.append(("program", [T_LPAREN, T_START, T_RPAREN, "body"]))
    producoes.append(("body", [T_LPAREN, "body_tail"]))
    producoes.append(("body_tail", [T_END, T_RPAREN]))
    producoes.append(("body_tail", ["expr_body", T_RPAREN, "body"]))
    producoes.append(("expr_body", ["item", "rest1"]))
    producoes.append(("rest1", []))
    producoes.append(("rest1", ["item", "rest2"]))
    producoes.append(("rest2", []))
    producoes.append(("rest2", ["binop"]))
    producoes.append(("rest2", ["kw_ctrl3"]))
    producoes.append(("rest2", ["item", "item_tail"]))
    producoes.append(("item_tail", ["kw_ctrl4"]))
    producoes.append(("item", [T_NUMERO]))
    producoes.append(("item", [T_IDENT]))
    producoes.append(("item", [T_RES]))
    producoes.append(("item", [T_LPAREN, "expr_body", T_RPAREN]))
    for op in ("+", "-", "*", "/", "|", "%", "^", ">", "<", "==", "!=", ">=", "<="):
        producoes.append(("binop", [op]))
    producoes.append(("kw_ctrl3", [T_IF]))
    producoes.append(("kw_ctrl3", [T_WHILE]))
    producoes.append(("kw_ctrl4", [T_IFELSE]))
    return producoes


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


# --------------------------------------------------------------
# Parser LL(1) com pilha
# --------------------------------------------------------------


def parsear(tokens: list[Token], tabela_ll1: dict) -> dict:
    # Parser LL(1) dirigido por tabela com pilha explícita.
    # Mantemos uma pilha com o que ainda esperamos ver.
    # A cada passo:
    #   - se o topo é terminal e casa com o token atual -> consome
    #   - se o topo é não-terminal -> consulta a tabela e expande
    # Cada expansão é registrada em `derivacao` e em `passos`.
    producoes = tabela_ll1["producoes"]
    tabela = tabela_ll1["tabela"]
    inicial = tabela_ll1["inicial"]
    nao_terminais = tabela_ll1["nao_terminais"]

    entrada: list[tuple[str, Token | None]] = [
        (_token_para_terminal(tok), tok) for tok in tokens
    ]
    entrada.append((T_EOF, None))

    pilha: list[str] = [T_EOF, inicial]
    derivacao: list[dict] = []
    passos: list[dict] = []
    i = 0

    while pilha:
        pilha_snap = list(pilha)
        topo = pilha.pop()
        terminal_atual, token_atual = entrada[i]

        if topo == T_EOF:
            if terminal_atual == T_EOF:
                passos.append({"tipo": "casa", "pilha": pilha_snap, "pos": i, "simbolo": T_EOF})
                break
            raise Erros(
                f"Entrada extra após o fim do programa: {_descreve(token_atual, terminal_atual)}"
            )

        if topo not in nao_terminais:
            if topo == terminal_atual:
                passos.append({"tipo": "casa", "pilha": pilha_snap, "pos": i, "simbolo": topo})
                i += 1
                continue
            raise Erros(
                f"Erro sintático: esperado '{topo}' mas encontrado "
                f"{_descreve(token_atual, terminal_atual)}"
            )

        chave = (topo, terminal_atual)
        if chave not in tabela:
            raise Erros(
                f"Erro sintático: não há produção para [{topo}, {terminal_atual}] "
                f"(token {_descreve(token_atual, terminal_atual)})"
            )
        idx = tabela[chave]
        lhs, rhs = producoes[idx]
        passos.append({"tipo": "expande", "pilha": pilha_snap, "pos": i,
                       "idx": idx, "lhs": lhs, "rhs": list(rhs)})
        derivacao.append({"idx": idx, "lhs": lhs, "rhs": list(rhs), "pos_token": i})
        for sim in reversed(rhs):
            pilha.append(sim)

    if i != len(entrada) - 1:
        terminal_atual, token_atual = entrada[i]
        raise Erros(
            f"Erro sintático: tokens extras após o programa "
            f"({_descreve(token_atual, terminal_atual)})"
        )

    return {"derivacao": derivacao, "passos": passos, "tokens": tokens}


def _descreve(token: Token | None, terminal: str) -> str:
    if token is None:
        return f"'$' (fim de entrada, terminal {terminal})"
    return f"'{token.valor}' (linha {token.linha}, coluna {token.coluna})"


# --------------------------------------------------------------
# Utilitários de apresentação
# --------------------------------------------------------------


def derivacao_para_texto(derivacao: list[dict]) -> str:
    linhas: list[str] = []
    for i, passo in enumerate(derivacao, start=1):
        rhs = " ".join(passo["rhs"]) if passo["rhs"] else "ε"
        linhas.append(f"{i:03d}. {passo['lhs']} -> {rhs}")
    return "\n".join(linhas)


def derivacao_para_texto_tabela(passos: list[dict], tokens: list[Token]) -> str:
    MAX_PILHA = 50
    MAX_ENT   = 40

    def _pilha_str(snap: list[str]) -> str:
        s = " ".join(reversed(snap))
        return s if len(s) <= MAX_PILHA else s[:MAX_PILHA - 1] + "…"

    def _ent_str(pos: int) -> str:
        vals = [t.valor for t in tokens[pos:pos + 10]]
        if pos + 10 < len(tokens):
            vals.append("…")
        if not vals:
            vals = ["$"]
        s = " ".join(vals)
        return s if len(s) <= MAX_ENT else s[:MAX_ENT - 1] + "…"

    linhas: list[str] = []
    linhas.append("# Derivação LL(1) — Passo a Passo")
    linhas.append("")
    linhas.append("| Passo | Pilha (topo →) | Entrada (→) | Ação |")
    linhas.append("|------:|---|---|---|")
    for n, p in enumerate(passos, start=1):
        pilha_s = _pilha_str(p["pilha"])
        ent_s   = _ent_str(p["pos"])
        if p["tipo"] == "expande":
            rhs = " ".join(p["rhs"]) if p["rhs"] else "ε"
            acao = f"Expande: `{p['lhs']}` → `{rhs}`"
        else:
            acao = f"Casa: `{p['simbolo']}`"
        linhas.append(f"| {n} | `{pilha_s}` | `{ent_s}` | {acao} |")
    return "\n".join(linhas)
