# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Ponto de entrada do programa (Fase 2 — Analisador Sintático LL(1)).
# Uso: python main.py <arquivo.txt>
#
# O fluxo completo que acontece quando você roda o programa:
#   1) lerArquivo        -> abre o .txt e lê linha por linha
#   2) lexer             -> transforma cada linha em tokens (salva em output/)
#   3) lerTokens         -> relê os tokens do arquivo (integração com a Fase 1)
#   4) construirGramatica-> monta gramática + calcula FIRST/FOLLOW + tabela LL(1)
#   5) dump da gramática -> salva produções/FIRST/FOLLOW/tabela em output/gramatica_dump.md
#   6) parsear           -> roda o parser com pilha e gera a derivação
#   7) gerarArvore       -> constrói a AST a partir dos tokens e salva
#   8) gerarAssembly     -> percorre a AST e emite código ARMv7

import argparse
import sys
from pathlib import Path

from src.lexer_fsm import Erros
from src.pipeline import executar_fase2, exibirResultados
from src.parser_ll1 import derivacao_para_texto_tabela, arvore_para_texto


def _dump_gramatica(g: dict) -> str:
    # Gera um arquivo markdown com as seções exigidas pelo enunciado:
    # algoritmo de construção, produções numeradas, conjuntos FIRST/FOLLOW,
    # tabela de análise LL(1) no formato plano e no formato matricial 2D.
    def fmt_set(s: set) -> str:
        return "{ " + ", ".join(sorted(s)) + " }" if s else "{ }"

    md: list[str] = []

    md.append("# Gramática LL(1)")
    md.append("")

    # --- 0. Algoritmo de construção da tabela LL(1) ---
    md.append("## 0. Algoritmo de Construção da Tabela de Análise LL(1)")
    md.append("")
    md.append("Para cada regra de produção **A → α** na gramática:")
    md.append("")
    md.append("1. Para cada terminal **a** ∈ FIRST(α):")
    md.append("   - Adicione a produção **A → α** na célula **Tabela[A, a]**.")
    md.append("2. Se **ε** ∈ FIRST(α):")
    md.append("   - Para cada terminal **b** ∈ FOLLOW(A):")
    md.append("     - Adicione **A → α** na célula **Tabela[A, b]**.")
    md.append("     - Isso inclui **$** se ele estiver em FOLLOW(A).")
    md.append("3. Qualquer célula não preenchida = **erro sintático**.")
    md.append("4. Se alguma célula receber **duas ou mais produções** distintas")
    md.append("   = **conflito LL(1)** (a gramática **não** é LL(1)).")
    md.append("")
    md.append("> Implementado em `_construir_tabela_ll1()` dentro de `src/parser_ll1.py`.")
    md.append("> O algoritmo itera até ponto-fixo para FIRST e FOLLOW antes de preencher a tabela.")
    md.append("")

    # --- 1. Regras de Produção ---
    md.append("## 1. Regras de Produção")
    md.append("")
    md.append("| # | Não-Terminal | Produção |")
    md.append("|---|---|---|")
    for i, (lhs, rhs) in enumerate(g["producoes"]):
        corpo = " ".join(rhs) if rhs else "ε"
        md.append(f"| {i} | {lhs} | {corpo} |")

    md.append("")

    # --- 2. Conjuntos FIRST ---
    md.append("## 2. Conjuntos FIRST")
    md.append("")
    md.append("FIRST(A) = conjunto de terminais que podem **iniciar** uma derivação de A.")
    md.append("Se A pode derivar ε, então ε ∈ FIRST(A).")
    md.append("")
    md.append("| Não-Terminal | FIRST |")
    md.append("|---|---|")
    for nt in sorted(g["nao_terminais"]):
        md.append(f"| {nt} | {fmt_set(g['first'][nt])} |")

    md.append("")

    # --- 3. Conjuntos FOLLOW ---
    md.append("## 3. Conjuntos FOLLOW")
    md.append("")
    md.append("FOLLOW(A) = terminais que podem aparecer **imediatamente após** A.")
    md.append("$ ∈ FOLLOW(símbolo inicial) sempre. ε nunca pertence a FOLLOW.")
    md.append("")
    md.append("| Não-Terminal | FOLLOW |")
    md.append("|---|---|")
    for nt in sorted(g["nao_terminais"]):
        md.append(f"| {nt} | {fmt_set(g['follow'][nt])} |")

    md.append("")

    # --- 4. Tabela de Análise LL(1) — formato plano ---
    md.append("## 4. Tabela de Análise LL(1) — Formato Plano")
    md.append("")
    md.append("Cada entrada M[A, a] lista a produção a aplicar.")
    md.append("Entradas ausentes = erro sintático.")
    md.append("")
    md.append("| Não-Terminal (A) | Terminal (a) | Produção |")
    md.append("|---|---|---|")
    for (nt, t), idx in sorted(g["tabela"].items()):
        lhs, rhs = g["producoes"][idx]
        corpo = " ".join(rhs) if rhs else "ε"
        md.append(f"| {nt} | {t} | #{idx}: {lhs} → {corpo} |")

    md.append("")

    # --- 5. Tabela de Análise LL(1) — formato matricial 2D ---
    # O número na célula é o índice da produção (ver seção 1).
    # Colunas divididas em dois grupos para caber em markdown.
    md.append("## 5. Tabela de Análise LL(1) — Formato Matricial M[A, a]")
    md.append("")
    md.append("Número na célula = índice da produção (seção 1). `—` = erro sintático.")
    md.append("")

    # preserva a ordem dos não-terminais conforme aparecem nas produções
    nt_order: list[str] = []
    _seen: set[str] = set()
    for lhs, _ in g["producoes"]:
        if lhs not in _seen:
            nt_order.append(lhs)
            _seen.add(lhs)

    all_terms_in_table = sorted(set(t for (_, t) in g["tabela"].keys()))

    # Grupo A: tokens literais, palavras-chave e EOF
    kws = {"LPAREN", "RPAREN", "NUMERO", "IDENT", "RES",
           "END", "IF", "WHILE", "IFELSE", "START", "$"}
    group_a = [t for t in all_terms_in_table if t in kws]
    group_b = [t for t in all_terms_in_table if t not in kws]

    for titulo, grp in [
        ("Grupo A — Tokens, palavras-chave e $", sorted(group_a)),
        ("Grupo B — Operadores", sorted(group_b)),
    ]:
        if not grp:
            continue
        md.append(f"### {titulo}")
        md.append("")
        md.append("| NT \\ T | " + " | ".join(grp) + " |")
        md.append("|---|" + "---|" * len(grp))
        for nt in nt_order:
            cells = []
            has_entry = False
            for term in grp:
                key = (nt, term)
                if key in g["tabela"]:
                    cells.append(f"**#{g['tabela'][key]}**")
                    has_entry = True
                else:
                    cells.append("—")
            if has_entry:
                md.append(f"| `{nt}` | " + " | ".join(cells) + " |")
        md.append("")

    return "\n".join(md)


