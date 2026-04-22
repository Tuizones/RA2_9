# Gramática LL(1)

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

## 4. Tabela de Análise LL(1)

| Não-Terminal | Terminal | Produção |
|---|---|---|
| binop | != | binop → != |
| binop | % | binop → % |
| binop | * | binop → * |
| binop | + | binop → + |
| binop | - | binop → - |
| binop | / | binop → / |
| binop | < | binop → < |
| binop | <= | binop → <= |
| binop | == | binop → == |
| binop | > | binop → > |
| binop | >= | binop → >= |
| binop | ^ | binop → ^ |
| binop | | | binop → | |
| body | LPAREN | body → LPAREN body_tail |
| body_tail | END | body_tail → END RPAREN |
| body_tail | IDENT | body_tail → expr_body RPAREN body |
| body_tail | LPAREN | body_tail → expr_body RPAREN body |
| body_tail | NUMERO | body_tail → expr_body RPAREN body |
| body_tail | RES | body_tail → expr_body RPAREN body |
| expr_body | IDENT | expr_body → item rest1 |
| expr_body | LPAREN | expr_body → item rest1 |
| expr_body | NUMERO | expr_body → item rest1 |
| expr_body | RES | expr_body → item rest1 |
| item | IDENT | item → IDENT |
| item | LPAREN | item → LPAREN expr_body RPAREN |
| item | NUMERO | item → NUMERO |
| item | RES | item → RES |
| item_tail | IFELSE | item_tail → kw_ctrl4 |
| kw_ctrl3 | IF | kw_ctrl3 → IF |
| kw_ctrl3 | WHILE | kw_ctrl3 → WHILE |
| kw_ctrl4 | IFELSE | kw_ctrl4 → IFELSE |
| program | LPAREN | program → LPAREN START RPAREN body |
| rest1 | IDENT | rest1 → item rest2 |
| rest1 | LPAREN | rest1 → item rest2 |
| rest1 | NUMERO | rest1 → item rest2 |
| rest1 | RES | rest1 → item rest2 |
| rest1 | RPAREN | rest1 → ε |
| rest2 | != | rest2 → binop |
| rest2 | % | rest2 → binop |
| rest2 | * | rest2 → binop |
| rest2 | + | rest2 → binop |
| rest2 | - | rest2 → binop |
| rest2 | / | rest2 → binop |
| rest2 | < | rest2 → binop |
| rest2 | <= | rest2 → binop |
| rest2 | == | rest2 → binop |
| rest2 | > | rest2 → binop |
| rest2 | >= | rest2 → binop |
| rest2 | IDENT | rest2 → item item_tail |
| rest2 | IF | rest2 → kw_ctrl3 |
| rest2 | LPAREN | rest2 → item item_tail |
| rest2 | NUMERO | rest2 → item item_tail |
| rest2 | RES | rest2 → item item_tail |
| rest2 | RPAREN | rest2 → ε |
| rest2 | WHILE | rest2 → kw_ctrl3 |
| rest2 | ^ | rest2 → binop |
| rest2 | | | rest2 → binop |
