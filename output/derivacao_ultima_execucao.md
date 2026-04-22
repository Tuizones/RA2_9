# Derivação LL(1) — Passo a Passo

| Passo | Pilha (topo →) | Entrada (→) | Ação |
|------:|---|---|---|
| 1 | `program $` | `( START ) ( 10 3 + ) ( 7.5 …` | Expande: `program` → `LPAREN START RPAREN body` |
| 2 | `LPAREN START RPAREN body $` | `( START ) ( 10 3 + ) ( 7.5 …` | Casa: `LPAREN` |
| 3 | `START RPAREN body $` | `START ) ( 10 3 + ) ( 7.5 2.5 …` | Casa: `START` |
| 4 | `RPAREN body $` | `) ( 10 3 + ) ( 7.5 2.5 - …` | Casa: `RPAREN` |
| 5 | `body $` | `( 10 3 + ) ( 7.5 2.5 - ) …` | Expande: `body` → `LPAREN body_tail` |
| 6 | `LPAREN body_tail $` | `( 10 3 + ) ( 7.5 2.5 - ) …` | Casa: `LPAREN` |
| 7 | `body_tail $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 8 | `expr_body RPAREN body $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `expr_body` → `item rest1` |
| 9 | `item rest1 RPAREN body $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `item` → `NUMERO` |
| 10 | `NUMERO rest1 RPAREN body $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Casa: `NUMERO` |
| 11 | `rest1 RPAREN body $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Expande: `rest1` → `item rest2` |
| 12 | `item rest2 RPAREN body $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Expande: `item` → `NUMERO` |
| 13 | `NUMERO rest2 RPAREN body $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Casa: `NUMERO` |
| 14 | `rest2 RPAREN body $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Expande: `rest2` → `binop` |
| 15 | `binop RPAREN body $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Expande: `binop` → `+` |
| 16 | `+ RPAREN body $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Casa: `+` |
| 17 | `RPAREN body $` | `) ( 7.5 2.5 - ) ( 4 2.5 * …` | Casa: `RPAREN` |
| 18 | `body $` | `( 7.5 2.5 - ) ( 4 2.5 * ) …` | Expande: `body` → `LPAREN body_tail` |
| 19 | `LPAREN body_tail $` | `( 7.5 2.5 - ) ( 4 2.5 * ) …` | Casa: `LPAREN` |
| 20 | `body_tail $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 21 | `expr_body RPAREN body $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `expr_body` → `item rest1` |
| 22 | `item rest1 RPAREN body $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `item` → `NUMERO` |
| 23 | `NUMERO rest1 RPAREN body $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Casa: `NUMERO` |
| 24 | `rest1 RPAREN body $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Expande: `rest1` → `item rest2` |
| 25 | `item rest2 RPAREN body $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Expande: `item` → `NUMERO` |
| 26 | `NUMERO rest2 RPAREN body $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Casa: `NUMERO` |
| 27 | `rest2 RPAREN body $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Expande: `rest2` → `binop` |
| 28 | `binop RPAREN body $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Expande: `binop` → `-` |
| 29 | `- RPAREN body $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Casa: `-` |
| 30 | `RPAREN body $` | `) ( 4 2.5 * ) ( 10.0 4.0 | …` | Casa: `RPAREN` |
| 31 | `body $` | `( 4 2.5 * ) ( 10.0 4.0 | ) …` | Expande: `body` → `LPAREN body_tail` |
| 32 | `LPAREN body_tail $` | `( 4 2.5 * ) ( 10.0 4.0 | ) …` | Casa: `LPAREN` |
| 33 | `body_tail $` | `4 2.5 * ) ( 10.0 4.0 | ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 34 | `expr_body RPAREN body $` | `4 2.5 * ) ( 10.0 4.0 | ) ( …` | Expande: `expr_body` → `item rest1` |
| 35 | `item rest1 RPAREN body $` | `4 2.5 * ) ( 10.0 4.0 | ) ( …` | Expande: `item` → `NUMERO` |
| 36 | `NUMERO rest1 RPAREN body $` | `4 2.5 * ) ( 10.0 4.0 | ) ( …` | Casa: `NUMERO` |
| 37 | `rest1 RPAREN body $` | `2.5 * ) ( 10.0 4.0 | ) ( 10 …` | Expande: `rest1` → `item rest2` |
| 38 | `item rest2 RPAREN body $` | `2.5 * ) ( 10.0 4.0 | ) ( 10 …` | Expande: `item` → `NUMERO` |
| 39 | `NUMERO rest2 RPAREN body $` | `2.5 * ) ( 10.0 4.0 | ) ( 10 …` | Casa: `NUMERO` |
| 40 | `rest2 RPAREN body $` | `* ) ( 10.0 4.0 | ) ( 10 3 …` | Expande: `rest2` → `binop` |
| 41 | `binop RPAREN body $` | `* ) ( 10.0 4.0 | ) ( 10 3 …` | Expande: `binop` → `*` |
| 42 | `* RPAREN body $` | `* ) ( 10.0 4.0 | ) ( 10 3 …` | Casa: `*` |
| 43 | `RPAREN body $` | `) ( 10.0 4.0 | ) ( 10 3 / …` | Casa: `RPAREN` |
| 44 | `body $` | `( 10.0 4.0 | ) ( 10 3 / ) …` | Expande: `body` → `LPAREN body_tail` |
| 45 | `LPAREN body_tail $` | `( 10.0 4.0 | ) ( 10 3 / ) …` | Casa: `LPAREN` |
| 46 | `body_tail $` | `10.0 4.0 | ) ( 10 3 / ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 47 | `expr_body RPAREN body $` | `10.0 4.0 | ) ( 10 3 / ) ( …` | Expande: `expr_body` → `item rest1` |
| 48 | `item rest1 RPAREN body $` | `10.0 4.0 | ) ( 10 3 / ) ( …` | Expande: `item` → `NUMERO` |
| 49 | `NUMERO rest1 RPAREN body $` | `10.0 4.0 | ) ( 10 3 / ) ( …` | Casa: `NUMERO` |
| 50 | `rest1 RPAREN body $` | `4.0 | ) ( 10 3 / ) ( 10 …` | Expande: `rest1` → `item rest2` |
| 51 | `item rest2 RPAREN body $` | `4.0 | ) ( 10 3 / ) ( 10 …` | Expande: `item` → `NUMERO` |
| 52 | `NUMERO rest2 RPAREN body $` | `4.0 | ) ( 10 3 / ) ( 10 …` | Casa: `NUMERO` |
| 53 | `rest2 RPAREN body $` | `| ) ( 10 3 / ) ( 10 3 …` | Expande: `rest2` → `binop` |
| 54 | `binop RPAREN body $` | `| ) ( 10 3 / ) ( 10 3 …` | Expande: `binop` → `|` |
| 55 | `| RPAREN body $` | `| ) ( 10 3 / ) ( 10 3 …` | Casa: `|` |
| 56 | `RPAREN body $` | `) ( 10 3 / ) ( 10 3 % …` | Casa: `RPAREN` |
| 57 | `body $` | `( 10 3 / ) ( 10 3 % ) …` | Expande: `body` → `LPAREN body_tail` |
| 58 | `LPAREN body_tail $` | `( 10 3 / ) ( 10 3 % ) …` | Casa: `LPAREN` |
| 59 | `body_tail $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 60 | `expr_body RPAREN body $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `expr_body` → `item rest1` |
| 61 | `item rest1 RPAREN body $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `item` → `NUMERO` |
| 62 | `NUMERO rest1 RPAREN body $` | `10 3 / ) ( 10 3 % ) ( …` | Casa: `NUMERO` |
| 63 | `rest1 RPAREN body $` | `3 / ) ( 10 3 % ) ( 2 …` | Expande: `rest1` → `item rest2` |
| 64 | `item rest2 RPAREN body $` | `3 / ) ( 10 3 % ) ( 2 …` | Expande: `item` → `NUMERO` |
| 65 | `NUMERO rest2 RPAREN body $` | `3 / ) ( 10 3 % ) ( 2 …` | Casa: `NUMERO` |
| 66 | `rest2 RPAREN body $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `rest2` → `binop` |
| 67 | `binop RPAREN body $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `binop` → `/` |
| 68 | `/ RPAREN body $` | `/ ) ( 10 3 % ) ( 2 5 …` | Casa: `/` |
| 69 | `RPAREN body $` | `) ( 10 3 % ) ( 2 5 ^ …` | Casa: `RPAREN` |
| 70 | `body $` | `( 10 3 % ) ( 2 5 ^ ) …` | Expande: `body` → `LPAREN body_tail` |
| 71 | `LPAREN body_tail $` | `( 10 3 % ) ( 2 5 ^ ) …` | Casa: `LPAREN` |
| 72 | `body_tail $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 73 | `expr_body RPAREN body $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `expr_body` → `item rest1` |
| 74 | `item rest1 RPAREN body $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `item` → `NUMERO` |
| 75 | `NUMERO rest1 RPAREN body $` | `10 3 % ) ( 2 5 ^ ) ( …` | Casa: `NUMERO` |
| 76 | `rest1 RPAREN body $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Expande: `rest1` → `item rest2` |
| 77 | `item rest2 RPAREN body $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Expande: `item` → `NUMERO` |
| 78 | `NUMERO rest2 RPAREN body $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Casa: `NUMERO` |
| 79 | `rest2 RPAREN body $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Expande: `rest2` → `binop` |
| 80 | `binop RPAREN body $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Expande: `binop` → `%` |
| 81 | `% RPAREN body $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Casa: `%` |
| 82 | `RPAREN body $` | `) ( 2 5 ^ ) ( 20 VARA ) …` | Casa: `RPAREN` |
| 83 | `body $` | `( 2 5 ^ ) ( 20 VARA ) ( …` | Expande: `body` → `LPAREN body_tail` |
| 84 | `LPAREN body_tail $` | `( 2 5 ^ ) ( 20 VARA ) ( …` | Casa: `LPAREN` |
| 85 | `body_tail $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 86 | `expr_body RPAREN body $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `expr_body` → `item rest1` |
| 87 | `item rest1 RPAREN body $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `item` → `NUMERO` |
| 88 | `NUMERO rest1 RPAREN body $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Casa: `NUMERO` |
| 89 | `rest1 RPAREN body $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Expande: `rest1` → `item rest2` |
| 90 | `item rest2 RPAREN body $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Expande: `item` → `NUMERO` |
| 91 | `NUMERO rest2 RPAREN body $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Casa: `NUMERO` |
| 92 | `rest2 RPAREN body $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Expande: `rest2` → `binop` |
| 93 | `binop RPAREN body $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Expande: `binop` → `^` |
| 94 | `^ RPAREN body $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Casa: `^` |
| 95 | `RPAREN body $` | `) ( 20 VARA ) ( ( VARA ) 2 …` | Casa: `RPAREN` |
| 96 | `body $` | `( 20 VARA ) ( ( VARA ) 2 | …` | Expande: `body` → `LPAREN body_tail` |
| 97 | `LPAREN body_tail $` | `( 20 VARA ) ( ( VARA ) 2 | …` | Casa: `LPAREN` |
| 98 | `body_tail $` | `20 VARA ) ( ( VARA ) 2 | ) …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 99 | `expr_body RPAREN body $` | `20 VARA ) ( ( VARA ) 2 | ) …` | Expande: `expr_body` → `item rest1` |
| 100 | `item rest1 RPAREN body $` | `20 VARA ) ( ( VARA ) 2 | ) …` | Expande: `item` → `NUMERO` |
| 101 | `NUMERO rest1 RPAREN body $` | `20 VARA ) ( ( VARA ) 2 | ) …` | Casa: `NUMERO` |
| 102 | `rest1 RPAREN body $` | `VARA ) ( ( VARA ) 2 | ) ( …` | Expande: `rest1` → `item rest2` |
| 103 | `item rest2 RPAREN body $` | `VARA ) ( ( VARA ) 2 | ) ( …` | Expande: `item` → `IDENT` |
| 104 | `IDENT rest2 RPAREN body $` | `VARA ) ( ( VARA ) 2 | ) ( …` | Casa: `IDENT` |
| 105 | `rest2 RPAREN body $` | `) ( ( VARA ) 2 | ) ( 2 …` | Expande: `rest2` → `ε` |
| 106 | `RPAREN body $` | `) ( ( VARA ) 2 | ) ( 2 …` | Casa: `RPAREN` |
| 107 | `body $` | `( ( VARA ) 2 | ) ( 2 RES …` | Expande: `body` → `LPAREN body_tail` |
| 108 | `LPAREN body_tail $` | `( ( VARA ) 2 | ) ( 2 RES …` | Casa: `LPAREN` |
| 109 | `body_tail $` | `( VARA ) 2 | ) ( 2 RES ) …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 110 | `expr_body RPAREN body $` | `( VARA ) 2 | ) ( 2 RES ) …` | Expande: `expr_body` → `item rest1` |
| 111 | `item rest1 RPAREN body $` | `( VARA ) 2 | ) ( 2 RES ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 112 | `LPAREN expr_body RPAREN rest1 RPAREN body $` | `( VARA ) 2 | ) ( 2 RES ) …` | Casa: `LPAREN` |
| 113 | `expr_body RPAREN rest1 RPAREN body $` | `VARA ) 2 | ) ( 2 RES ) ( …` | Expande: `expr_body` → `item rest1` |
| 114 | `item rest1 RPAREN rest1 RPAREN body $` | `VARA ) 2 | ) ( 2 RES ) ( …` | Expande: `item` → `IDENT` |
| 115 | `IDENT rest1 RPAREN rest1 RPAREN body $` | `VARA ) 2 | ) ( 2 RES ) ( …` | Casa: `IDENT` |
| 116 | `rest1 RPAREN rest1 RPAREN body $` | `) 2 | ) ( 2 RES ) ( ( …` | Expande: `rest1` → `ε` |
| 117 | `RPAREN rest1 RPAREN body $` | `) 2 | ) ( 2 RES ) ( ( …` | Casa: `RPAREN` |
| 118 | `rest1 RPAREN body $` | `2 | ) ( 2 RES ) ( ( ( …` | Expande: `rest1` → `item rest2` |
| 119 | `item rest2 RPAREN body $` | `2 | ) ( 2 RES ) ( ( ( …` | Expande: `item` → `NUMERO` |
| 120 | `NUMERO rest2 RPAREN body $` | `2 | ) ( 2 RES ) ( ( ( …` | Casa: `NUMERO` |
| 121 | `rest2 RPAREN body $` | `| ) ( 2 RES ) ( ( ( VARA …` | Expande: `rest2` → `binop` |
| 122 | `binop RPAREN body $` | `| ) ( 2 RES ) ( ( ( VARA …` | Expande: `binop` → `|` |
| 123 | `| RPAREN body $` | `| ) ( 2 RES ) ( ( ( VARA …` | Casa: `|` |
| 124 | `RPAREN body $` | `) ( 2 RES ) ( ( ( VARA ) …` | Casa: `RPAREN` |
| 125 | `body $` | `( 2 RES ) ( ( ( VARA ) 0 …` | Expande: `body` → `LPAREN body_tail` |
| 126 | `LPAREN body_tail $` | `( 2 RES ) ( ( ( VARA ) 0 …` | Casa: `LPAREN` |
| 127 | `body_tail $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 128 | `expr_body RPAREN body $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `expr_body` → `item rest1` |
| 129 | `item rest1 RPAREN body $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `item` → `NUMERO` |
| 130 | `NUMERO rest1 RPAREN body $` | `2 RES ) ( ( ( VARA ) 0 > …` | Casa: `NUMERO` |
| 131 | `rest1 RPAREN body $` | `RES ) ( ( ( VARA ) 0 > ) …` | Expande: `rest1` → `item rest2` |
| 132 | `item rest2 RPAREN body $` | `RES ) ( ( ( VARA ) 0 > ) …` | Expande: `item` → `RES` |
| 133 | `RES rest2 RPAREN body $` | `RES ) ( ( ( VARA ) 0 > ) …` | Casa: `RES` |
| 134 | `rest2 RPAREN body $` | `) ( ( ( VARA ) 0 > ) ( …` | Expande: `rest2` → `ε` |
| 135 | `RPAREN body $` | `) ( ( ( VARA ) 0 > ) ( …` | Casa: `RPAREN` |
| 136 | `body $` | `( ( ( VARA ) 0 > ) ( ( …` | Expande: `body` → `LPAREN body_tail` |
| 137 | `LPAREN body_tail $` | `( ( ( VARA ) 0 > ) ( ( …` | Casa: `LPAREN` |
| 138 | `body_tail $` | `( ( VARA ) 0 > ) ( ( VARA …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 139 | `expr_body RPAREN body $` | `( ( VARA ) 0 > ) ( ( VARA …` | Expande: `expr_body` → `item rest1` |
| 140 | `item rest1 RPAREN body $` | `( ( VARA ) 0 > ) ( ( VARA …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 141 | `LPAREN expr_body RPAREN rest1 RPAREN body $` | `( ( VARA ) 0 > ) ( ( VARA …` | Casa: `LPAREN` |
| 142 | `expr_body RPAREN rest1 RPAREN body $` | `( VARA ) 0 > ) ( ( VARA ) …` | Expande: `expr_body` → `item rest1` |
| 143 | `item rest1 RPAREN rest1 RPAREN body $` | `( VARA ) 0 > ) ( ( VARA ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 144 | `LPAREN expr_body RPAREN rest1 RPAREN rest1 RPAREN…` | `( VARA ) 0 > ) ( ( VARA ) …` | Casa: `LPAREN` |
| 145 | `expr_body RPAREN rest1 RPAREN rest1 RPAREN body $` | `VARA ) 0 > ) ( ( VARA ) 1 …` | Expande: `expr_body` → `item rest1` |
| 146 | `item rest1 RPAREN rest1 RPAREN rest1 RPAREN body $` | `VARA ) 0 > ) ( ( VARA ) 1 …` | Expande: `item` → `IDENT` |
| 147 | `IDENT rest1 RPAREN rest1 RPAREN rest1 RPAREN body…` | `VARA ) 0 > ) ( ( VARA ) 1 …` | Casa: `IDENT` |
| 148 | `rest1 RPAREN rest1 RPAREN rest1 RPAREN body $` | `) 0 > ) ( ( VARA ) 1 - …` | Expande: `rest1` → `ε` |
| 149 | `RPAREN rest1 RPAREN rest1 RPAREN body $` | `) 0 > ) ( ( VARA ) 1 - …` | Casa: `RPAREN` |
| 150 | `rest1 RPAREN rest1 RPAREN body $` | `0 > ) ( ( VARA ) 1 - ) …` | Expande: `rest1` → `item rest2` |
| 151 | `item rest2 RPAREN rest1 RPAREN body $` | `0 > ) ( ( VARA ) 1 - ) …` | Expande: `item` → `NUMERO` |
| 152 | `NUMERO rest2 RPAREN rest1 RPAREN body $` | `0 > ) ( ( VARA ) 1 - ) …` | Casa: `NUMERO` |
| 153 | `rest2 RPAREN rest1 RPAREN body $` | `> ) ( ( VARA ) 1 - ) WHILE …` | Expande: `rest2` → `binop` |
| 154 | `binop RPAREN rest1 RPAREN body $` | `> ) ( ( VARA ) 1 - ) WHILE …` | Expande: `binop` → `>` |
| 155 | `> RPAREN rest1 RPAREN body $` | `> ) ( ( VARA ) 1 - ) WHILE …` | Casa: `>` |
| 156 | `RPAREN rest1 RPAREN body $` | `) ( ( VARA ) 1 - ) WHILE ) …` | Casa: `RPAREN` |
| 157 | `rest1 RPAREN body $` | `( ( VARA ) 1 - ) WHILE ) ( …` | Expande: `rest1` → `item rest2` |
| 158 | `item rest2 RPAREN body $` | `( ( VARA ) 1 - ) WHILE ) ( …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 159 | `LPAREN expr_body RPAREN rest2 RPAREN body $` | `( ( VARA ) 1 - ) WHILE ) ( …` | Casa: `LPAREN` |
| 160 | `expr_body RPAREN rest2 RPAREN body $` | `( VARA ) 1 - ) WHILE ) ( ( …` | Expande: `expr_body` → `item rest1` |
| 161 | `item rest1 RPAREN rest2 RPAREN body $` | `( VARA ) 1 - ) WHILE ) ( ( …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 162 | `LPAREN expr_body RPAREN rest1 RPAREN rest2 RPAREN…` | `( VARA ) 1 - ) WHILE ) ( ( …` | Casa: `LPAREN` |
| 163 | `expr_body RPAREN rest1 RPAREN rest2 RPAREN body $` | `VARA ) 1 - ) WHILE ) ( ( ( …` | Expande: `expr_body` → `item rest1` |
| 164 | `item rest1 RPAREN rest1 RPAREN rest2 RPAREN body $` | `VARA ) 1 - ) WHILE ) ( ( ( …` | Expande: `item` → `IDENT` |
| 165 | `IDENT rest1 RPAREN rest1 RPAREN rest2 RPAREN body…` | `VARA ) 1 - ) WHILE ) ( ( ( …` | Casa: `IDENT` |
| 166 | `rest1 RPAREN rest1 RPAREN rest2 RPAREN body $` | `) 1 - ) WHILE ) ( ( ( VARA …` | Expande: `rest1` → `ε` |
| 167 | `RPAREN rest1 RPAREN rest2 RPAREN body $` | `) 1 - ) WHILE ) ( ( ( VARA …` | Casa: `RPAREN` |
| 168 | `rest1 RPAREN rest2 RPAREN body $` | `1 - ) WHILE ) ( ( ( VARA ) …` | Expande: `rest1` → `item rest2` |
| 169 | `item rest2 RPAREN rest2 RPAREN body $` | `1 - ) WHILE ) ( ( ( VARA ) …` | Expande: `item` → `NUMERO` |
| 170 | `NUMERO rest2 RPAREN rest2 RPAREN body $` | `1 - ) WHILE ) ( ( ( VARA ) …` | Casa: `NUMERO` |
| 171 | `rest2 RPAREN rest2 RPAREN body $` | `- ) WHILE ) ( ( ( VARA ) 5 …` | Expande: `rest2` → `binop` |
| 172 | `binop RPAREN rest2 RPAREN body $` | `- ) WHILE ) ( ( ( VARA ) 5 …` | Expande: `binop` → `-` |
| 173 | `- RPAREN rest2 RPAREN body $` | `- ) WHILE ) ( ( ( VARA ) 5 …` | Casa: `-` |
| 174 | `RPAREN rest2 RPAREN body $` | `) WHILE ) ( ( ( VARA ) 5 >= …` | Casa: `RPAREN` |
| 175 | `rest2 RPAREN body $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Expande: `rest2` → `kw_ctrl3` |
| 176 | `kw_ctrl3 RPAREN body $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Expande: `kw_ctrl3` → `WHILE` |
| 177 | `WHILE RPAREN body $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Casa: `WHILE` |
| 178 | `RPAREN body $` | `) ( ( ( VARA ) 5 >= ) ( …` | Casa: `RPAREN` |
| 179 | `body $` | `( ( ( VARA ) 5 >= ) ( 1 …` | Expande: `body` → `LPAREN body_tail` |
| 180 | `LPAREN body_tail $` | `( ( ( VARA ) 5 >= ) ( 1 …` | Casa: `LPAREN` |
| 181 | `body_tail $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 182 | `expr_body RPAREN body $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `expr_body` → `item rest1` |
| 183 | `item rest1 RPAREN body $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 184 | `LPAREN expr_body RPAREN rest1 RPAREN body $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Casa: `LPAREN` |
| 185 | `expr_body RPAREN rest1 RPAREN body $` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Expande: `expr_body` → `item rest1` |
| 186 | `item rest1 RPAREN rest1 RPAREN body $` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 187 | `LPAREN expr_body RPAREN rest1 RPAREN rest1 RPAREN…` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Casa: `LPAREN` |
| 188 | `expr_body RPAREN rest1 RPAREN rest1 RPAREN body $` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Expande: `expr_body` → `item rest1` |
| 189 | `item rest1 RPAREN rest1 RPAREN rest1 RPAREN body $` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Expande: `item` → `IDENT` |
| 190 | `IDENT rest1 RPAREN rest1 RPAREN rest1 RPAREN body…` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Casa: `IDENT` |
| 191 | `rest1 RPAREN rest1 RPAREN rest1 RPAREN body $` | `) 5 >= ) ( 1 FLAG ) ( 0 …` | Expande: `rest1` → `ε` |
| 192 | `RPAREN rest1 RPAREN rest1 RPAREN body $` | `) 5 >= ) ( 1 FLAG ) ( 0 …` | Casa: `RPAREN` |
| 193 | `rest1 RPAREN rest1 RPAREN body $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Expande: `rest1` → `item rest2` |
| 194 | `item rest2 RPAREN rest1 RPAREN body $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Expande: `item` → `NUMERO` |
| 195 | `NUMERO rest2 RPAREN rest1 RPAREN body $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Casa: `NUMERO` |
| 196 | `rest2 RPAREN rest1 RPAREN body $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Expande: `rest2` → `binop` |
| 197 | `binop RPAREN rest1 RPAREN body $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Expande: `binop` → `>=` |
| 198 | `>= RPAREN rest1 RPAREN body $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Casa: `>=` |
| 199 | `RPAREN rest1 RPAREN body $` | `) ( 1 FLAG ) ( 0 FLAG ) IFELSE …` | Casa: `RPAREN` |
| 200 | `rest1 RPAREN body $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Expande: `rest1` → `item rest2` |
| 201 | `item rest2 RPAREN body $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 202 | `LPAREN expr_body RPAREN rest2 RPAREN body $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Casa: `LPAREN` |
| 203 | `expr_body RPAREN rest2 RPAREN body $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Expande: `expr_body` → `item rest1` |
| 204 | `item rest1 RPAREN rest2 RPAREN body $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Expande: `item` → `NUMERO` |
| 205 | `NUMERO rest1 RPAREN rest2 RPAREN body $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Casa: `NUMERO` |
| 206 | `rest1 RPAREN rest2 RPAREN body $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Expande: `rest1` → `item rest2` |
| 207 | `item rest2 RPAREN rest2 RPAREN body $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Expande: `item` → `IDENT` |
| 208 | `IDENT rest2 RPAREN rest2 RPAREN body $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Casa: `IDENT` |
| 209 | `rest2 RPAREN rest2 RPAREN body $` | `) ( 0 FLAG ) IFELSE ) ( ( FLAG …` | Expande: `rest2` → `ε` |
| 210 | `RPAREN rest2 RPAREN body $` | `) ( 0 FLAG ) IFELSE ) ( ( FLAG …` | Casa: `RPAREN` |
| 211 | `rest2 RPAREN body $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Expande: `rest2` → `item item_tail` |
| 212 | `item item_tail RPAREN body $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 213 | `LPAREN expr_body RPAREN item_tail RPAREN body $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Casa: `LPAREN` |
| 214 | `expr_body RPAREN item_tail RPAREN body $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Expande: `expr_body` → `item rest1` |
| 215 | `item rest1 RPAREN item_tail RPAREN body $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Expande: `item` → `NUMERO` |
| 216 | `NUMERO rest1 RPAREN item_tail RPAREN body $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Casa: `NUMERO` |
| 217 | `rest1 RPAREN item_tail RPAREN body $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Expande: `rest1` → `item rest2` |
| 218 | `item rest2 RPAREN item_tail RPAREN body $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Expande: `item` → `IDENT` |
| 219 | `IDENT rest2 RPAREN item_tail RPAREN body $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Casa: `IDENT` |
| 220 | `rest2 RPAREN item_tail RPAREN body $` | `) IFELSE ) ( ( FLAG ) 0 == ) …` | Expande: `rest2` → `ε` |
| 221 | `RPAREN item_tail RPAREN body $` | `) IFELSE ) ( ( FLAG ) 0 == ) …` | Casa: `RPAREN` |
| 222 | `item_tail RPAREN body $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Expande: `item_tail` → `kw_ctrl4` |
| 223 | `kw_ctrl4 RPAREN body $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Expande: `kw_ctrl4` → `IFELSE` |
| 224 | `IFELSE RPAREN body $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Casa: `IFELSE` |
| 225 | `RPAREN body $` | `) ( ( FLAG ) 0 == ) ( ( …` | Casa: `RPAREN` |
| 226 | `body $` | `( ( FLAG ) 0 == ) ( ( 10 …` | Expande: `body` → `LPAREN body_tail` |
| 227 | `LPAREN body_tail $` | `( ( FLAG ) 0 == ) ( ( 10 …` | Casa: `LPAREN` |
| 228 | `body_tail $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 229 | `expr_body RPAREN body $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `expr_body` → `item rest1` |
| 230 | `item rest1 RPAREN body $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 231 | `LPAREN expr_body RPAREN rest1 RPAREN body $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Casa: `LPAREN` |
| 232 | `expr_body RPAREN rest1 RPAREN body $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Expande: `expr_body` → `item rest1` |
| 233 | `item rest1 RPAREN rest1 RPAREN body $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Expande: `item` → `IDENT` |
| 234 | `IDENT rest1 RPAREN rest1 RPAREN body $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Casa: `IDENT` |
| 235 | `rest1 RPAREN rest1 RPAREN body $` | `) 0 == ) ( ( 10 3 + ) …` | Expande: `rest1` → `ε` |
| 236 | `RPAREN rest1 RPAREN body $` | `) 0 == ) ( ( 10 3 + ) …` | Casa: `RPAREN` |
| 237 | `rest1 RPAREN body $` | `0 == ) ( ( 10 3 + ) ( …` | Expande: `rest1` → `item rest2` |
| 238 | `item rest2 RPAREN body $` | `0 == ) ( ( 10 3 + ) ( …` | Expande: `item` → `NUMERO` |
| 239 | `NUMERO rest2 RPAREN body $` | `0 == ) ( ( 10 3 + ) ( …` | Casa: `NUMERO` |
| 240 | `rest2 RPAREN body $` | `== ) ( ( 10 3 + ) ( 2 …` | Expande: `rest2` → `binop` |
| 241 | `binop RPAREN body $` | `== ) ( ( 10 3 + ) ( 2 …` | Expande: `binop` → `==` |
| 242 | `== RPAREN body $` | `== ) ( ( 10 3 + ) ( 2 …` | Casa: `==` |
| 243 | `RPAREN body $` | `) ( ( 10 3 + ) ( 2 4 …` | Casa: `RPAREN` |
| 244 | `body $` | `( ( 10 3 + ) ( 2 4 * …` | Expande: `body` → `LPAREN body_tail` |
| 245 | `LPAREN body_tail $` | `( ( 10 3 + ) ( 2 4 * …` | Casa: `LPAREN` |
| 246 | `body_tail $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `body_tail` → `expr_body RPAREN body` |
| 247 | `expr_body RPAREN body $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `expr_body` → `item rest1` |
| 248 | `item rest1 RPAREN body $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 249 | `LPAREN expr_body RPAREN rest1 RPAREN body $` | `( 10 3 + ) ( 2 4 * ) …` | Casa: `LPAREN` |
| 250 | `expr_body RPAREN rest1 RPAREN body $` | `10 3 + ) ( 2 4 * ) - …` | Expande: `expr_body` → `item rest1` |
| 251 | `item rest1 RPAREN rest1 RPAREN body $` | `10 3 + ) ( 2 4 * ) - …` | Expande: `item` → `NUMERO` |
| 252 | `NUMERO rest1 RPAREN rest1 RPAREN body $` | `10 3 + ) ( 2 4 * ) - …` | Casa: `NUMERO` |
| 253 | `rest1 RPAREN rest1 RPAREN body $` | `3 + ) ( 2 4 * ) - ) …` | Expande: `rest1` → `item rest2` |
| 254 | `item rest2 RPAREN rest1 RPAREN body $` | `3 + ) ( 2 4 * ) - ) …` | Expande: `item` → `NUMERO` |
| 255 | `NUMERO rest2 RPAREN rest1 RPAREN body $` | `3 + ) ( 2 4 * ) - ) …` | Casa: `NUMERO` |
| 256 | `rest2 RPAREN rest1 RPAREN body $` | `+ ) ( 2 4 * ) - ) ( …` | Expande: `rest2` → `binop` |
| 257 | `binop RPAREN rest1 RPAREN body $` | `+ ) ( 2 4 * ) - ) ( …` | Expande: `binop` → `+` |
| 258 | `+ RPAREN rest1 RPAREN body $` | `+ ) ( 2 4 * ) - ) ( …` | Casa: `+` |
| 259 | `RPAREN rest1 RPAREN body $` | `) ( 2 4 * ) - ) ( END …` | Casa: `RPAREN` |
| 260 | `rest1 RPAREN body $` | `( 2 4 * ) - ) ( END )` | Expande: `rest1` → `item rest2` |
| 261 | `item rest2 RPAREN body $` | `( 2 4 * ) - ) ( END )` | Expande: `item` → `LPAREN expr_body RPAREN` |
| 262 | `LPAREN expr_body RPAREN rest2 RPAREN body $` | `( 2 4 * ) - ) ( END )` | Casa: `LPAREN` |
| 263 | `expr_body RPAREN rest2 RPAREN body $` | `2 4 * ) - ) ( END )` | Expande: `expr_body` → `item rest1` |
| 264 | `item rest1 RPAREN rest2 RPAREN body $` | `2 4 * ) - ) ( END )` | Expande: `item` → `NUMERO` |
| 265 | `NUMERO rest1 RPAREN rest2 RPAREN body $` | `2 4 * ) - ) ( END )` | Casa: `NUMERO` |
| 266 | `rest1 RPAREN rest2 RPAREN body $` | `4 * ) - ) ( END )` | Expande: `rest1` → `item rest2` |
| 267 | `item rest2 RPAREN rest2 RPAREN body $` | `4 * ) - ) ( END )` | Expande: `item` → `NUMERO` |
| 268 | `NUMERO rest2 RPAREN rest2 RPAREN body $` | `4 * ) - ) ( END )` | Casa: `NUMERO` |
| 269 | `rest2 RPAREN rest2 RPAREN body $` | `* ) - ) ( END )` | Expande: `rest2` → `binop` |
| 270 | `binop RPAREN rest2 RPAREN body $` | `* ) - ) ( END )` | Expande: `binop` → `*` |
| 271 | `* RPAREN rest2 RPAREN body $` | `* ) - ) ( END )` | Casa: `*` |
| 272 | `RPAREN rest2 RPAREN body $` | `) - ) ( END )` | Casa: `RPAREN` |
| 273 | `rest2 RPAREN body $` | `- ) ( END )` | Expande: `rest2` → `binop` |
| 274 | `binop RPAREN body $` | `- ) ( END )` | Expande: `binop` → `-` |
| 275 | `- RPAREN body $` | `- ) ( END )` | Casa: `-` |
| 276 | `RPAREN body $` | `) ( END )` | Casa: `RPAREN` |
| 277 | `body $` | `( END )` | Expande: `body` → `LPAREN body_tail` |
| 278 | `LPAREN body_tail $` | `( END )` | Casa: `LPAREN` |
| 279 | `body_tail $` | `END )` | Expande: `body_tail` → `END RPAREN` |
| 280 | `END RPAREN $` | `END )` | Casa: `END` |
| 281 | `RPAREN $` | `)` | Casa: `RPAREN` |
| 282 | `$` | `$` | Casa: `$` |
