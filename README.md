# RA2 9 — Analisador Sintático LL(1) com Geração de Assembly ARMv7

| | |
|---|---|
| **Instituição** | Pontifícia Universidade Católica do Paraná |
| **Disciplina** | Linguagens Formais e Compiladores |
| **Professor** | Frank Coelho de Alcantara |
| **Grupo Canvas** | RA2 9 |
| **Fase** | 2 Analisador Sintático LL(1) |
| **Ano/Semestre** | 2026 / 1° Semestre |
|||

### Integrantes
| Nome | Usuário GitHub |
|---|---|
| Arthur Felipe Bach Biancolini | Tuizones |
| Emanuel Riceto da Silva | emanuelriceto |
| Frederico Virmond Fruet | fredfruet |

> **Índice rápido:**
> [O que o projeto faz](#1-o-que-o-projeto-faz) ·
> [Fundamentos teóricos](#1bis-fundamentos-teóricos-llk) ·
> [Pipeline](#2-pipeline-end-to-end) ·
> [Estrutura de arquivos](#3-estrutura-do-repositório) ·
> [A linguagem](#4-a-linguagem) ·
> [Como executar](#5-como-executar) ·
> [Gramática LL(1)](#6-gramática-ll1) ·
> [FIRST e FOLLOW](#7-conjuntos-first-e-follow) ·
> [Tabela de Análise](#8-tabela-de-análise-ll1) ·
> [Como o parser funciona](#9-como-o-parser-funciona) ·
> [A AST](#10-a-árvore-sintática-ast) ·
> [Geração de Assembly](#11-geração-de-assembly) ·
> [Testes](#12-arquivos-de-teste) ·
> [Tratamento de erros](#13-tratamento-de-erros) ·
> [Distribuição do trabalho](#14-distribuição-do-trabalho) ·
> [Referências](#15-referências)

---

## 1. O que o projeto faz

Este projeto é um **Compilador**: lê um arquivo-fonte
escrito numa linguagem RPN (Notação Polonesa Reversa) personalizada, valida
a sintaxe com um **parser LL(1)**, constrói uma **Árvore Sintática Abstrata
(AST)** e gera **código Assembly ARMv7** pronto para rodar no simulador
[CPUlator DE1-SoC](https://cpulator.01xz.net/?sys=arm-de1soc).

### O que é LL(1)?

Um parser **LL(1)** lê a entrada da **esquerda para a direita** (*Left-to-right*),
produz uma derivação mais à **esquerda** (*Leftmost*) e precisa de apenas
**1 símbolo de lookahead** para decidir qual regra aplicar — sem retrocesso,
sem ambiguidade.

Ele usa uma **pilha** e uma **tabela de decisão** `M[não-terminal, terminal]`:

```
Pilha: [ PROGRAM  $  ]     Token corrente: (
→ consulta M[PROGRAM, (]  →  expande: PROGRAM → "(" start ")" BODY
Pilha: [ "(" start ")" BODY $ ]
→ topo "(" casa com (   →  consome token
→ topo start  casa com lexema START   → consome
...
```

---

<a id="1bis-fundamentos-teóricos-llk"></a>

## 1.bis. Fundamentos Teóricos — Por que LL(1)?

Esta seção condensa a teoria de Linguagens Formais e Compiladores que **justifica**
cada decisão de projeto da nossa gramática e do nosso parser. Todas as escolhas
que você verá no código (ordem das regras, fatoração de `BODY`, `REST1`/`REST2`
anuláveis, palavras-chave no fim de cada estrutura de controle) são consequência
direta dos conceitos abaixo.

### 1.bis.1. Hierarquia das Gramáticas (perspectiva LL)

```
Gram_LL(k+1)  ⊃  Gram_LL(k)  ⊃  …  ⊃  Gram_LL(1)  ⊃  Gram_Regulares
```

- **LL(k)** — gramáticas reconhecidas por parsers _top-down_ que derivam
  **L**eftmost, lendo da esquerda (**L**eft-to-right) com `k` símbolos de
  lookahead. Quanto maior o `k`, mais gramáticas aceitas — `LL(1)` é o caso
  mais restrito (e o mais usado por ser eficiente e implementável à mão).
- **LL(1)** — apenas **1** símbolo de lookahead basta para escolher a
  produção. Garantida pela **condição LL(1)** (ver § 1.bis.4).
- **Regulares** — caso particular: `A → a` ou `A → aB`. Equivalentes a
  autômatos finitos / expressões regulares (justamente a Fase 1 deste projeto).

Neste trabalho usamos **LL(1)** porque queremos um parser implementado à mão,
legível, com tabela construída automaticamente e diagnóstico de erro preciso.

### 1.bis.2. Classificação de Parsers Top-down

```mermaid
flowchart TD
    P[parsers top-down] --> RD[recursive descent<br/>uma função por não-terminal]
    P --> LL["LL(k)\n dirigido por tabela"]
    LL --> PRED["predictive parser\n tabela M[A,a]\n + pilha + 1 lookahead"]

    classDef ours fill:#dcfce7,stroke:#16a34a,stroke-width:2px
    class LL,PRED ours
```

O caminho destacado em verde é o que implementamos: parser **top-down**,
**LL(1)**, **dirigido por tabela** (predictive parser).

### 1.bis.3. Ambiguidade vs. Previsibilidade

Uma gramática é **ambígua** se existe alguma sentença `w` da linguagem que
admite **duas árvores de derivação distintas** (ou, equivalentemente, duas
derivações leftmost diferentes). Ambiguidade é uma propriedade **semântica**
da gramática.

**LL(1) é uma propriedade mais forte** que não-ambiguidade:

- Toda gramática `LL(1)` é não-ambígua. 
- Existem gramáticas não-ambíguas que **não** são `LL(1)` (por exemplo, com
  recursão à esquerda ou prefixos comuns não-fatorados). 

O parser `LL(1)` precisa decidir **qual produção aplicar** olhando **apenas
1 símbolo à frente**. Para isso, a tabela `M[A, a]` deve ter **no máximo uma
entrada** por célula — a chamada **condição LL(1)**.

### 1.bis.4. A Condição LL(1) (FIRST disjuntos)

> **Definição formal** — Para todo não-terminal `A` com produções
> `A → α₁ | α₂ | … | αₙ`, vale:
>
> 1. `FIRST(αᵢ) ∩ FIRST(αⱼ) = ∅` para todo `i ≠ j`.
> 2. Se `ε ∈ FIRST(αᵢ)` para algum `i`, então
>    `FIRST(αⱼ) ∩ FOLLOW(A) = ∅` para todo `j ≠ i`.

Na prática isso significa: **olhando 1 token, só uma regra é aplicável**.
Duas situações típicas violam essa condição e exigem reescrita da gramática:

#### Recursão à esquerda

`A → A α | β` faz o parser tentar expandir `A` para sempre, sem consumir
token algum (loop infinito). A transformação canônica é:

```
A   → β A'
A'  → α A' | ε
```

_Aplicação no nosso projeto:_ não temos recursão à esquerda direta porque
**toda** expressão da linguagem começa obrigatoriamente com `(`, e
`EXPR_BODY → ITEM REST1` consome esse `(` (via `ITEM → "(" EXPR_BODY ")"`)
antes de qualquer recursão.

#### Fatoração à esquerda

Duas regras com prefixo comum (`A → α β₁ | α β₂`) impedem decisão preditiva.
A transformação canônica fatora o prefixo:

```
A   → α A'
A'  → β₁ | β₂
```

_Aplicação no nosso projeto:_ tanto **"fim do programa"** `(END)` quanto
**"mais um statement"** `(EXPR…)` começam com `(`. Em vez de

```
BODY → "(" end ")"
     | "(" EXPR_BODY ")" BODY      ← prefixo comum "("
```

fatoramos para:

```
BODY      → "(" BODY_TAIL
BODY_TAIL → end ")"
          | EXPR_BODY ")" BODY     ← agora 1 lookahead resolve
```

Após consumir o `(`, o próximo token (`end` vs. `numero`/`ident`/`(`/`res`)
identifica unicamente qual alternativa aplicar.

### 1.bis.5. Por que palavras-chave no FINAL

Em linguagens tradicionais (C, Java) a palavra-chave aparece no **início**:
`if (cond) { … }`. Numa linguagem RPN como a nossa, **a sintaxe pós-fixada
facilita LL(1)**: colocando `IF`/`WHILE`/`IFELSE` no fim, o parser primeiro
lê todos os operandos como `ITEM` e só depois usa um lookahead para decidir
se é um operador binário, uma estrutura de controle de 3 elementos
(`IF`/`WHILE`) ou de 4 (`IFELSE`):

```
REST2 → ε                  ; (V MEM)  ou  (N RES)
      | BINOP               ; (A B op)
      | KW_CTRL3            ; (COND BLOCO IF/WHILE)
      | ITEM ITEM_TAIL      ; (COND THEN ELSE IFELSE)
```

Os `FIRST` de cada alternativa são **disjuntos** por construção:
`FIRST(BINOP) = {+,-,*,/,…}`, `FIRST(KW_CTRL3) = {IF, WHILE}`,
`FIRST(ITEM) = {(, numero, ident, RES}` — sem sobreposição. ✓

---

## 2. Pipeline end-to-end

Tudo que acontece ao rodar `python main.py teste1.txt`:

```mermaid
flowchart LR
    A[("teste1.txt")] --> B["lerArquivo()"]
    B --> C["tokenizar_linha()\n(AFD da Fase 1)"]
    C --> D[("tokens_ultima\n_execucao.txt")]
    D --> E["lerTokens()"]
    F["construirGramatica()\nFIRST · FOLLOW · Tabela"] --> G
    E --> G["parsear()\n(LL(1) com pilha)"]
    G --> H["gerarArvore()"]
    H --> I[("arvore_ultima\n_execucao.json\n+ .md")]
    H --> J["gerarAssembly()"]
    J --> K[("ultima_execucao.s")]
    H --> L["exibirResultados()"]
    L --> M(["console"])
    F --> N[("gramatica_dump.md")]
    G --> O[("derivacao_ultima\n_execucao.md")]

    classDef io fill:#fef3c7,stroke:#d97706
    classDef step fill:#dbeafe,stroke:#1d4ed8
    class A,D,I,K,N,O io
    class B,C,E,G,H,J,L,F step
```

### Fluxo em palavras

1. **`lerArquivo`** — abre o `.txt`, ignora linhas em branco e comentários `#`.
2. **`tokenizar_linha`** — o AFD da Fase 1 classifica cada caractere em tokens
   (`NUMERO`, `IDENT`, `LPAREN`, operadores, keywords…).
3. **`lerTokens`** — relê os tokens do arquivo salvo (integração Fase 1 → Fase 2).
4. **`construirGramatica`** — monta as 32 produções, calcula FIRST e FOLLOW
   (algoritmo de ponto-fixo) e constrói a tabela LL(1).
5. **`parsear`** — roda o algoritmo de pilha, registrando cada passo.
6. **`gerarArvore`** — re-percorre os passos e constrói a AST semântica.
7. **`gerarAssembly`** — percorre a AST recursivamente emitindo instruções ARMv7.
8. Salva todos os artefatos em `output/`.

---

## 3. Estrutura do Repositório

```
.
├── main.py                              # Ponto de entrada (CLI)
├── README.md                            # Este arquivo
├── gramatica.md                         # Gramática formal (EBNF estendido)
├── docs/
│   └── diagramas.md                     # Diagramas Mermaid detalhados
│
├── teste1.txt                           # Programa de teste 1 (≥10 linhas)
├── teste2.txt                           # Programa de teste 2 (≥10 linhas)
├── teste3.txt                           # Programa de teste 3 (≥10 linhas)
├── teste_erro_lexico.txt                # Casos de erro léxico
├── teste_erro_sintatico.txt             # Casos de erro sintático
│
├── src/
│   ├── lexer_fsm.py                     # AFD tokenizador (Fase 1, reaproveitado)
│   ├── parser_ll1.py                    # Gramática + parser LL(1) + AST
│   ├── armv7_generator.py               # Gerador de Assembly ARMv7
│   └── pipeline.py                      # Funções obrigatórias do enunciado
│
├── tests/
│   ├── test_lexer.py                    # Testes do AFD léxico
│   └── test_pipeline.py                 # Testes do parser, AST e Assembly
│
└── output/                              # Artefatos da última execução
    ├── tokens_ultima_execucao.txt        # Tokens (TIPO:valor, um por linha)
    ├── derivacao_ultima_execucao.md      # Passo a passo da pilha LL(1)
    ├── arvore_ultima_execucao.json       # AST em JSON (consumível por Fase 3)
    ├── arvore_ultima_execucao.md         # AST em texto legível (markdown)
    ├── gramatica_dump.md                 # Produções + FIRST/FOLLOW + tabela
    └── ultima_execucao.s                 # Assembly ARMv7 pronto para o CPUlator
```

---

## 4. A Linguagem

Toda expressão é escrita em **Notação Polonesa Reversa (RPN)** entre parênteses:
`(operando1 operando2 operador)`. Um programa **sempre** começa com `(START)`
e termina com `(END)` — uma instrução por linha.

### 4.1. Operadores aritméticos

| Operador | Significado | Exemplo | Resultados |
|:---:|---|---|---|
| `+` | Adição | `(3 4 +)` | `7` |
| `-` | Subtração | `(10 3 -)` | `7` |
| `*` | Multiplicação | `(4 2.5 *)` | `10.0` |
| `\|` | Divisão **real** | `(10.0 4.0 \|)` | `2.5` |
| `/` | Divisão **inteira** | `(10 3 /)` | `3` |
| `%` | Resto da divisão inteira | `(10 3 %)` | `1` |
| `^` | Potenciação | `(2 5 ^)` | `32` |

> **Alterado de `\\` para `|` nessa atividade** 

### 4.2. Operadores relacionais

Retornam `1.0` (verdadeiro) ou `0.0` (falso), usados como condição nas
estruturas de controle.

| Operador | Significado | Exemplo |
|:---:|---|---|
| `>` | maior que | `((VARA) 0 >)` |
| `<` | menor que | `((X) 10 <)` |
| `==` | igual | `((FLAG) 1 ==)` |
| `!=` | diferente | `((CONT) 0 !=)` |
| `>=` | maior ou igual | `((VARA) 5 >=)` |
| `<=` | menor ou igual | `((N) 100 <=)` |

### 4.3. Comandos especiais

| Forma | Significado |
|---|---|
| `(V MEM)` | Armazena o valor `V` na memória chamada `MEM` |
| `(MEM)` | Lê o valor de `MEM` (retorna `0` se não inicializada) |
| `(N RES)` | Recupera o resultado da expressão `N` linhas atrás |

`MEM` é qualquer sequência de **letras maiúsculas** (`VARA`, `CONT`, `X`, `FLAG`…).
`RES` é palavra-reservada.

### 4.4. Estruturas de controle (definidas pelo grupo)

Usamos **palavras-chave no final** da expressão (estilo pós-fixado), o que
preserva o padrão RPN da linguagem e permite decisão com **1 símbolo de lookahead**.

| Estrutura | Sintaxe | Semântica |
|---|---|---|
| **IF** | `(COND BLOCO IF)` | Executa `BLOCO` se `COND ≠ 0` |
| **IFELSE** | `(COND THEN ELSE IFELSE)` | Executa `THEN` se `COND ≠ 0`, senão `ELSE` |
| **WHILE** | `(COND BLOCO WHILE)` | Repete `BLOCO` enquanto `COND ≠ 0` |

`COND`, `BLOCO`, `THEN` e `ELSE` são **expressões RPN válidas** (inclusive aninhadas).

**Exemplo completo** (retirado de `teste1.txt`):

```
(START)
(20 VARA)
(((VARA) 0 >)  ((VARA) 1 -) WHILE)
(((VARA) 5 >=) (1 FLAG) (0 FLAG) IFELSE)
(END)
```

### 4.5. Exemplo de aninhamento

```
((A (C D *) +))     → soma A com o produto de C e D
(((A B %) (D E *) /))  → divide o resto de A%B pelo produto D*E
```

---

## 5. Como Executar

### 5.1. Pré-requisitos

- **Python 3.10+** (nenhuma dependência externa)
- Para testes: `pip install pytest` (ou use `python -m pytest`)

### 5.2. Executar o analisador

```bash
python main.py teste1.txt
```

Saída no console:

```
Linha 1: operação binária (+)
Linha 2: operação binária (-)
...
Árvore Sintática:
program
  binary(+)
    number(10)
    number(3)
  ...

Gramática salva em    : output/gramatica_dump.md
Tokens salvos em      : output/tokens_ultima_execucao.txt
Derivação salva em    : output/derivacao_ultima_execucao.md
Árvore salva em       : output/arvore_ultima_execucao.json + arvore_ultima_execucao.md
Assembly gerado em    : output/ultima_execucao.s
```

### 5.3. Artefatos gerados

| Arquivo | Formato | Conteúdo |
|---|---|---|
| `tokens_ultima_execucao.txt` | texto | `linha_N;TIPO:valor,...` |
| `derivacao_ultima_execucao.md` | markdown | tabela passo a passo da pilha LL(1) |
| `arvore_ultima_execucao.json` | JSON | AST completa (usável na Fase 3) |
| `arvore_ultima_execucao.md` | markdown | AST em texto indentado |
| `gramatica_dump.md` | markdown | produções + FIRST/FOLLOW + tabela LL(1) |
| `ultima_execucao.s` | Assembly | código ARMv7 para o CPUlator |

### 5.4. Argumentos opcionais

```bash
python main.py teste2.txt \
  --out output/teste2.s \
  --tokens-out output/tokens_t2.txt \
  --arvore-out output/arvore_t2.json \
  --derivacao-out output/derivacao_t2.md \
  --gramatica-out output/gramatica_t2.md
```

### 5.5. Rodar os testes automatizados

```bash
python -m pytest tests/ -v
```

Resultado esperado: **37 testes**, todos passando.

### 5.6. Executar o Assembly no CPUlator

1. Abrir <https://cpulator.01xz.net/?sys=arm-de1soc>
2. Colar o conteúdo de `output/ultima_execucao.s` no editor
3. Pressionar **F7** (Compilar) e depois **F5** (Executar)
4. O resultado da última expressão aparece no display **HEX3–HEX0**

---

## 6. Gramática LL(1)

Convenção (ISO/IEC 14977 — EBNF):
**MAIÚSCULAS** = não-terminais · **minúsculas** = categorias léxicas
terminais (`numero`, `ident`) · **literais entre aspas** = terminais
exatos (`"("`, `"+"`, `if`) · `[ ]` opcional · `{ }` repetição (0+) ·
`|` alternativa · `ε` = cadeia vazia · `$` = fim de entrada.

### 6.1. Forma EBNF (canônica)

#### Como ler EBNF (símbolos da meta-linguagem)

| Símbolo | Significado |
|:---:|---|
| `=` | "é definido como" — abre a regra |
| `,` | **e depois** (concatenação / sequência). **Não é "ou".** |
| `\|` | **ou** (alternativa) |
| `{ X }` | **zero ou mais** ocorrências de `X` (repetição) |
| `[ X ]` | **opcional** — zero ou uma ocorrência de `X` |
| `( ... )` | agrupamento |
| `"texto"` | terminal literal exato |
| `;` | fim da regra |

> **Atenção:** em EBNF a vírgula significa **concatenação**, não escolha.
> `A , B` = "primeiro A, depois B"; `A | B` = "A ou B".

#### A gramática

```ebnf
PROGRAM   = "(" start ")" , { "(" EXPR_BODY ")" } , "(" end ")" ;
EXPR_BODY = ITEM
          | ITEM , ITEM , [ TAIL ] ;
TAIL      = BINOP
          | KW_CTRL3
          | ITEM , KW_CTRL4 ;
ITEM      = numero | ident | res | "(" , EXPR_BODY , ")" ;
BINOP     = "+" | "-" | "*" | "/" | "|" | "%" | "^"
          | ">" | "<" | "==" | "!=" | ">=" | "<=" ;
KW_CTRL3  = if | while ;
KW_CTRL4  = ifelse ;
```

#### Lendo cada regra em português

- **`PROGRAM`** — *uma* sequência fixa: `(start)` no início, depois
  **zero ou mais** blocos `(EXPR_BODY)`, depois `(end)` no fim.
  Não é uma escolha entre alternativas — é a estrutura única e
  obrigatória de qualquer programa válido.
- **`EXPR_BODY`** — o conteúdo de um statement, *sem* os parênteses
  externos. Pode ser **1 item** isolado (forma `(MEM)`) ou **2 itens
  obrigatórios** seguidos de uma `TAIL` opcional.
- **`TAIL`** — o "verbo" de uma expressão pós-fixada: um operador
  binário, uma keyword de 2 operandos (`if`/`while`) ou um terceiro
  item seguido de `ifelse` (4 itens no total).
- **`ITEM`** — um operando: número, identificador de memória, a
  palavra-chave `res`, ou uma sub-expressão completa entre parênteses
  (recursão que permite aninhamento arbitrário).
- **`BINOP`, `KW_CTRL3`, `KW_CTRL4`** — apenas listas de tokens
  terminais; servem para agrupar e dar nome.

#### Exemplo: derivando `(START) (10 3 +) (END)`

```
PROGRAM
  = "(" start ")"  ,  { "(" EXPR_BODY ")" }  ,  "(" end ")"
                       └─ uma iteração ─┘
                       └ EXPR_BODY = 10 , 3 , (TAIL = BINOP = "+")
```

A repetição `{ ... }` deu **uma** volta (um único statement no meio);
poderia ter dado zero (`(START)(END)`) ou várias.

> **Nota sobre caixa.** Na convenção EBNF, **terminais** são minúsculos
> (`start`, `end`, `if`, `while`, `ifelse`, `res`, `numero`, `ident`)
> ou literais entre aspas (`"("`, `"+"`). No código-fonte do programa
> a ser parseado, esses lexemas continuam sendo escritos em **MAIÚSCULAS**
> (ex.: `(START)`, `(IF …)`) — a tabela em [§ 1.3 de `gramatica.md`](gramatica.md#13-mapeamento-literal--s%C3%ADmbolo-interno)
> faz o mapeamento `lexema MAIÚSCULO ↔ terminal minúsculo` que o
> [`_token_para_terminal`](src/parser_ll1.py) implementa.

> **Por que ainda precisamos da BNF da § 6.2.** EBNF é ótima para
> humanos mas a tabela LL(1) só sabe consultar regras no formato
> `A → α` (sem `{ }` ou `[ ]`). Cada `{ ... }` e `[ ... ]` precisa ser
> traduzido para um novo não-terminal recursivo/anulável. Por exemplo,
> a repetição `{ "(" EXPR_BODY ")" } "(" end ")"` vira
> `BODY → "(" BODY_TAIL` com `BODY_TAIL` decidindo a cada iteração entre
> "acabou" (`end ")"`) e "vem mais um statement" (`EXPR_BODY ")" BODY`).
> Mesma informação, formato diferente.

### 6.2. Forma BNF fatorada (numerada — base da tabela LL(1))

A EBNF acima é traduzida para BNF onde cada `[ ]` / `{ }` vira um
não-terminal anulável (`REST1`, `REST2`, `ITEM_TAIL`, `BODY`,
`BODY_TAIL`). Esta numeração `#0..#31` é a usada na tabela `M[A, a]`
e em `output/derivacao_ultima_execucao.md`.

| # | Não-Terminal | Produção | Observação |
|:---:|---|---|---|
| 00 | `PROGRAM` | `"(" start ")" BODY` | raiz — toda entrada começa com `(START)` |
| 01 | `BODY` | `"(" BODY_TAIL` | consome `(` antes de decidir (fatoração à esquerda) |
| 02 | `BODY_TAIL` | `end ")"` | fim do programa |
| 03 | `BODY_TAIL` | `EXPR_BODY ")" BODY` | mais uma instrução + continua |
| 04 | `EXPR_BODY` | `ITEM REST1` | pelo menos 1 item por expressão |
| 05 | `REST1` | `ε` | expressão de 1 item: `(MEM)` |
| 06 | `REST1` | `ITEM REST2` | expressão de 2+ itens |
| 07 | `REST2` | `ε` | — |
| 08 | `REST2` | `BINOP` | operador binário aritmético/relacional |
| 09 | `REST2` | `KW_CTRL3` | keyword com 2 operandos (IF, WHILE) |
| 10 | `REST2` | `ITEM ITEM_TAIL` | 3 itens → IFELSE |
| 11 | `ITEM_TAIL` | `KW_CTRL4` | keyword com 3 operandos (IFELSE) |
| 12 | `ITEM` | `numero` | literal numérico |
| 13 | `ITEM` | `ident` | identificador de memória |
| 14 | `ITEM` | `res` | palavra-chave RES |
| 15 | `ITEM` | `"(" EXPR_BODY ")"` | sub-expressão aninhada |
| 16–22 | `BINOP` | `"+" "-" "*" "/" "\|" "%" "^"` | aritméticos |
| 23–28 | `BINOP` | `">" "<" "==" "!=" ">=" "<="` | relacionais |
| 29 | `KW_CTRL3` | `if` | |
| 30 | `KW_CTRL3` | `while` | |
| 31 | `KW_CTRL4` | `ifelse` | |

> **Mapeamento lexema ↔ terminal:** o lexer reconhece os lexemas
> em **maiúsculas** (`START`, `END`, `IF`, `WHILE`, `IFELSE`, `RES`)
> e a função `_token_para_terminal()` traduz cada um para o terminal
> correspondente em **minúsculas** (`start`, `end`, `if`, `while`,
> `ifelse`, `res`) usado nas produções acima e na tabela LL(1).
> Identificadores de memória (ex.: `VARA`) viram a categoria `ident`,
> e números (`10`, `3.14`) viram `numero`

### 6.3. Por que essa gramática é LL(1)?

Três decisões de projeto garantem que nunca há conflito:

**1. Fatoração à esquerda em `BODY`**

Sem fatoração, `BODY_TAIL` teria dois casos começando com `(`:
`(END)` e `(expressão…)`. Com a regra `BODY = "(" BODY_TAIL`,
consumimos o `(` primeiro e só então olhamos se o próximo token é
`end` ou início de expressão — 1 símbolo resolve.

**2. `REST1` e `REST2` anuláveis apenas quando necessário**

`REST1` vai para `ε` somente quando vê `)` (expressão de 1 item, ex: `(MEM)`).
Em qualquer outro caso, expande para `ITEM REST2`. Sem ambiguidade.

**3. Palavra-chave final para estruturas de controle**

`if`, `while` e `ifelse` aparecem **no final** da expressão pós-fixada.
Quando o parser está em `REST2`, um único lookahead distingue:
- operador aritmético/relacional → `BINOP`
- `if` ou `while` → `KW_CTRL3`
- outro item (terá `ifelse` depois) → `ITEM ITEM_TAIL`

A própria função `construirGramatica()` detecta conflitos em tempo de execução:
se uma célula da tabela recebesse 2 produções, lançaria
`Erros("Gramática não é LL(1):\n  M[A, t] tem múltiplas produções: ...")`
(ver `_construir_tabela_ll1` em `src/parser_ll1.py`).

### 6.4. Exemplos canônicos das transparências

Esta subseção aplica os algoritmos de transformação aos dois exemplos clássicos
usados nas aulas, reforçando o porquê da forma final da nossa gramática.

#### Recursão à esquerda — gramática de expressões aritméticas

```
E  → E + T  |  T          ← ambígua para LL(1) (recursão esquerda)
T  → T * F  |  F          ← ambígua para LL(1) (recursão esquerda)
F  → ( E )  |  id
```

Aplicando a transformação `A → Aα | β  ⇒  A → βA' ; A' → αA' | ε`:

```
E   → T E'
E'  → + T E'  |  ε
T   → F T'
T'  → * F T'  |  ε
F   → ( E )   |  id
```

Resultado: gramática equivalente, **sem recursão à esquerda**, parseável por LL(1).
Esta é a gramática padrão usada para construir o exemplo de tabela das transparências.

#### Fatoração à esquerda — if-then-else

```
S  → if E then S
   |  if E then S else S      ← prefixo "if E then S" comum ⚠
```

Aplicando `A → αβ₁ | αβ₂  ⇒  A → αA' ; A' → β₁ | β₂`:

```
S   → if E then S S'
S'  → else S  |  ε            ← 1 lookahead distingue
```

No nosso projeto, o problema análogo — dois statements começando com `(` —
foi resolvido pela mesma técnica em `BODY → "(" BODY_TAIL` (ver § 6.3).

---

## 7. Conjuntos FIRST e FOLLOW

### 7.1. Definições formais

> **FIRST(α)** — conjunto de **terminais** que podem **iniciar** uma cadeia
> derivada de α (sequência de terminais e não-terminais).
>
> **FOLLOW(A)** — conjunto de **terminais** que podem aparecer **imediatamente
> à direita** de `A` em alguma forma sentencial válida.

Ambos são calculados por **algoritmo de ponto-fixo** em
`construirGramatica()`: a regra é reaplicada até que nenhum conjunto cresça
mais.

### 7.2. Algoritmo de FIRST

| # | Caso | Ação |
|:---:|---|---|
| 1 | `X → a α` (terminal `a`) | adicione `a` a `FIRST(X)` |
| 2 | `X → Y α` (não-terminal `Y`) | adicione `FIRST(Y) − {ε}` a `FIRST(X)`. Se `ε ∈ FIRST(Y)`, repita o procedimento com o próximo símbolo de α |
| 3 | `X → Y₁ Y₂ … Yₙ` com **todos** os `Yᵢ` capazes de derivar `ε` | adicione `ε` a `FIRST(X)` |
| | (caso especial) `X → ε` | adicione `ε` a `FIRST(X)` |

Repetir até ponto fixo (nada novo adicionado em uma passagem completa).

**Como aplicamos no projeto** — trecho real de
[`src/parser_ll1.py`](src/parser_ll1.py) (`_calcular_first`):

```python
first: dict[str, set[str]] = {nt: set() for nt in nao_terminais}
mudou = True
while mudou:                              # ponto fixo
    mudou = False
    for lhs, rhs in producoes:
        if not rhs:                       # caso especial: A → ε
            if EPSILON not in first[lhs]:
                first[lhs].add(EPSILON); mudou = True
            continue
        anulavel = True
        for sim in rhs:                   # X1 X2 … Xn
            if _eh_terminal(sim, nao_terminais):    # caso 1
                first[lhs].add(sim); anulavel = False; break
            first[lhs].update(first[sim] - {EPSILON})  # caso 2
            if EPSILON not in first[sim]:
                anulavel = False; break
        if anulavel:                      # caso 3
            first[lhs].add(EPSILON)
```

**Lógica linha-a-linha:**
- `first = {nt: set()}` — começa todos os FIRST vazios; só vamos
  **adicionar** elementos (monotonia garante terminação).
- `while mudou` — laço de **ponto fixo**: continua enquanto algum
  conjunto crescer numa passagem completa.
- `if not rhs` — produção `A → ε`; o único caso em que `ε` entra
  diretamente em `FIRST(A)`.
- `anulavel = True` — flag que registra se **todos** os símbolos do
  RHS vistos até agora podem derivar `ε`. Se sim, ao final do laço
  o próprio `A` é anulável (caso 3).
- `if _eh_terminal(sim, ...)` — terminal: adiciona literalmente e
  para (`break`) — terminal nunca deriva `ε`.
- `first[lhs].update(first[sim] - {EPSILON})` — não-terminal: copia
  o FIRST dele **sem** o `ε` (o ε é mero sinalizador de
  "continue olhando o próximo símbolo").
- `if EPSILON not in first[sim]: break` — se o NT atual **não** é
  anulável, paramos: o que vem depois dele não influencia FIRST(A).
- O `if anulavel:` final cobre o caso 3: se todo o RHS pode sumir,
  então `A` também pode produzir a cadeia vazia.

A função auxiliar `_first_de_sequencia(seq)` calcula `FIRST` de uma
cadeia (`X1 X2 …`) seguindo o mesmo princípio — é a base do cálculo
de FOLLOW e da construção da tabela.

### 7.3. Algoritmo de FOLLOW

| # | Caso | Ação |
|:---:|---|---|
| 1 | `S` é o símbolo inicial | adicione `$` a `FOLLOW(S)` |
| 2 | Produção `A → α B β` | adicione `FIRST(β) − {ε}` a `FOLLOW(B)` |
| 3 | Produção `A → α B` ou `A → α B β` com `ε ∈ FIRST(β)` | adicione `FOLLOW(A)` a `FOLLOW(B)` |

> Note que **ε nunca entra em FOLLOW** — ele só aparece em FIRST como
> sinalizador de "propaga para o próximo símbolo".

A implementação em [src/parser_ll1.py](src/parser_ll1.py) (`_calcular_first`,
`_calcular_follow`) segue exatamente esse algoritmo.

**Como aplicamos no projeto** — trecho real de `_calcular_follow`:

```python
follow: dict[str, set[str]] = {nt: set() for nt in nao_terminais}
follow[inicial].add(T_EOF)                # caso 1: $ ∈ FOLLOW(S)
mudou = True
while mudou:
    mudou = False
    for lhs, rhs in producoes:            # A → α B β
        for i, sim in enumerate(rhs):
            if sim not in nao_terminais:
                continue
            cauda = rhs[i + 1:]           # β
            first_cauda = _first_de_sequencia(cauda, first, nao_terminais)
            follow[sim].update(first_cauda - {EPSILON})   # caso 2
            if EPSILON in first_cauda or not cauda:
                follow[sim].update(follow[lhs])           # caso 3
```

**Lógica linha-a-linha:**
- `follow[inicial].add(T_EOF)` — caso 1 do algoritmo: o símbolo
  inicial sempre tem `$` em seu FOLLOW (fim de entrada é o que
  vem "depois" da raiz).
- `for i, sim in enumerate(rhs)` — varremos cada posição do RHS.
  Só nos interessam **não-terminais** (terminais não têm FOLLOW).
- `cauda = rhs[i + 1:]` — é o `β` do algoritmo: tudo que aparece
  **depois** de `B` na produção `A → α B β`.
- `_first_de_sequencia(cauda, ...)` — calcula `FIRST(β)` (pode
  conter `ε` se toda a cauda for anulável).
- `follow[sim].update(first_cauda - {EPSILON})` — caso 2: tudo
  que pode aparecer **logo após** `B` (sem o ε, que não é terminal
  real).
- `if EPSILON in first_cauda or not cauda` — caso 3: se a cauda
  some (vazia ou anulável), então o que vem depois de `A` também
  vem depois de `B`, logo `FOLLOW(A) ⊆ FOLLOW(B)`.

Observe como o caso 3 ("se β deriva ε ou está ausente, propague
FOLLOW(A) para FOLLOW(B)") se traduz literalmente em uma linha:
`follow[sim].update(follow[lhs])`.

### 7.4. Conjuntos calculados para nossa gramática

> Nas tabelas abaixo os terminais aparecem na convenção EBNF:
> categorias léxicas em minúsculas (`numero`, `ident`) e literais entre
> aspas (`"("`, `"+"`) ou palavras-reservadas em minúsculas (`if`, `while`,
> `start`, `end`, `res`, `ifelse`). O dump auto-gerado em
> [output/gramatica_dump.md](output/gramatica_dump.md) usa o mesmo
> alfabeto.

### 7.5. FIRST

| Não-Terminal | FIRST |
|---|---|
| `PROGRAM`   | { `"("` } |
| `BODY`      | { `"("` } |
| `BODY_TAIL` | { `"("`, `end`, `ident`, `numero`, `res` } |
| `EXPR_BODY` | { `"("`, `ident`, `numero`, `res` } |
| `ITEM`      | { `"("`, `ident`, `numero`, `res` } |
| `REST1`     | { `"("`, `ident`, `numero`, `res`, `ε` } |
| `REST2`     | { `"("`, `ident`, `if`, `numero`, `res`, `while`, `"!="`, `"%"`, `"*"`, `"+"`, `"-"`, `"/"`, `"<"`, `"<="`, `"=="`, `">"`, `">="`, `"^"`, `"\|"`, `ε` } |
| `ITEM_TAIL` | { `ifelse` } |
| `BINOP`     | { `"!="`, `"%"`, `"*"`, `"+"`, `"-"`, `"/"`, `"<"`, `"<="`, `"=="`, `">"`, `">="`, `"^"`, `"\|"` } |
| `KW_CTRL3`  | { `if`, `while` } |
| `KW_CTRL4`  | { `ifelse` } |

### 7.6. FOLLOW

| Não-Terminal | FOLLOW |
|---|---|
| `PROGRAM`   | { `$` } |
| `BODY`      | { `$` } |
| `BODY_TAIL` | { `$` } |
| `EXPR_BODY` | { `")"` } |
| `ITEM`      | { `"("`, `")"`, `ident`, `if`, `ifelse`, `numero`, `res`, `while`, `"!="`, `"%"`, `"*"`, `"+"`, `"-"`, `"/"`, `"<"`, `"<="`, `"=="`, `">"`, `">="`, `"^"`, `"\|"` } |
| `REST1`     | { `")"` } |
| `REST2`     | { `")"` } |
| `ITEM_TAIL` | { `")"` } |
| `BINOP`     | { `")"` } |
| `KW_CTRL3`  | { `")"` } |
| `KW_CTRL4`  | { `")"` } |

---

## 8. Tabela de Análise LL(1)

### 8.1. Algoritmo de construção

Conforme apresentado nas aulas, a tabela `M[A, a]` é construída a partir dos
conjuntos FIRST e FOLLOW com o seguinte algoritmo:

> **Para cada regra de produção A → α:**
>
> | Passo | Condição | Ação |
> |:---:|---|---|
> | 1 | Para cada terminal **a** ∈ FIRST(α) | Adicione **A → α** em `M[A, a]` |
> | 2 | Se **ε** ∈ FIRST(α) | Para cada **b** ∈ FOLLOW(A): adicione **A → α** em `M[A, b]` |
> | 3 | Célula vazia | Erro sintático |
> | 4 | Célula com 2+ produções | Conflito LL(1) — gramática não é LL(1) |
>
> ε nunca é chave na tabela — é apenas o sinalizador de "propagar para FOLLOW".

O código Python que executa este algoritmo está em `src/parser_ll1.py` →
`_construir_tabela_ll1()`. A função detecta conflitos em tempo de execução.

**Como aplicamos no projeto** — trecho real:

```python
for idx, (lhs, rhs) in enumerate(producoes):
    first_rhs = _first_de_sequencia(rhs, first, nao_terminais)
    for term in first_rhs - {EPSILON}:                        # passo 1
        chave = (lhs, term)
        if chave in tabela and tabela[chave] != idx:          # passo 4
            conflitos.append(
                f"Conflito LL(1) em [{lhs}, {term}]: "
                f"produções {tabela[chave]} e {idx}")
        tabela[chave] = idx
    if EPSILON in first_rhs:                                  # passo 2
        for term in follow[lhs]:
            chave = (lhs, term)
            if chave in tabela and tabela[chave] != idx:
                conflitos.append(...)
            tabela[chave] = idx
if conflitos:
    raise Erros("Gramática não é LL(1):\n  " + "\n  ".join(conflitos))
```

**Lógica linha-a-linha:**
- `for idx, (lhs, rhs) in enumerate(producoes)` — cada produção
  recebe um índice estável (0..31). Esse índice é o que aparece
  nas células da tabela e na coluna "#" da derivação.
- `first_rhs = _first_de_sequencia(rhs, ...)` — calcula
  `FIRST(α)` para o lado direito da produção atual. Se o RHS for
  vazio, retorna `{ε}`.
- `for term in first_rhs - {EPSILON}` — **passo 1** do algoritmo:
  para cada terminal real em FIRST(α), `M[A, t] = idx`. ε é
  excluído porque não é terminal de entrada.
- `if chave in tabela and tabela[chave] != idx` — detecta
  conflito: a célula já está ocupada por outra produção. Note o
  `!= idx` — uma mesma produção pode contribuir 2 vezes via
  caminhos diferentes (FIRST + FOLLOW), e isso **não** é conflito.
- `if EPSILON in first_rhs` — **passo 2**: se a produção pode
  derivar `ε`, ela também responde por todos os terminais que
  podem aparecer **depois** de `A` (FOLLOW(A)).
- `raise Erros(...)` — se qualquer conflito foi detectado, a
  construção falha imediatamente. Isso é nosso teste empírico de
  que a gramática é LL(1).

Resultado para nossa gramática: **57 entradas, 0 conflitos** — confirmado a
cada execução em [output/gramatica_dump.md](output/gramatica_dump.md).

### 8.2. Entradas da tabela (formato plano)

Cada célula `M[A, a]` indica qual produção aplicar quando o **topo da pilha**
é o não-terminal `A` e o **token corrente** é `a`.
Células não listadas = **erro sintático**.

| M\[A, a\] | Produção |
|---|---|
| `M[PROGRAM, "("]` | `PROGRAM → "(" start ")" BODY` |
| `M[BODY, "("]` | `BODY → "(" BODY_TAIL` |
| `M[BODY_TAIL, end]` | `BODY_TAIL → end ")"` |
| `M[BODY_TAIL, "(" / numero / ident / res]` | `BODY_TAIL → EXPR_BODY ")" BODY` |
| `M[EXPR_BODY, "(" / numero / ident / res]` | `EXPR_BODY → ITEM REST1` |
| `M[REST1, ")"]` | `REST1 → ε` |
| `M[REST1, "(" / numero / ident / res]` | `REST1 → ITEM REST2` |
| `M[REST2, ")"]` | `REST2 → ε` |
| `M[REST2, "+" / "-" / "*" / … (operadores)]` | `REST2 → BINOP` |
| `M[REST2, if / while]` | `REST2 → KW_CTRL3` |
| `M[REST2, "(" / numero / ident / res]` | `REST2 → ITEM ITEM_TAIL` |
| `M[ITEM_TAIL, ifelse]` | `ITEM_TAIL → KW_CTRL4` |
| `M[ITEM, numero]` | `ITEM → numero` |
| `M[ITEM, ident]` | `ITEM → ident` |
| `M[ITEM, res]` | `ITEM → res` |
| `M[ITEM, "("]` | `ITEM → "(" EXPR_BODY ")"` |

### 8.3. Formato matricial M[A, a] — tabela completa

Número = índice da produção. `—` = erro sintático.
Uma única tabela com **todos** os terminais (tokens, palavras-chave, operadores e `$`).

| NT \ T | `$` | `"("` | `")"` | `numero` | `ident` | `end` | `res` | `if` | `while` | `ifelse` | `"+"` | `"-"` | `"*"` | `"/"` | `"\|"` | `"%"` | `"^"` | `">"` | `"<"` | `"=="` | `"!="` | `">="` | `"<="` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `PROGRAM`   | — | **0**  | — | —     | —     | —     | —     | —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `BODY`      | — | **1**  | — | —     | —     | —     | —     | —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `BODY_TAIL` | — | **3**  | — | **3** | **3** | **2** | **3** | —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `EXPR_BODY` | — | **4**  | — | **4** | **4** | —     | **4** | —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `ITEM`      | — | **15** | — | **12**| **13**| —     | **14**| —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `REST1`     | — | **6**  | **5** | **6** | **6** | —   | **6** | —    | —    | —     | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `REST2`     | — | **10** | **7** | **10**| **10**| —   | **10**| **9**| **9**| —     | **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8**| **8** |
| `ITEM_TAIL` | — | —      | — | —     | —     | —     | —     | —    | —    | **11**| — | — | — | — | — | — | — | — | — | — | — | — | — |
| `BINOP`     | — | —      | — | —     | —     | —     | —     | —    | —    | —     | **16**| **17**| **18**| **19**| **20**| **21**| **22**| **23**| **24**| **25**| **26**| **27**| **28** |
| `KW_CTRL3`  | — | —      | — | —     | —     | —     | —     | **29**| **30**| —    | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `KW_CTRL4`  | — | —      | — | —     | —     | —     | —     | —    | —    | **31**| — | — | — | — | — | — | — | — | — | — | — | — | — |

**Legenda — Regras de Produção** (número usado nas células acima)

| # | Produção |
|:---:|---|
| 0 | `PROGRAM → "(" start ")" BODY` |
| 1 | `BODY → "(" BODY_TAIL` |
| 2 | `BODY_TAIL → end ")"` |
| 3 | `BODY_TAIL → EXPR_BODY ")" BODY` |
| 4 | `EXPR_BODY → ITEM REST1` |
| 5 | `REST1 → ε` |
| 6 | `REST1 → ITEM REST2` |
| 7 | `REST2 → ε` |
| 8 | `REST2 → BINOP` |
| 9 | `REST2 → KW_CTRL3` |
| 10 | `REST2 → ITEM ITEM_TAIL` |
| 11 | `ITEM_TAIL → KW_CTRL4` |
| 12 | `ITEM → numero` |
| 13 | `ITEM → ident` |
| 14 | `ITEM → res` |
| 15 | `ITEM → "(" EXPR_BODY ")"` |
| 16 | `BINOP → "+"` |
| 17 | `BINOP → "-"` |
| 18 | `BINOP → "*"` |
| 19 | `BINOP → "/"` |
| 20 | `BINOP → "\|"` |
| 21 | `BINOP → "%"` |
| 22 | `BINOP → "^"` |
| 23 | `BINOP → ">"` |
| 24 | `BINOP → "<"` |
| 25 | `BINOP → "=="` |
| 26 | `BINOP → "!="` |
| 27 | `BINOP → ">="` |
| 28 | `BINOP → "<="` |
| 29 | `KW_CTRL3 → if` |
| 30 | `KW_CTRL3 → while` |
| 31 | `KW_CTRL4 → ifelse` |

A tabela completa com todas as 57 entradas é gerada automaticamente a cada
execução em [`output/gramatica_dump.md`](output/gramatica_dump.md).
A documentação formal com o algoritmo e a tabela estática está em
[`gramatica.md`](gramatica.md).

---

## 9. Como o Parser Funciona

### 9.0. Parser preditivo LL(1) dirigido por tabela

Nosso parser é **top-down, LL(1), dirigido por tabela**. Suas características:

| Aspecto | Implementação |
|---|---|
| Constrói a árvore | da **raiz** para as folhas |
| Estratégia | **expansão** de não-terminais |
| Derivação simulada | **leftmost** (sempre o não-terminal mais à esquerda) |
| Decisão-chave | qual produção **expandir** dado o lookahead |
| Estrutura de dados | **pilha** de símbolos esperados + buffer de tokens |
| Lookahead | **1 token** (`LL(1)`) |
| Tabela de decisão | `M[A, a]` construída a partir de FIRST/FOLLOW |
| Diagnóstico de erro | preciso — sabe exatamente qual conjunto de tokens era esperado |

A cada passo o parser olha o **topo da pilha** e o **token corrente**:
se o topo é terminal, casa-e-consome; se é não-terminal, consulta `M[topo, token]`
para descobrir qual produção aplicar.

### 9.1. O algoritmo de pilha

```python
gram   = construirGramatica()         # gramática + FIRST/FOLLOW + tabela
tokens = lerTokens("output/tokens_ultima_execucao.txt")
result = parsear(tokens, gram)        # derivação LL(1)
arv    = gerarArvore(result)          # AST semântica
asm    = gerarAssembly(arv)           # código ARMv7
```

Internamente, `parsear` mantém:
- **pilha** inicializada com `["PROGRAM", "$"]`
- **buffer de tokens** terminado com `$`

A cada iteração:

```mermaid
flowchart TD
    A([início]) --> B{"topo == '$'?"}
    B -- sim --> C{"token == '$'?"}
    C -- sim --> OK([aceita ✓])
    C -- não --> E1(["erro: tokens sobrando"])
    B -- não --> D{"topo é terminal?"}
    D -- sim --> E{"casa com\ntoken corrente?"}
    E -- sim --> F["consome token\ndesempilha topo\nregistra 'Casa: X'"]
    F --> A
    E -- não --> E2(["erro sintático"])
    D -- não --> G["consulta M[topo, token]"]
    G --> H{"existe\nprodução?"}
    H -- não --> E3(["erro sintático"])
    H -- sim --> I["registra 'Expande: A → α'\nempilha α invertido"]
    I --> A

    classDef err fill:#fee2e2,stroke:#dc2626
    classDef ok  fill:#dcfce7,stroke:#16a34a
    class E1,E2,E3 err
    class OK ok
```

**Como aplicamos no projeto** — núcleo real de `parsear()` em
[`src/parser_ll1.py`](src/parser_ll1.py):

```python
pilha: list[str] = [T_EOF, inicial]       # topo à direita (pop = topo)
i = 0
while pilha:
    topo = pilha.pop()
    terminal_atual, token_atual = entrada[i]

    if topo == T_EOF:                     # fim da pilha = aceita
        if terminal_atual == T_EOF: break
        raise Erros("Entrada extra após o fim do programa: ...")

    if topo not in nao_terminais:         # terminal: casa-e-consome
        if topo == terminal_atual:
            i += 1; continue
        raise Erros(f"esperado '{topo}' mas encontrado ...")

    chave = (topo, terminal_atual)        # não-terminal: consulta tabela
    if chave not in tabela:
        raise Erros(f"não há produção para [{topo}, {terminal_atual}]")
    idx = tabela[chave]
    lhs, rhs = producoes[idx]
    derivacao.append({"idx": idx, "lhs": lhs, "rhs": list(rhs)})
    for sim in reversed(rhs):             # empilha RHS invertido
        pilha.append(sim)
```

**Lógica linha-a-linha:**
- `pilha = [T_EOF, inicial]` — convenção: **topo à direita**
  (`pop()` retorna o último). O `$` no fundo casa com o `$` que
  acrescentamos ao buffer; quando os dois se encontram, aceita.
- `topo = pilha.pop()` — desempilha o símbolo que esperamos ver
  **agora**.
- `if topo == T_EOF` — só ocorre quando a pilha esvazia
  totalmente (o `$` foi atingido). Se o token corrente também é
  `$`, a entrada é aceita; senão sobraram tokens.
- `if topo not in nao_terminais` — **terminal no topo**:
  estratégia "casa-e-consome". Se casar, avança o cursor `i` da
  entrada; se não casar, é erro sintático com mensagem precisa.
- `chave = (topo, terminal_atual)` — **não-terminal no topo**:
  monta a chave de consulta da tabela LL(1).
- `if chave not in tabela` — célula vazia = erro sintático. A
  mensagem cita exatamente qual NT estava no topo e qual token
  encontrou — nosso melhor diagnóstico.
- `for sim in reversed(rhs): pilha.append(sim)` — **detalhe
  crítico**: empilhamos o RHS **de trás para frente**, para que
  o **primeiro** símbolo de α fique no topo. Isso é o que
  implementa a derivação **leftmost** (mais à esquerda).

O `reversed(rhs)` garante derivação **mais à esquerda** (leftmost):
o primeiro símbolo do RHS fica no topo da pilha e é processado primeiro.

### 9.2. Exemplo passo a passo

Para `(START) (3 4 +) (END)`:

| Passo | Pilha (topo →) | Token | Ação |
|:---:|---|---|---|
| 1 | `PROGRAM $` | `(` | Expande: `PROGRAM → "(" start ")" BODY` |
| 2 | `"(" start ")" BODY $` | `(` | Casa: `"("` |
| 3 | `start ")" BODY $` | `START` | Casa: `start` |
| 4 | `")" BODY $` | `)` | Casa: `")"` |
| 5 | `BODY $` | `(` | Expande: `BODY → "(" BODY_TAIL` |
| 6 | `"(" BODY_TAIL $` | `(` | Casa: `"("` |
| 7 | `BODY_TAIL $` | `3` | Expande: `BODY_TAIL → EXPR_BODY ")" BODY` |
| … | … | … | … |

O passo a passo completo da última execução está em
[`output/derivacao_ultima_execucao.md`](output/derivacao_ultima_execucao.md).

### 9.3. Da derivação para a AST

O `parsear()` apenas **valida** a entrada e produz a lista de passos
(`derivacao` + `passos`) usada para o relatório em
[output/derivacao_ultima_execucao.md](output/derivacao_ultima_execucao.md).

A **AST semântica** é construída separadamente por `gerarArvore()`,
que faz uma **descida recursiva** sobre o mesmo fluxo de tokens (ver funções
internas `parse_expr`/`parse_item`). Essa separação tem dois benefícios:

1. `parsear()` permanece puro: só verifica conformidade com a gramática
   LL(1) e produz um log auditoria. Ideal para mensagens de erro precisas.
2. `gerarArvore()` produz nós com **semântica** (`mem_read`, `mem_write`,
   `res_ref`, `if`, `ifelse`, `while`, `binary`) que o gerador de Assembly
   sabe traduzir diretamente — sem precisar conhecer a gramática concreta.

O pós-fixado da linguagem permite que essa segunda passada seja trivial
(no máximo 4 itens por expressão, decidido por lookahead de 1).

---

## 10. A Árvore Sintática (AST)

### 10.1. Tipos de nó

| Tipo | Campos | Representa |
|---|---|---|
| `program` | `stmts: [nó, …]` | raiz — lista de instruções do programa |
| `binary` | `op`, `esq`, `dir` | operação binária aritmética ou relacional |
| `number` | `valor` (string) | literal numérico (`"10"`, `"3.14"`) |
| `ident` | `valor` | identificador puro (operando sem parênteses, ex.: `(VARA 1 -)` → `ident(VARA)`) |
| `mem_read` | `nome` | leitura de memória: `(MEM)` |
| `mem_write` | `nome`, `valor` (sub-AST) | escrita em memória: `(V MEM)` — o campo `valor` contém a sub-AST que produz V |
| `res_ref` | `linhas_atras` (int) | referência a resultado anterior: `(N RES)` |
| `keyword` | `valor` (`"RES"`) | nó transitório para `RES` cru — normalmente convertido em `res_ref` por `gerarArvore` |
| `if` | `cond`, `then_block` | `(COND BLOCO IF)` |
| `ifelse` | `cond`, `then_block`, `else_block` | `(COND THEN ELSE IFELSE)` |
| `while` | `cond`, `body` | `(COND BLOCO WHILE)` |

> **Nota:** o nó `number.valor` é sempre **string** (preserva a grafia
> do lexema, ex.: `"7.5"` vs. `"7.50"`). A conversão para `double`
> acontece somente no gerador de Assembly.

**Como aplicamos no projeto** — `gerarArvore()` faz **descida recursiva**
sobre os tokens (mesma estratégia top-down, mas sem a tabela: 4 itens
por expressão é decidível por inspeção direta). Trecho real de
[`src/parser_ll1.py`](src/parser_ll1.py):

```python
def parse_expr() -> dict:
    esperar("(")
    itens = []
    while atual()["tipo"] != "RPAREN":
        itens.append(parse_item())
    esperar(")")

    if len(itens) == 1:                            # (MEM) → leitura
        return {"tipo": "mem_read", "nome": itens[0]["valor"]}

    if len(itens) == 2:                            # (V MEM) ou (N RES)
        primeiro, segundo = itens
        if segundo["tipo"] == "ident":
            return {"tipo": "mem_write",
                    "nome": segundo["valor"], "valor": primeiro}
        if segundo["tipo"] == "keyword" and segundo["valor"] == "RES":
            return {"tipo": "res_ref",
                    "linhas_atras": int(primeiro["valor"])}

    if len(itens) == 3:                            # (E1 E2 OP) ou (C B IF/WHILE)
        e1, e2, op = itens
        if op["tipo"] == "keyword" and op["valor"] == "IF":
            return {"tipo": "if", "cond": e1, "then_block": e2}
        if op["tipo"] == "keyword" and op["valor"] == "WHILE":
            return {"tipo": "while", "cond": e1, "body": e2}
        return {"tipo": "binary", "op": op["valor"], "esq": e1, "dir": e2}

    if len(itens) == 4:                            # (C T E IFELSE)
        return {"tipo": "ifelse", "cond": itens[0],
                "then_block": itens[1], "else_block": itens[2]}
```

**Lógica linha-a-linha:**
- `esperar("(")` ... `esperar(")")` — toda expressão é cercada
  por parênteses; consumimos os delimitadores e tratamos só o
  conteúdo.
- `while atual()["tipo"] != "RPAREN"` — coleta itens até o
  fechamento. Cada `parse_item()` lê 1 token simples (número,
  ident, keyword) **ou** chama `parse_expr()` recursivamente para
  uma sub-expressão.
- `len(itens) == 1` → **leitura de memória**: `(MEM)`. O único
  item tem que ser um identificador, e o nó produzido é `mem_read`.
- `len(itens) == 2` + segundo é `ident` → **escrita em memória**:
  `(V MEM)`. O **primeiro** item é a sub-AST que produz o valor;
  o **segundo** é o nome do destino.
- `len(itens) == 2` + segundo é `keyword RES` → **referência a
  resultado anterior**: `(N RES)`. `N` deve ser inteiro.
- `len(itens) == 3` — três variantes possíveis, decididas pelo
  **terceiro** item (que é sempre o "verbo" no pós-fixado):
  - `keyword IF` → comando `if` simples (sem else).
  - `keyword WHILE` → laço `while`.
  - operador → expressão `binary` (`+`, `-`, `*`, `<`, `==`, …).
- `len(itens) == 4` → única forma legal é `(C T E IFELSE)`.
  Cond, then-block e else-block são extraídos por posição.

Note como o **mesmo formato pós-fixado** que tornou a gramática
LL(1) (decidir produção por 1 lookahead) torna a construção da AST
trivial: a palavra-chave/operador no **fim** da expressão decide o
tipo do nó semântico.

### 10.2. Estrutura em JSON

```json
{
  "tipo": "program",
  "stmts": [
    { "tipo": "binary", "op": "+",
      "esq": { "tipo": "number", "valor": "10" },
      "dir": { "tipo": "number", "valor": "3" } },
    { "tipo": "while",
      "cond": { "tipo": "binary", "op": ">",
                "esq": { "tipo": "mem_read", "nome": "VARA" },
                "dir": { "tipo": "number", "valor": "0" } },
      "body": { "tipo": "binary", "op": "-",
                "esq": { "tipo": "mem_read", "nome": "VARA" },
                "dir": { "tipo": "number", "valor": "1" } } },
    { "tipo": "mem_write", "nome": "VARA",
      "valor": { "tipo": "number", "valor": "20" } }
  ]
}
```

O JSON completo da última execução está em
[`output/arvore_ultima_execucao.json`](output/arvore_ultima_execucao.json).

### 10.3. Árvore do último teste (`teste1.txt`)

```
program
  binary(+)
    number(10)
    number(3)
  binary(-)
    number(7.5)
    number(2.5)
  binary(*)
    number(4)
    number(2.5)
  binary(|)
    number(10.0)
    number(4.0)
  binary(/)
    number(10)
    number(3)
  binary(%)
    number(10)
    number(3)
  binary(^)
    number(2)
    number(5)
  mem_write(VARA)
    number(20)
  binary(|)
    mem_read(VARA)
    number(2)
  res_ref(linhas_atras=2)
  while
    cond:
      binary(>)
        mem_read(VARA)
        number(0)
    body:
      binary(-)
        mem_read(VARA)
        number(1)
  ifelse
    cond:
      binary(>=)
        mem_read(VARA)
        number(5)
    then:
      mem_write(FLAG)
        number(1)
    else:
      mem_write(FLAG)
        number(0)
  binary(==)
    mem_read(FLAG)
    number(0)
  binary(-)
    binary(+)
      number(10)
      number(3)
    binary(*)
      number(2)
      number(4)
```

---

## 11. Geração de Assembly

### 11.1. Estratégia geral

A geração percorre a AST **recursivamente**. Todos os valores são tratados como
`double` IEEE 754 (64 bits) usando os registradores VFP `d0`–`d7`.

Como o ARMv7 não tem `PUSH`/`POP` para registradores VFP diretamente,
usamos o par `r4:r5` como intermediário:

```asm
@ empilhar d0:
VMOV r4, r5, d0
PUSH {r4, r5}

@ desempilhar para d1:
POP {r4, r5}
VMOV d1, r4, r5
```

### 11.2. Como cada nó é traduzido

| Nó da AST | Assembly gerado |
|---|---|
| `number(N)` | `VLDR.F64 d0, =const_N` → empilha |
| `mem_read(MEM)` | `LDR r0, =mem_MEM` · `VLDR.F64 d0, [r0]` → empilha |
| `mem_write(MEM, e)` | gera `e` → desempilha → `VSTR.F64 d0, [mem_MEM]` |
| `res_ref(N)` | `LDR r0, =resultado_(linha-N)` · `VLDR.F64 d0, [r0]` |
| `binary(+)` | gera esq+dir → `VADD.F64 d0, d0, d1` |
| `binary(-)` | idem → `VSUB.F64 d0, d0, d1` |
| `binary(*)` | idem → `VMUL.F64 d0, d0, d1` |
| `binary(\|)` | idem → `VDIV.F64 d0, d0, d1` (divisão real) |
| `binary(/)` | idem → chama `__op_idiv` (divisão inteira) |
| `binary(%)` | idem → chama `__op_mod` |
| `binary(^)` | idem → chama `__op_pow` (multiplicação iterativa) |
| `binary(> < == …)` | `VCMP.F64 d0, d1` · `VMRS APSR_nzcv, FPSCR` · desvio condicional → empilha `1.0` ou `0.0` |
| `if` | gera cond → `VCMP` → `BEQ fim_X` → gera bloco → `fim_X:` |
| `ifelse` | gera cond → `BEQ else_X` → then → `B fim_X` → `else_X:` → else → `fim_X:` |
| `while` | `loop_X:` → gera cond → `BEQ fim_X` → bloco → `B loop_X` → `fim_X:` |

### 11.3. Estruturas de controle em detalhe

Esta seção mostra o ciclo completo de cada estrutura de controle: a **lógica**, o **código Python** em `_emit_*` e o **Assembly** resultante para um exemplo concreto.

---

#### IF — `(COND BLOCO IF)`

**Lógica:** avalia a condição; se ela for `0.0` (falso), salta o bloco inteiro e empilha `0.0` como resultado neutro.

```
┌─ avalia COND ──────────────────────────────────────┐
│  d0 = resultado da condição                        │
│  if d0 == 0.0  →  pula para [if_fim_0]             │
│  else          →  executa BLOCO, descarta resultado│
└────────────────────────────────────────────────────┘
[if_fim_0]:  empilha 0.0 (resultado padronizado)
```

**Código Python (`src/armv7_generator.py`):**

```python
def _emit_if(no, linhas, ctx):
    rotulo_fim = _novo_rotulo(ctx, "if_fim")      # ex: if_fim_0
    _emit_cond_valor(no["cond"], linhas, ctx)     # avalia condição → pilha
    _emit_pop_para_d(linhas, "d0")               # desempilha para d0
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")         # compara com 0.0
    linhas.append("    VMRS APSR_nzcv, FPSCR")  # flags ARM ← FPSCR
    linhas.append(f"    BEQ {rotulo_fim}")       # falso → pula bloco
    _emit_expressao(no["then_block"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")               # descarta resultado do bloco
    linhas.append(f"{rotulo_fim}:")
    linhas.append("    LDR r0, =const_zero")     # empilha 0.0 como resultado
    linhas.append("    VLDR.F64 d0, [r0]")
    _emit_push_d0(linhas)
```

**Assembly gerado para `(((VARA) 5 >=) (1 FLAG) IF)`:**

```asm
@ --- condição: (VARA) >= 5 ---
    LDR r0, =mem_vara
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha VARA
    LDR r0, =const_0        @ const_0: .double 5.0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha 5.0
    POP {r4, r5}
    VMOV d1, r4, r5          @ d1 = 5.0
    POP {r4, r5}
    VMOV d0, r4, r5          @ d0 = VARA
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BGE cmp_t_0
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]        @ falso → d0 = 0.0
    B cmp_e_0
cmp_t_0:
    LDR r0, =const_one
    VLDR.F64 d0, [r0]        @ verdadeiro → d0 = 1.0
cmp_e_0:
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha 1.0 ou 0.0
@ --- teste IF ---
    POP {r4, r5}
    VMOV d0, r4, r5          @ desempilha condição
    LDR r0, =const_zero
    VLDR.F64 d1, [r0]
    VCMP.F64 d0, d1          @ d0 == 0.0?
    VMRS APSR_nzcv, FPSCR
    BEQ if_fim_1             @ falso → pula bloco
@ --- bloco THEN: (1 FLAG) ---
    LDR r0, =const_1        @ const_1: .double 1.0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =mem_flag
    VSTR.F64 d0, [r0]        @ FLAG ← 1.0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5          @ descarta resultado do bloco
if_fim_1:
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]        @ resultado neutro = 0.0
    VMOV r4, r5, d0
    PUSH {r4, r5}
```

---

#### IFELSE — `(COND THEN ELSE IFELSE)`

**Lógica:** avalia condição; se falso, desvia para `else_block`; após o `then_block`, salta o `else_block`.

```
┌─ avalia COND ─────────────────────────────────────┐
│  if d0 == 0.0  →  pula para [else_0]              │
│  executa THEN  →  B [ife_fim_0]                   │
└───────────────────────────────────────────────────┘
[else_0]:  executa ELSE
[ife_fim_0]:  (valor do ramo escolhido já está na pilha)
```

**Código Python:**

```python
def _emit_ifelse(no, linhas, ctx):
    rotulo_else = _novo_rotulo(ctx, "else")       # ex: else_0
    rotulo_fim  = _novo_rotulo(ctx, "ife_fim")    # ex: ife_fim_0
    _emit_cond_valor(no["cond"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")
    linhas.append(f"    BEQ {rotulo_else}")       # falso → ELSE
    _emit_expressao(no["then_block"], linhas, ctx)
    linhas.append(f"    B {rotulo_fim}")          # pula ELSE
    linhas.append(f"{rotulo_else}:")
    _emit_expressao(no["else_block"], linhas, ctx)
    linhas.append(f"{rotulo_fim}:")              # valor do ramo já na pilha
```

**Assembly gerado para `(((VARA) 5 >=) (1 FLAG) (0 FLAG) IFELSE)`:**

```asm
@ --- condição: (VARA) >= 5 (idêntico ao IF acima) ---
    ... @ avalia VARA >= 5, empilha 1.0 ou 0.0
@ --- teste IFELSE ---
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =const_zero
    VLDR.F64 d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ else_2               @ falso → else
@ --- bloco THEN: (1 FLAG) ---
    ...                      @ FLAG ← 1.0, empilha 1.0
    B ife_fim_2              @ pula else
else_2:
@ --- bloco ELSE: (0 FLAG) ---
    ...                      @ FLAG ← 0.0, empilha 0.0
ife_fim_2:                   @ valor do ramo escolhido já está na pilha
```

---

#### WHILE — `(COND BLOCO WHILE)`

**Lógica:** reavalia a condição a cada iteração. O corpo deve ter **efeito colateral** (guardar em memória) para que a condição eventualmente vire falsa.

```
[while_i_0]:               ← início do loop
┌─ avalia COND ────────────────────────────────────┐
│  if d0 == 0.0  →  pula para [while_f_0]          │
│  executa CORPO, descarta resultado               │
│  B [while_i_0]           ← volta ao início       │
└──────────────────────────────────────────────────┘
[while_f_0]:  empilha 0.0 (resultado neutro)
```

> **Importante:** o corpo PRECISA escrever em memória para modificar o
> estado do programa. `((VARA) 1 -)` **sozinho** não basta — calcula o
> resultado mas o **descarta**. A forma correta é `(((VARA) 1 -) VARA)`,
> que armazena `VARA - 1` de volta em `VARA`.

**Código Python:**

```python
def _emit_while(no, linhas, ctx):
    rotulo_ini = _novo_rotulo(ctx, "while_i")     # ex: while_i_0
    rotulo_fim = _novo_rotulo(ctx, "while_f")     # ex: while_f_0
    linhas.append(f"{rotulo_ini}:")              # início do loop
    _emit_cond_valor(no["cond"], linhas, ctx)     # avalia condição → pilha
    _emit_pop_para_d(linhas, "d0")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")
    linhas.append(f"    BEQ {rotulo_fim}")        # falso → sai do loop
    _emit_expressao(no["body"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")               # descarta resultado do corpo
    linhas.append(f"    B {rotulo_ini}")          # volta ao início
    linhas.append(f"{rotulo_fim}:")
    linhas.append("    LDR r0, =const_zero")     # empilha 0.0 como resultado
    linhas.append("    VLDR.F64 d0, [r0]")
    _emit_push_d0(linhas)
```

**Assembly gerado para `(((VARA) 0 >) (((VARA) 1 -) VARA) WHILE)`:**

```asm
while_i_0:
@ --- condição: (VARA) > 0 ---
    LDR r0, =mem_vara
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha VARA
    LDR r0, =const_0        @ const_0: .double 0.0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha 0.0
    POP {r4, r5}
    VMOV d1, r4, r5          @ d1 = 0.0
    POP {r4, r5}
    VMOV d0, r4, r5          @ d0 = VARA
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BGT cmp_t_3
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]
    B cmp_e_3
cmp_t_3:
    LDR r0, =const_one
    VLDR.F64 d0, [r0]
cmp_e_3:
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha 1.0 (VARA > 0) ou 0.0
@ --- teste WHILE ---
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =const_zero
    VLDR.F64 d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ while_f_0            @ VARA <= 0 → sai
@ --- corpo: (((VARA) 1 -) VARA) → VARA ← VARA - 1 ---
    LDR r0, =mem_vara
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha VARA
    LDR r0, =const_1        @ const_1: .double 1.0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha 1.0
    POP {r4, r5}
    VMOV d1, r4, r5          @ d1 = 1.0
    POP {r4, r5}
    VMOV d0, r4, r5          @ d0 = VARA
    VSUB.F64 d0, d0, d1      @ d0 = VARA - 1
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ empilha resultado
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =mem_vara
    VSTR.F64 d0, [r0]        @ VARA ← VARA - 1  (efeito colateral!)
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5          @ descarta resultado do corpo
    B while_i_0              @ volta ao início
while_f_0:
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}            @ resultado neutro = 0.0
```

---

### 11.4. Rotinas auxiliares

As operações sem instrução nativa em ARMv7 são implementadas como sub-rotinas:

| Rotina | Função |
|---|---|
| `__op_idiv` | divisão inteira: converte `double→int`, divide, volta para `double` |
| `__op_mod` | resto: divide e subtrai `quociente × divisor` |
| `__op_pow` | potência com expoente inteiro (laço de multiplicações) |
| `__sdiv32` | divisão de 32 bits por subtrações (Cortex-A9 não tem `SDIV`) |
| `__exibir_hex` | exibe inteiro nos 6 displays HEX do DE1-SoC |

---

## 12. Arquivos de Teste
Para validar o tratamento de erros:

| Arquivo | Erros cobertos |
|---|---|
| [`teste_erro_lexico.txt`](teste_erro_lexico.txt) | `&`, `3.14.5`, `.5`, `10x`, `Mem` (minúscula), `=` sozinho, `!` sozinho, `MEM1` (dígito) |
| [`teste_erro_sintatico.txt`](teste_erro_sintatico.txt) | `(3 2 + 5)`, `(+ 3 2)`, `(IF 3 2)`, parênteses extras, `(1 RES MEM)` |

```bash
python main.py teste_erro_lexico.txt     # aborta na primeira linha problemática
python main.py teste_erro_sintatico.txt
```

Os testes unitários em [`tests/`](tests/) cobrem:

- Tokens léxicos inválidos (`@`, `&`, números malformados)
- Programas sem `(START)` ou sem `(END)`
- Estruturas de controle malformadas
- Aninhamento profundo e expressões vazias
- Pipeline completo com os 3 arquivos de teste

---

## 13. Tratamento de Erros

Toda mensagem inclui **linha** e **coluna** quando disponível:

| Origem | Exemplo de mensagem |
|---|---|
| Lexer | `linha 4, col 7: caractere inválido '@'` |
| Parser | `Erro sintático: não há produção para [REST2, if] (token 'IF' (linha 6, coluna 12))` |
| Parser | `Erro sintático: esperado ')' mas encontrado '+' (linha 3, coluna 4)` |
| Parser | `Entrada extra após o fim do programa: '(' (linha 8, coluna 1)` |
| Semântico | `Comando (N RES) exige N inteiro não negativo` |
| Semântico | `Comando (MEM) exige identificador em letras maiúsculas` |

A classe `Erros` (em [`src/lexer_fsm.py`](src/lexer_fsm.py)) é compartilhada por
todos os módulos, mantendo o `try/except` em `main.py` simples.

---

## 14. Distribuição do Trabalho

| Aluno | Responsabilidades | Arquivos |
|---|---|---|
| **Frederico** (fredfruet) | `construirGramatica`, FIRST/FOLLOW, tabela LL(1), `parsear` | [`src/parser_ll1.py`](src/parser_ll1.py), [`gramatica.md`](gramatica.md), [`tests/test_pipeline.py`](tests/test_pipeline.py) |
| **Emanuel** (emanuelriceto) | `lerTokens`, novas keywords e relacionais no AFD, testes léxicos | [`src/lexer_fsm.py`](src/lexer_fsm.py), [`src/pipeline.py`](src/pipeline.py), [`tests/test_lexer.py`](tests/test_lexer.py) |
| **Arthur** (Tuizones) | `gerarArvore`, `gerarAssembly`, `main`, integração end-to-end | [`main.py`](main.py), [`src/armv7_generator.py`](src/armv7_generator.py) |

Cada contribuição está registrada no repositório como **pull request separado**.


## 15. Referências

### Bibliografia

- AHO, A. V.; LAM, M. S.; SETHI, R.; ULLMAN, J. D. **Compiladores: princípios, técnicas e ferramentas**. 2ª ed. Pearson, 2008. *("Dragon Book" — capítulos sobre top-down parsing, FIRST/FOLLOW e tabela LL(1))*.
- HOPCROFT, J. E.; ULLMAN, J. D. **Introduction to Automata Theory, Languages, and Computation**. *(hierarquia de Chomsky e gramáticas livres de contexto)*.
- ARM Architecture Reference Manual — ARMv7-A and ARMv7-R edition.

### Material da disciplina

- ALCANTARA, F. C. **Aula 5 -Parsers LL1** — transparências da disciplina de Linguagens Formais e Compiladores, PUCPR. *(classificação de parsers, ambiguidade, derivação esquerda/direita, recursão à esquerda, fatoração à esquerda)*.
- ALCANTARA, F. C. **Aula 6 -Parsers LL1 Novo** — transparências da disciplina. *(algoritmos formais de FIRST e FOLLOW, construção da tabela `M[A, a]`, exemplos de traço de execução)*.

### Ferramentas e ambientes

- CPUlator DE1-SoC — <https://cpulator.01xz.net> *(simulador ARMv7 + periféricos do kit DE1-SoC)*.
- Python 3.10+ — <https://docs.python.org/3/>.
- pytest — <https://docs.pytest.org/>.
