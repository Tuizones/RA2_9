# Gramática LL(1), FIRST/FOLLOW e Tabela de Análise

> Documento escrito para a **Fase 2** do projeto da disciplina de
> **Linguagens Formais e Compiladores** — PUCPR (Prof. Frank Coelho de
> Alcantara). Grupo **RA2 9**.
>
> O dump dinâmico (atualizado a cada execução) com todos os conjuntos
> e a tabela completa é gerado automaticamente em `output/gramatica_dump.md`.

---

## 0. Algoritmo de Construção da Tabela de Análise LL(1)

A tabela de análise `M[A, a]` é construída a partir dos conjuntos
**FIRST** e **FOLLOW** seguindo o algoritmo do livro-texto:

**Para cada regra de produção A → α:**

| Passo | Condição | Ação |
|:---:|---|---|
| 1 | Para cada terminal **a** ∈ **FIRST(α)** | Adicione **A → α** em `M[A, a]` |
| 2 | Se **ε** ∈ **FIRST(α)** | Para cada terminal **b** ∈ **FOLLOW(A)**: adicione **A → α** em `M[A, b]` |
| 2a | Se **ε** ∈ **FIRST(α)** e **$** ∈ **FOLLOW(A)** | Adicione **A → α** em `M[A, $]` |
| 3 | Célula vazia | Erro sintático |
| 4 | Célula com **duas produções** distintas | Conflito LL(1) — gramática **não** é LL(1) |

> **Importante:** ε nunca entra como chave na tabela; é apenas o sinalizador
> de "propagar para FOLLOW".

### Como o algoritmo se relaciona com FIRST e FOLLOW

```
FIRST(α) tells the parser: "which terminals can START a string derived from α?"
FOLLOW(A) tells the parser: "which terminals can FOLLOW A in any sentential form?"

When FIRST(α) contains ε, A can "disappear", so whatever comes after A
(i.e. FOLLOW(A)) also guides the choice of A → α.
```

O código Python que implementa este algoritmo está em
`src/parser_ll1.py` → função `_construir_tabela_ll1()`.

---

## 1. Regras de Produção (EBNF)

Convenção: **minúsculas** = não-terminais, **MAIÚSCULAS** = terminais.
`ε` é a cadeia vazia. `$` é o marcador de fim de entrada.

```
(00) program    -> LPAREN START RPAREN body
(01) body       -> LPAREN body_tail
(02) body_tail  -> END RPAREN
(03) body_tail  -> expr_body RPAREN body
(04) expr_body  -> item rest1
(05) rest1      -> ε
(06) rest1      -> item rest2
(07) rest2      -> ε
(08) rest2      -> binop
(09) rest2      -> kw_ctrl3
(10) rest2      -> item item_tail
(11) item_tail  -> kw_ctrl4
(12) item       -> NUMERO
(13) item       -> IDENT
(14) item       -> RES
(15) item       -> LPAREN expr_body RPAREN
(16) binop      -> +
(17) binop      -> -
(18) binop      -> *
(19) binop      -> /        @ divisão inteira
(20) binop      -> |        @ divisão real
(21) binop      -> %
(22) binop      -> ^
(23) binop      -> >
(24) binop      -> <
(25) binop      -> ==
(26) binop      -> !=
(27) binop      -> >=
(28) binop      -> <=
(29) kw_ctrl3   -> IF
(30) kw_ctrl3   -> WHILE
(31) kw_ctrl4   -> IFELSE
```

### Observações sobre o desenho da gramática

1. **Fatoração à esquerda em `body`.** Sem ela, a produção
   `program → (START) stmt_list (END)` geraria um conflito LL(1) em
   `[stmt_list, LPAREN]`, já que tanto `stmt` quanto `(END)` começam com
   `LPAREN`. Consumimos o `LPAREN` antes e só então decidimos pelo
   terminal de *lookahead* (`END` vs. início de `expr_body`).
2. **`rest1` / `rest2` / `item_tail` são anuláveis somente quando
   necessário.** Isso garante que, no pior caso, a decisão use apenas
   um símbolo de *lookahead*.
