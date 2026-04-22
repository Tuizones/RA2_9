# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Analisador sintático LL(1) — todo o maquinário do parser está aqui.
#
# Funções principais:
#   construirGramatica()  — define as produções e calcula FIRST, FOLLOW e tabela
#   parsear(tokens, gram) — roda o parser com pilha, gerando a derivação passo a passo
#   gerarArvore(resultado)— constrói a AST semântica a partir dos tokens
#
# A linguagem é baseada em notação pós-fixada (RPN), sempre entre parênteses.
# Todo programa começa com (START) e termina com (END).
#
# Gramática que definimos (minúsculas = não-terminais, MAIÚSCULAS = terminais):
#
#   program    -> LPAREN START RPAREN body
#   body       -> LPAREN body_tail
#   body_tail  -> END RPAREN                        # fim do programa
#              |  expr_body RPAREN body              # mais um statement
#   expr_body  -> item rest1
#   rest1      -> ε                                 # (MEM) — só um item
#              |  item rest2
#   rest2      -> ε                                 # (V MEM) ou (N RES)
#              |  binop                              # (A B op)
#              |  kw_ctrl3                           # (COND BLOCO IF/WHILE)
#              |  item item_tail
#   item_tail  -> kw_ctrl4                           # (COND THEN ELSE IFELSE)
#   item       -> NUMERO | IDENT | RES
#              |  LPAREN expr_body RPAREN
#   binop      -> + | - | * | / | | | % | ^
#              |  > | < | == | != | >= | <=
#   kw_ctrl3   -> IF | WHILE
#   kw_ctrl4   -> IFELSE

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
    producoes.append(("program", [T_LPAREN, T_START, T_RPAREN, "body"]))
    producoes.append(("body", [T_LPAREN, "body_tail"]))
    producoes.append(("body_tail", [T_END, T_RPAREN]))
    producoes.append(("body_tail", ["expr_body", T_RPAREN, "body"]))
    producoes.append(("expr_body", ["item", "rest1"]))
    producoes.append(("rest1", []))  # ε
    producoes.append(("rest1", ["item", "rest2"]))
    producoes.append(("rest2", []))  # ε
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
# gerarArvore: constrói a AST semântica a partir dos tokens
#
# A derivação LL(1) é útil para ver o processo de parsing, mas para gerar
# assembly é muito mais prático ter uma AST com nós com significado.
# Por isso re-parseamos os tokens de forma recursiva descendente aqui.


def gerarArvore(resultado_parse: dict) -> dict:
    tokens: list[Token] = resultado_parse["tokens"]
    pos = [0]  # cursor mutável

    def esperar_terminal(terminal: str, valor: str | None = None) -> Token:
        if pos[0] >= len(tokens):
            raise Erros(f"Fim inesperado; esperado {terminal}")
        tok = tokens[pos[0]]
        t = _token_para_terminal(tok)
        if t != terminal or (valor is not None and tok.valor != valor):
            raise Erros(
                f"Esperado {terminal}{' ' + valor if valor else ''} mas veio "
                f"{_descreve(tok, t)}"
            )
        pos[0] += 1
        return tok

    def parse_item() -> dict:
        tok = tokens[pos[0]]
        t = _token_para_terminal(tok)
        if t == T_NUMERO:
            pos[0] += 1
            return {"tipo": "number", "valor": tok.valor}
        if t == T_IDENT:
            pos[0] += 1
            return {"tipo": "ident", "valor": tok.valor}
        if t == T_RES:
            pos[0] += 1
            return {"tipo": "keyword", "valor": "RES"}
        if t == T_LPAREN:
            return parse_expr()
        raise Erros(f"Item inválido: {_descreve(tok, t)}")

    def parse_expr() -> dict:
        esperar_terminal(T_LPAREN)
        primeiro = parse_item()

        tok = tokens[pos[0]]
        t = _token_para_terminal(tok)

        # (item)  ->  mem_read
        if t == T_RPAREN:
            pos[0] += 1
            if primeiro["tipo"] != "ident":
                raise Erros("Comando (MEM) exige identificador em letras maiúsculas")
            return {"tipo": "mem_read", "nome": primeiro["valor"]}

        segundo = parse_item()
        tok = tokens[pos[0]]
        t = _token_para_terminal(tok)

        # dois itens + ')'
        if t == T_RPAREN:
            pos[0] += 1
            # (N RES)
            if segundo.get("tipo") == "keyword" and segundo.get("valor") == "RES":
                if primeiro.get("tipo") != "number" or not _eh_int_nao_negativo(primeiro.get("valor", "")):
                    raise Erros("Comando (N RES) exige N inteiro não negativo")
                return {"tipo": "res_ref", "linhas_atras": int(primeiro["valor"])}
            # (V MEM)
            if segundo.get("tipo") == "ident":
                return {"tipo": "mem_write", "nome": segundo["valor"], "valor": primeiro}
            raise Erros("Expressão de dois itens inválida")

        # binop + ')'
        if tok.tipo == TIPO_OPERADOR and tok.valor in BINOPS:
            pos[0] += 1
            esperar_terminal(T_RPAREN)
            return {"tipo": "binary", "op": tok.valor, "esq": primeiro, "dir": segundo}

        # kw_ctrl3 + ')'
        if t == T_IF:
            pos[0] += 1
            esperar_terminal(T_RPAREN)
            return {"tipo": "if", "cond": primeiro, "then_block": segundo}
        if t == T_WHILE:
            pos[0] += 1
            esperar_terminal(T_RPAREN)
            return {"tipo": "while", "cond": primeiro, "body": segundo}

        # terceiro item -> (COND THEN ELSE IFELSE)
        terceiro = parse_item()
        kw = tokens[pos[0]]
        kw_t = _token_para_terminal(kw)
        if kw_t != T_IFELSE:
            raise Erros(
                f"Expressão de 3 itens exige IFELSE como quarto símbolo, "
                f"veio {_descreve(kw, kw_t)}"
            )
        pos[0] += 1
        esperar_terminal(T_RPAREN)
        return {
            "tipo": "ifelse",
            "cond": primeiro,
            "then_block": segundo,
            "else_block": terceiro,
        }

    # program: ( START ) stmt_list ( END )
    esperar_terminal(T_LPAREN)
    esperar_terminal(T_START, "START")
    esperar_terminal(T_RPAREN)

    stmts: list[dict] = []
    while True:
        if pos[0] >= len(tokens):
            raise Erros("Programa não foi finalizado com (END)")
        tok = tokens[pos[0]]
        if (
            tok.tipo == TIPO_ABRE
            and pos[0] + 2 < len(tokens)
            and tokens[pos[0] + 1].tipo == TIPO_KEYWORD
            and tokens[pos[0] + 1].valor == "END"
            and tokens[pos[0] + 2].tipo == TIPO_FECHA
        ):
            break
        stmts.append(parse_expr())

    esperar_terminal(T_LPAREN)
    esperar_terminal(T_END, "END")
    esperar_terminal(T_RPAREN)
    if pos[0] != len(tokens):
        tok = tokens[pos[0]]
        raise Erros(f"Tokens extras após (END): {_descreve(tok, _token_para_terminal(tok))}")

    return {"tipo": "program", "stmts": stmts}


