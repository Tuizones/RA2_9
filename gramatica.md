# Gramática LL(1), FIRST/FOLLOW e Tabela de Análise

> Documento gerado para a **Fase 2** do projeto da disciplina de
> **Linguagens Formais e Compiladores** — PUCPR (Prof. Frank Coelho de
> Alcantara). Grupo **RA2 9**.
>
> Todos os dados abaixo podem ser reproduzidos executando:
>
> ```
> python scripts/dump_gramatica.py
> ```

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

Cada célula `M[não-terminal, terminal]` traz o número da produção a
aplicar. Células ausentes indicam erro sintático. A tabela é **livre de
conflitos** — a gramática é LL(1).

| M[A, a] | Produção |
|---|---|
| M[program, LPAREN] | #0 program → LPAREN START RPAREN body |
| M[body, LPAREN] | #1 body → LPAREN body_tail |
| M[body_tail, END] | #2 body_tail → END RPAREN |
| M[body_tail, LPAREN] | #3 body_tail → expr_body RPAREN body |
| M[body_tail, NUMERO] | #3 body_tail → expr_body RPAREN body |
| M[body_tail, IDENT]  | #3 body_tail → expr_body RPAREN body |
| M[body_tail, RES]    | #3 body_tail → expr_body RPAREN body |
| M[expr_body, NUMERO] | #4 expr_body → item rest1 |
| M[expr_body, IDENT]  | #4 expr_body → item rest1 |
| M[expr_body, RES]    | #4 expr_body → item rest1 |
| M[expr_body, LPAREN] | #4 expr_body → item rest1 |
| M[rest1, RPAREN] | #5 rest1 → ε |
| M[rest1, NUMERO] / IDENT / RES / LPAREN | #6 rest1 → item rest2 |
| M[rest2, RPAREN] | #7 rest2 → ε |
| M[rest2, +, -, *, /, \|, %, ^, >, <, ==, !=, >=, <=] | #8 rest2 → binop |
| M[rest2, IF] / WHILE | #9 rest2 → kw_ctrl3 |
| M[rest2, NUMERO] / IDENT / RES / LPAREN | #10 rest2 → item item_tail |
| M[item_tail, IFELSE] | #11 item_tail → kw_ctrl4 |
| M[item, NUMERO] | #12 item → NUMERO |
| M[item, IDENT]  | #13 item → IDENT |
| M[item, RES]    | #14 item → RES |
| M[item, LPAREN] | #15 item → LPAREN expr_body RPAREN |
| M[binop, +] / − / * / / / \| / % / ^ | #16–#22 |
| M[binop, >] / < / == / != / >= / <= | #23–#28 |
| M[kw_ctrl3, IF] | #29 |
| M[kw_ctrl3, WHILE] | #30 |
| M[kw_ctrl4, IFELSE] | #31 |

A tabela completa e literal (todas as 57 entradas) pode ser regenerada com
`python scripts/dump_gramatica.py`.

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
