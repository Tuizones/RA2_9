# Gramática LL(1)

## 0. Algoritmo de Construção da Tabela de Análise LL(1)

Para cada regra de produção **A → α** na gramática:

1. Para cada terminal **a** ∈ FIRST(α):
   - Adicione a produção **A → α** na célula **Tabela[A, a]**.
2. Se **ε** ∈ FIRST(α):
   - Para cada terminal **b** ∈ FOLLOW(A):
     - Adicione **A → α** na célula **Tabela[A, b]**.
     - Isso inclui **$** se ele estiver em FOLLOW(A).
3. Qualquer célula não preenchida = **erro sintático**.
4. Se alguma célula receber **duas ou mais produções** distintas
   = **conflito LL(1)** (a gramática **não** é LL(1)).

> Implementado em `_construir_tabela_ll1()` dentro de `src/parser_ll1.py`.
> O algoritmo itera até ponto-fixo para FIRST e FOLLOW antes de preencher a tabela.

## 1. Regras de Produção

| # | Não-Terminal | Produção |
|---|---|---|
| 0 | program | LPAREN START RPAREN body |
| 1 | body | LPAREN body_tail |
| 2 | body_tail | END RPAREN |
| 3 | body_tail | expr_body RPAREN body |
| 4 | expr_body | item rest1 |
| 5 | rest1 | ε |
| 6 | rest1 | item rest2 |
| 7 | rest2 | ε |
| 8 | rest2 | binop |
| 9 | rest2 | kw_ctrl3 |
| 10 | rest2 | item item_tail |
| 11 | item_tail | kw_ctrl4 |
| 12 | item | NUMERO |
| 13 | item | IDENT |
| 14 | item | RES |
| 15 | item | LPAREN expr_body RPAREN |
| 16 | binop | + |
| 17 | binop | - |
| 18 | binop | * |
| 19 | binop | / |
| 20 | binop | | |
| 21 | binop | % |
| 22 | binop | ^ |
| 23 | binop | > |
| 24 | binop | < |
| 25 | binop | == |
| 26 | binop | != |
| 27 | binop | >= |
| 28 | binop | <= |
| 29 | kw_ctrl3 | IF |
| 30 | kw_ctrl3 | WHILE |
| 31 | kw_ctrl4 | IFELSE |

## 2. Conjuntos FIRST

FIRST(A) = conjunto de terminais que podem **iniciar** uma derivação de A.
Se A pode derivar ε, então ε ∈ FIRST(A).

| Não-Terminal | FIRST |
|---|---|
| binop | { !=, %, *, +, -, /, <, <=, ==, >, >=, ^, | } |
| body | { LPAREN } |
| body_tail | { END, IDENT, LPAREN, NUMERO, RES } |
| expr_body | { IDENT, LPAREN, NUMERO, RES } |
| item | { IDENT, LPAREN, NUMERO, RES } |
| item_tail | { IFELSE } |
| kw_ctrl3 | { IF, WHILE } |
| kw_ctrl4 | { IFELSE } |
| program | { LPAREN } |
| rest1 | { IDENT, LPAREN, NUMERO, RES, ε } |
| rest2 | { !=, %, *, +, -, /, <, <=, ==, >, >=, IDENT, IF, LPAREN, NUMERO, RES, WHILE, ^, |, ε } |

## 3. Conjuntos FOLLOW

FOLLOW(A) = terminais que podem aparecer **imediatamente após** A.
$ ∈ FOLLOW(símbolo inicial) sempre. ε nunca pertence a FOLLOW.

| Não-Terminal | FOLLOW |
|---|---|
| binop | { RPAREN } |
| body | { $ } |
| body_tail | { $ } |
| expr_body | { RPAREN } |
| item | { !=, %, *, +, -, /, <, <=, ==, >, >=, IDENT, IF, IFELSE, LPAREN, NUMERO, RES, RPAREN, WHILE, ^, | } |
| item_tail | { RPAREN } |
| kw_ctrl3 | { RPAREN } |
| kw_ctrl4 | { RPAREN } |
| program | { $ } |
| rest1 | { RPAREN } |
| rest2 | { RPAREN } |

## 4. Tabela de Análise LL(1) — Formato Plano

Cada entrada M[A, a] lista a produção a aplicar.
Entradas ausentes = erro sintático.