def _eh_int_nao_negativo(valor: str) -> bool:
    if not valor:
        return False
    for ch in valor:
        if ch < "0" or ch > "9":
            return False
    return True


# --------------------------------------------------------------
# Utilitários de apresentação
# --------------------------------------------------------------


def arvore_para_texto(no: dict, nivel: int = 0) -> str:
    ident = "  " * nivel
    tipo = no.get("tipo")
    if tipo == "program":
        linhas = [f"{ident}program"]
        for s in no["stmts"]:
            linhas.append(arvore_para_texto(s, nivel + 1))
        return "\n".join(linhas)
    if tipo == "number":
        return f"{ident}number({no['valor']})"
    if tipo == "ident":
        return f"{ident}ident({no['valor']})"
    if tipo == "keyword":
        return f"{ident}keyword({no['valor']})"
    if tipo == "res_ref":
        return f"{ident}res_ref(linhas_atras={no['linhas_atras']})"
    if tipo == "mem_read":
        return f"{ident}mem_read({no['nome']})"
    if tipo == "mem_write":
        linhas = [f"{ident}mem_write({no['nome']})"]
        linhas.append(arvore_para_texto(no["valor"], nivel + 1))
        return "\n".join(linhas)
    if tipo == "binary":
        linhas = [f"{ident}binary({no['op']})"]
        linhas.append(arvore_para_texto(no["esq"], nivel + 1))
        linhas.append(arvore_para_texto(no["dir"], nivel + 1))
        return "\n".join(linhas)
    if tipo == "if":
        linhas = [f"{ident}if"]
        linhas.append(f"{ident}  cond:")
        linhas.append(arvore_para_texto(no["cond"], nivel + 2))
        linhas.append(f"{ident}  then:")
        linhas.append(arvore_para_texto(no["then_block"], nivel + 2))
        return "\n".join(linhas)
    if tipo == "ifelse":
        linhas = [f"{ident}ifelse"]
        linhas.append(f"{ident}  cond:")
        linhas.append(arvore_para_texto(no["cond"], nivel + 2))
        linhas.append(f"{ident}  then:")
        linhas.append(arvore_para_texto(no["then_block"], nivel + 2))
        linhas.append(f"{ident}  else:")
        linhas.append(arvore_para_texto(no["else_block"], nivel + 2))
        return "\n".join(linhas)
    if tipo == "while":
        linhas = [f"{ident}while"]
        linhas.append(f"{ident}  cond:")
        linhas.append(arvore_para_texto(no["cond"], nivel + 2))
        linhas.append(f"{ident}  body:")
        linhas.append(arvore_para_texto(no["body"], nivel + 2))
        return "\n".join(linhas)
    return f"{ident}{tipo}?"


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