3. **Comandos especiais** (`(V MEM)`, `(MEM)`, `(N RES)`) e
   **estruturas de controle** (`(COND BODY IF)`, `(COND BODY WHILE)`,
   `(COND THEN ELSE IFELSE)`) compartilham as mesmas regras estruturais —
   a distinção é feita semanticamente ao construir a árvore.

---

## 2. Conjuntos FIRST

```
FIRST(program)   = { LPAREN }
FIRST(body)      = { LPAREN }
FIRST(body_tail) = { END, IDENT, LPAREN, NUMERO, RES }
FIRST(expr_body) = { IDENT, LPAREN, NUMERO, RES }
FIRST(rest1)     = { IDENT, LPAREN, NUMERO, RES, ε }
FIRST(rest2)     = { !=, %, *, +, -, /, <, <=, ==, >, >=,
                     IDENT, IF, LPAREN, NUMERO, RES, WHILE, ^, |, ε }
FIRST(item_tail) = { IFELSE }
FIRST(item)      = { IDENT, LPAREN, NUMERO, RES }
FIRST(binop)     = { !=, %, *, +, -, /, <, <=, ==, >, >=, ^, | }
FIRST(kw_ctrl3)  = { IF, WHILE }
FIRST(kw_ctrl4)  = { IFELSE }
```

## 3. Conjuntos FOLLOW

```
FOLLOW(program)   = { $ }
FOLLOW(body)      = { $ }
FOLLOW(body_tail) = { $ }
FOLLOW(expr_body) = { RPAREN }
FOLLOW(rest1)     = { RPAREN }
FOLLOW(rest2)     = { RPAREN }
FOLLOW(item_tail) = { RPAREN }
FOLLOW(item)      = { !=, %, *, +, -, /, <, <=, ==, >, >=,
                      IDENT, IF, IFELSE, LPAREN, NUMERO, RES,
                      RPAREN, WHILE, ^, | }
FOLLOW(binop)     = { RPAREN }
FOLLOW(kw_ctrl3)  = { RPAREN }
FOLLOW(kw_ctrl4)  = { RPAREN }
```

---

## 4. Tabela de Análise LL(1)

Cada célula `M[A, a]` indica a produção a aplicar quando o topo da pilha é o
não-terminal **A** e o token corrente é o terminal **a**.
Células ausentes = **erro sintático**.
A gramática é **livre de conflitos** — nenhuma célula recebe duas produções.

### 4.1. Formato plano (M[A, a] → #produção)

| M[A, a] | Produção |
|---|---|
| M[program, LPAREN] | #0  program → LPAREN START RPAREN body |
| M[body, LPAREN] | #1  body → LPAREN body_tail |
| M[body_tail, END] | #2  body_tail → END RPAREN |
| M[body_tail, LPAREN / NUMERO / IDENT / RES] | #3  body_tail → expr_body RPAREN body |
| M[expr_body, LPAREN / NUMERO / IDENT / RES] | #4  expr_body → item rest1 |
| M[rest1, RPAREN] | #5  rest1 → ε |
| M[rest1, LPAREN / NUMERO / IDENT / RES] | #6  rest1 → item rest2 |
| M[rest2, RPAREN] | #7  rest2 → ε |
| M[rest2, +/-/\*/…(operadores)] | #8  rest2 → binop |
| M[rest2, IF / WHILE] | #9  rest2 → kw_ctrl3 |
| M[rest2, LPAREN / NUMERO / IDENT / RES] | #10 rest2 → item item_tail |
| M[item_tail, IFELSE] | #11 item_tail → kw_ctrl4 |
| M[item, NUMERO] | #12 item → NUMERO |
| M[item, IDENT]  | #13 item → IDENT |
| M[item, RES]    | #14 item → RES |
| M[item, LPAREN] | #15 item → LPAREN expr_body RPAREN |
| M[binop, +/-/\*/…] | #16–#28 um por operador |
| M[kw_ctrl3, IF] | #29 kw_ctrl3 → IF |
| M[kw_ctrl3, WHILE] | #30 kw_ctrl3 → WHILE |
| M[kw_ctrl4, IFELSE] | #31 kw_ctrl4 → IFELSE |