| Não-Terminal (A) | Terminal (a) | Produção |
|---|---|---|
| binop | != | #26: binop → != |
| binop | % | #21: binop → % |
| binop | * | #18: binop → * |
| binop | + | #16: binop → + |
| binop | - | #17: binop → - |
| binop | / | #19: binop → / |
| binop | < | #24: binop → < |
| binop | <= | #28: binop → <= |
| binop | == | #25: binop → == |
| binop | > | #23: binop → > |
| binop | >= | #27: binop → >= |
| binop | ^ | #22: binop → ^ |
| binop | | | #20: binop → | |
| body | LPAREN | #1: body → LPAREN body_tail |
| body_tail | END | #2: body_tail → END RPAREN |
| body_tail | IDENT | #3: body_tail → expr_body RPAREN body |
| body_tail | LPAREN | #3: body_tail → expr_body RPAREN body |
| body_tail | NUMERO | #3: body_tail → expr_body RPAREN body |
| body_tail | RES | #3: body_tail → expr_body RPAREN body |
| expr_body | IDENT | #4: expr_body → item rest1 |
| expr_body | LPAREN | #4: expr_body → item rest1 |
| expr_body | NUMERO | #4: expr_body → item rest1 |
| expr_body | RES | #4: expr_body → item rest1 |
| item | IDENT | #13: item → IDENT |
| item | LPAREN | #15: item → LPAREN expr_body RPAREN |
| item | NUMERO | #12: item → NUMERO |
| item | RES | #14: item → RES |
| item_tail | IFELSE | #11: item_tail → kw_ctrl4 |
| kw_ctrl3 | IF | #29: kw_ctrl3 → IF |
| kw_ctrl3 | WHILE | #30: kw_ctrl3 → WHILE |
| kw_ctrl4 | IFELSE | #31: kw_ctrl4 → IFELSE |
| program | LPAREN | #0: program → LPAREN START RPAREN body |
| rest1 | IDENT | #6: rest1 → item rest2 |
| rest1 | LPAREN | #6: rest1 → item rest2 |
| rest1 | NUMERO | #6: rest1 → item rest2 |
| rest1 | RES | #6: rest1 → item rest2 |
| rest1 | RPAREN | #5: rest1 → ε |
| rest2 | != | #8: rest2 → binop |
| rest2 | % | #8: rest2 → binop |
| rest2 | * | #8: rest2 → binop |
| rest2 | + | #8: rest2 → binop |
| rest2 | - | #8: rest2 → binop |
| rest2 | / | #8: rest2 → binop |
| rest2 | < | #8: rest2 → binop |
| rest2 | <= | #8: rest2 → binop |
| rest2 | == | #8: rest2 → binop |
| rest2 | > | #8: rest2 → binop |
| rest2 | >= | #8: rest2 → binop |
| rest2 | IDENT | #10: rest2 → item item_tail |
| rest2 | IF | #9: rest2 → kw_ctrl3 |
| rest2 | LPAREN | #10: rest2 → item item_tail |
| rest2 | NUMERO | #10: rest2 → item item_tail |
| rest2 | RES | #10: rest2 → item item_tail |
| rest2 | RPAREN | #7: rest2 → ε |
| rest2 | WHILE | #9: rest2 → kw_ctrl3 |
| rest2 | ^ | #8: rest2 → binop |
| rest2 | | | #8: rest2 → binop |

## 5. Tabela de Análise LL(1) — Formato Matricial M[A, a]

Número na célula = índice da produção (seção 1). `—` = erro sintático.

### Grupo A — Tokens, palavras-chave e $

| NT \ T | END | IDENT | IF | IFELSE | LPAREN | NUMERO | RES | RPAREN | WHILE |
|---|---|---|---|---|---|---|---|---|---|
| `program` | — | — | — | — | **#0** | — | — | — | — |
| `body` | — | — | — | — | **#1** | — | — | — | — |
| `body_tail` | **#2** | **#3** | — | — | **#3** | **#3** | **#3** | — | — |
| `expr_body` | — | **#4** | — | — | **#4** | **#4** | **#4** | — | — |
| `rest1` | — | **#6** | — | — | **#6** | **#6** | **#6** | **#5** | — |
| `rest2` | — | **#10** | **#9** | — | **#10** | **#10** | **#10** | **#7** | **#9** |
| `item_tail` | — | — | — | **#11** | — | — | — | — | — |
| `item` | — | **#13** | — | — | **#15** | **#12** | **#14** | — | — |
| `kw_ctrl3` | — | — | **#29** | — | — | — | — | — | **#30** |
| `kw_ctrl4` | — | — | — | **#31** | — | — | — | — | — |

### Grupo B — Operadores

| NT \ T | != | % | * | + | - | / | < | <= | == | > | >= | ^ | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `rest2` | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** | **#8** |
| `binop` | **#26** | **#21** | **#18** | **#16** | **#17** | **#19** | **#24** | **#28** | **#25** | **#23** | **#27** | **#22** | **#20** |

