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
    def fmt_set(s: set) -> str:
        return "{ " + ", ".join(sorted(s)) + " }" if s else "{ }"

    md: list[str] = []

    md.append("# Gramática LL(1)")
    md.append("")

    md.append("## 1. Regras de Produção")
    md.append("")
    md.append("| # | Não-Terminal | Produção |")
    md.append("|---|---|---|")
    for i, (lhs, rhs) in enumerate(g["producoes"]):
        corpo = " ".join(rhs) if rhs else "ε"
        md.append(f"| {i} | {lhs} | {corpo} |")

    md.append("")

    md.append("## 2. Conjuntos FIRST")
    md.append("")
    md.append("| Não-Terminal | FIRST |")
    md.append("|---|---|")
    for nt in sorted(g["nao_terminais"]):
        md.append(f"| {nt} | {fmt_set(g['first'][nt])} |")

    md.append("")

    md.append("## 3. Conjuntos FOLLOW")
    md.append("")
    md.append("| Não-Terminal | FOLLOW |")
    md.append("|---|---|")
    for nt in sorted(g["nao_terminais"]):
        md.append(f"| {nt} | {fmt_set(g['follow'][nt])} |")

    md.append("")

    md.append("## 4. Tabela de Análise LL(1)")
    md.append("")
    md.append("| Não-Terminal | Terminal | Produção |")
    md.append("|---|---|---|")
    for (nt, t), idx in sorted(g["tabela"].items()):
        lhs, rhs = g["producoes"][idx]
        corpo = " ".join(rhs) if rhs else "ε"
        md.append(f"| {nt} | {t} | {lhs} → {corpo} |")

    return "\n".join(md)


def _arvore_para_markdown(arvore: dict, arquivo_fonte: str) -> str:
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

    Path(args.gramatica_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.gramatica_out).write_text(
        _dump_gramatica(resultado["gramatica"]) + "\n",
        encoding="utf-8",
    )

    Path(args.derivacao_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.derivacao_out).write_text(
        derivacao_para_texto_tabela(resultado["passos"], resultado["tokens"]) + "\n",
        encoding="utf-8",
    )

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