A tabela completa com todas as 57 entradas é gerada automaticamente em
[`output/gramatica_dump.md`](output/gramatica_dump.md) (seção 4 do dump).

---

### 4.2. Formato matricial 2D — M[A, a]

Número = índice da produção (ver seção 1). `—` = erro sintático.
Colunas divididas em dois grupos para caber na página.

**Grupo A — Tokens, palavras-chave e $**

| NT \ T | $ | END | IDENT | IF | IFELSE | LPAREN | NUMERO | RES | RPAREN | WHILE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `program`   | — | — | — | — | — | **#0** | — | — | — | — |
| `body`      | — | — | — | — | — | **#1** | — | — | — | — |
| `body_tail` | — | **#2** | **#3** | — | — | **#3** | **#3** | **#3** | — | — |
| `expr_body` | — | — | **#4** | — | — | **#4** | **#4** | **#4** | — | — |
| `rest1`     | — | — | **#6** | — | — | **#6** | **#6** | **#6** | **#5** | — |
| `rest2`     | — | — | **#10** | **#9** | — | **#10** | **#10** | **#10** | **#7** | **#9** |
| `item_tail` | — | — | — | — | **#11** | — | — | — | — | — |
| `item`      | — | — | **#13** | — | — | **#15** | **#12** | **#14** | — | — |
| `binop`     | — | — | — | — | — | — | — | — | — | — |
| `kw_ctrl3`  | — | — | — | **#29** | — | — | — | — | — | **#30** |
| `kw_ctrl4`  | — | — | — | — | **#31** | — | — | — | — | — |

**Grupo B — Operadores**

| NT \ T | != | % | \* | + | - | / | < | <= | == | > | >= | ^ | \| |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `rest2` | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** |
| `binop` | **#26** | **#21** | **#18** | **#16** | **#17** | **#19** | **#24** | **#28** | **#25** | **#23** | **#27** | **#22** | **#20** |

> Linhas com todas as células `—` são omitidas para brevidade.

---

### 4.3. Como ler a tabela (passo a passo do parser)

O parser mantém uma **pilha** e um **buffer de tokens**. A cada iteração:

```
Se topo da pilha == terminal:
    Se topo == token corrente  →  consome (avança no buffer)
    Caso contrário             →  ERRO SINTÁTICO

Se topo da pilha == não-terminal A, token corrente == a:
    Se M[A, a] existe          →  expande A com a produção M[A, a]
    Caso contrário             →  ERRO SINTÁTICO

Se topo == $ e token == $      →  ACEITA ✓
```

**Exemplo** para `(START) (3 4 +) (END)`:

| Pilha (topo →) | Token | Ação |
|---|---|---|
| `program $` | `(` | M[program, LPAREN] = #0 → expande |
| `LPAREN START RPAREN body $` | `(` | terminal: casa `(` |
| `START RPAREN body $` | `START` | terminal: casa `START` |
| `RPAREN body $` | `)` | terminal: casa `)` |
| `body $` | `(` | M[body, LPAREN] = #1 → expande |
| `LPAREN body_tail $` | `(` | terminal: casa `(` |
| `body_tail $` | `3` | M[body_tail, NUMERO] = #3 → expande |
| `expr_body RPAREN body $` | `3` | M[expr_body, NUMERO] = #4 → expande |
| … | … | … |

O passo a passo completo da última execução está em
[`output/derivacao_ultima_execucao.md`](output/derivacao_ultima_execucao.md).

---

## 5. Árvore Sintática do Último Teste (`teste1.txt`)

Gerada pelo comando `python main.py teste1.txt`, salva também em
[`output/arvore_ultima_execucao.txt`](output/arvore_ultima_execucao.txt)
e [`output/arvore_ultima_execucao.json`](output/arvore_ultima_execucao.json):

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