def _arvore_para_markdown(arvore: dict, arquivo_fonte: str) -> str:
    # Gera o arquivo markdown com a representação textual da árvore sintática.
    # O enunciado exige que a árvore esteja num arquivo markdown do repositório.
    md: list[str] = []
    md.append("# Árvore Sintática")
    md.append("")
    md.append(f"Gerada a partir de: `{arquivo_fonte}`")
    md.append("")
    md.append("```")
    md.append(arvore_para_texto(arvore))
    md.append("```")
    return "\n".join(md)


def _resumo_linhas(arvore: dict) -> list[dict]:
    # A exibirResultados() espera uma lista de dicts com 'descricao'.
    # Esta função percorre a AST e monta essa lista com um texto simples
    # para cada statement do programa.
    descricoes: list[dict] = []
    for stmt in arvore.get("stmts", []):
        tipo = stmt["tipo"]
        if tipo == "mem_write":
            descricoes.append({"descricao": f"escrita em memória {stmt['nome']}"})
        elif tipo == "mem_read":
            descricoes.append({"descricao": f"leitura de memória {stmt['nome']}"})
        elif tipo == "res_ref":
            descricoes.append({"descricao": f"referência a {stmt['linhas_atras']} linha(s) atrás"})
        elif tipo == "binary":
            descricoes.append({"descricao": f"operação binária ({stmt['op']})"})
        elif tipo == "if":
            descricoes.append({"descricao": "estrutura IF"})
        elif tipo == "ifelse":
            descricoes.append({"descricao": "estrutura IFELSE"})
        elif tipo == "while":
            descricoes.append({"descricao": "estrutura WHILE"})
        else:
            descricoes.append({"descricao": tipo})
    return descricoes


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisador Sintático LL(1) — Fase 2")
    parser.add_argument("arquivo", help="Arquivo-fonte com o programa")
    parser.add_argument("--out", default="output/ultima_execucao.s", help="Assembly de saída")
    parser.add_argument(
        "--tokens-out",
        default="output/tokens_ultima_execucao.txt",
        help="Arquivo de saída dos tokens",
    )
    parser.add_argument(
        "--arvore-out",
        default="output/arvore_ultima_execucao.json",
        help="Arquivo de saída da árvore sintática (JSON)",
    )
    parser.add_argument(
        "--derivacao-out",
        default="output/derivacao_ultima_execucao.md",
        help="Arquivo markdown com a derivação LL(1) passo a passo",
    )
    parser.add_argument(
        "--gramatica-out",
        default="output/gramatica_dump.md",
        help="Arquivo markdown com produções, FIRST/FOLLOW e tabela LL(1)",
    )
    args = parser.parse_args()

    try:
        resultado = executar_fase2(
            caminho_fonte=args.arquivo,
            caminho_tokens=args.tokens_out,
            caminho_asm=args.out,
            caminho_arvore=args.arvore_out,
        )
    except Erros as erro:
        print(f"[ERRO] {erro}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as erro:
        print(f"[ERRO] arquivo não encontrado: {erro.filename}", file=sys.stderr)
        sys.exit(1)

    # salva o dump da gramática em markdown (produções, FIRST, FOLLOW, tabela LL(1))
    Path(args.gramatica_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.gramatica_out).write_text(
        _dump_gramatica(resultado["gramatica"]) + "\n",
        encoding="utf-8",
    )

    # salva a derivação no formato de tabela LL(1) (Pilha | Entrada | Ação)
    # bem mais fácil de seguir do que uma lista numerada
    Path(args.derivacao_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.derivacao_out).write_text(
        derivacao_para_texto_tabela(resultado["passos"], resultado["tokens"]) + "\n",
        encoding="utf-8",
    )

    # salva a árvore em markdown (exigência do enunciado sec. 11.4)
    caminho_arvore_md = Path(args.arvore_out).with_suffix(".md")
    caminho_arvore_md.write_text(
        _arvore_para_markdown(resultado["arvore"], args.arquivo) + "\n",
        encoding="utf-8",
    )

    exibirResultados(_resumo_linhas(resultado["arvore"]))

    print()
    print("Árvore Sintática:")
    print(arvore_para_texto(resultado["arvore"]))

    print()
    print(f"Gramática salva em    : {args.gramatica_out}")
    print(f"Tokens salvos em      : {args.tokens_out}")
    print(f"Derivação salva em    : {args.derivacao_out}")
    print(f"Árvore salva em       : {args.arvore_out} + {caminho_arvore_md.name}")
    print(f"Assembly gerado em    : {args.out}")


if __name__ == "__main__":
    main()
