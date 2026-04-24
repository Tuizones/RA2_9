# Derivação LL(1) — Passo a Passo

| Passo | Pilha (topo →) | Entrada (→) | Ação |
|------:|---|---|---|
| 1 | `PROGRAM $` | `( START ) ( 10 3 + ) ( 7.5 …` | Expande: `PROGRAM` → `( start ) BODY` |
| 2 | `( start ) BODY $` | `( START ) ( 10 3 + ) ( 7.5 …` | Casa: `(` |
| 3 | `start ) BODY $` | `START ) ( 10 3 + ) ( 7.5 2.5 …` | Casa: `start` |
| 4 | `) BODY $` | `) ( 10 3 + ) ( 7.5 2.5 - …` | Casa: `)` |
| 5 | `BODY $` | `( 10 3 + ) ( 7.5 2.5 - ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 6 | `( BODY_TAIL $` | `( 10 3 + ) ( 7.5 2.5 - ) …` | Casa: `(` |
| 7 | `BODY_TAIL $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 8 | `EXPR_BODY ) BODY $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 9 | `ITEM REST1 ) BODY $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Expande: `ITEM` → `numero` |
| 10 | `numero REST1 ) BODY $` | `10 3 + ) ( 7.5 2.5 - ) ( …` | Casa: `numero` |
| 11 | `REST1 ) BODY $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Expande: `REST1` → `ITEM REST2` |
| 12 | `ITEM REST2 ) BODY $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Expande: `ITEM` → `numero` |
| 13 | `numero REST2 ) BODY $` | `3 + ) ( 7.5 2.5 - ) ( 4 …` | Casa: `numero` |
| 14 | `REST2 ) BODY $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Expande: `REST2` → `BINOP` |
| 15 | `BINOP ) BODY $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Expande: `BINOP` → `+` |
| 16 | `+ ) BODY $` | `+ ) ( 7.5 2.5 - ) ( 4 2.5 …` | Casa: `+` |
| 17 | `) BODY $` | `) ( 7.5 2.5 - ) ( 4 2.5 * …` | Casa: `)` |
| 18 | `BODY $` | `( 7.5 2.5 - ) ( 4 2.5 * ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 19 | `( BODY_TAIL $` | `( 7.5 2.5 - ) ( 4 2.5 * ) …` | Casa: `(` |
| 20 | `BODY_TAIL $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 21 | `EXPR_BODY ) BODY $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 22 | `ITEM REST1 ) BODY $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Expande: `ITEM` → `numero` |
| 23 | `numero REST1 ) BODY $` | `7.5 2.5 - ) ( 4 2.5 * ) ( …` | Casa: `numero` |
| 24 | `REST1 ) BODY $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Expande: `REST1` → `ITEM REST2` |
| 25 | `ITEM REST2 ) BODY $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Expande: `ITEM` → `numero` |
| 26 | `numero REST2 ) BODY $` | `2.5 - ) ( 4 2.5 * ) ( 10.0 …` | Casa: `numero` |
| 27 | `REST2 ) BODY $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Expande: `REST2` → `BINOP` |
| 28 | `BINOP ) BODY $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Expande: `BINOP` → `-` |
| 29 | `- ) BODY $` | `- ) ( 4 2.5 * ) ( 10.0 4.0 …` | Casa: `-` |
| 30 | `) BODY $` | `) ( 4 2.5 * ) ( 10.0 4.0 \| …` | Casa: `)` |
| 31 | `BODY $` | `( 4 2.5 * ) ( 10.0 4.0 \| ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 32 | `( BODY_TAIL $` | `( 4 2.5 * ) ( 10.0 4.0 \| ) …` | Casa: `(` |
| 33 | `BODY_TAIL $` | `4 2.5 * ) ( 10.0 4.0 \| ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 34 | `EXPR_BODY ) BODY $` | `4 2.5 * ) ( 10.0 4.0 \| ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 35 | `ITEM REST1 ) BODY $` | `4 2.5 * ) ( 10.0 4.0 \| ) ( …` | Expande: `ITEM` → `numero` |
| 36 | `numero REST1 ) BODY $` | `4 2.5 * ) ( 10.0 4.0 \| ) ( …` | Casa: `numero` |
| 37 | `REST1 ) BODY $` | `2.5 * ) ( 10.0 4.0 \| ) ( 10 …` | Expande: `REST1` → `ITEM REST2` |
| 38 | `ITEM REST2 ) BODY $` | `2.5 * ) ( 10.0 4.0 \| ) ( 10 …` | Expande: `ITEM` → `numero` |
| 39 | `numero REST2 ) BODY $` | `2.5 * ) ( 10.0 4.0 \| ) ( 10 …` | Casa: `numero` |
| 40 | `REST2 ) BODY $` | `* ) ( 10.0 4.0 \| ) ( 10 3 …` | Expande: `REST2` → `BINOP` |
| 41 | `BINOP ) BODY $` | `* ) ( 10.0 4.0 \| ) ( 10 3 …` | Expande: `BINOP` → `*` |
| 42 | `* ) BODY $` | `* ) ( 10.0 4.0 \| ) ( 10 3 …` | Casa: `*` |
| 43 | `) BODY $` | `) ( 10.0 4.0 \| ) ( 10 3 / …` | Casa: `)` |
| 44 | `BODY $` | `( 10.0 4.0 \| ) ( 10 3 / ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 45 | `( BODY_TAIL $` | `( 10.0 4.0 \| ) ( 10 3 / ) …` | Casa: `(` |
| 46 | `BODY_TAIL $` | `10.0 4.0 \| ) ( 10 3 / ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 47 | `EXPR_BODY ) BODY $` | `10.0 4.0 \| ) ( 10 3 / ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 48 | `ITEM REST1 ) BODY $` | `10.0 4.0 \| ) ( 10 3 / ) ( …` | Expande: `ITEM` → `numero` |
| 49 | `numero REST1 ) BODY $` | `10.0 4.0 \| ) ( 10 3 / ) ( …` | Casa: `numero` |
| 50 | `REST1 ) BODY $` | `4.0 \| ) ( 10 3 / ) ( 10 …` | Expande: `REST1` → `ITEM REST2` |
| 51 | `ITEM REST2 ) BODY $` | `4.0 \| ) ( 10 3 / ) ( 10 …` | Expande: `ITEM` → `numero` |
| 52 | `numero REST2 ) BODY $` | `4.0 \| ) ( 10 3 / ) ( 10 …` | Casa: `numero` |
| 53 | `REST2 ) BODY $` | `\| ) ( 10 3 / ) ( 10 3 …` | Expande: `REST2` → `BINOP` |
| 54 | `BINOP ) BODY $` | `\| ) ( 10 3 / ) ( 10 3 …` | Expande: `BINOP` → `\|` |
| 55 | `\| ) BODY $` | `\| ) ( 10 3 / ) ( 10 3 …` | Casa: `\|` |
| 56 | `) BODY $` | `) ( 10 3 / ) ( 10 3 % …` | Casa: `)` |
| 57 | `BODY $` | `( 10 3 / ) ( 10 3 % ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 58 | `( BODY_TAIL $` | `( 10 3 / ) ( 10 3 % ) …` | Casa: `(` |
| 59 | `BODY_TAIL $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 60 | `EXPR_BODY ) BODY $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 61 | `ITEM REST1 ) BODY $` | `10 3 / ) ( 10 3 % ) ( …` | Expande: `ITEM` → `numero` |
| 62 | `numero REST1 ) BODY $` | `10 3 / ) ( 10 3 % ) ( …` | Casa: `numero` |
| 63 | `REST1 ) BODY $` | `3 / ) ( 10 3 % ) ( 2 …` | Expande: `REST1` → `ITEM REST2` |
| 64 | `ITEM REST2 ) BODY $` | `3 / ) ( 10 3 % ) ( 2 …` | Expande: `ITEM` → `numero` |
| 65 | `numero REST2 ) BODY $` | `3 / ) ( 10 3 % ) ( 2 …` | Casa: `numero` |
| 66 | `REST2 ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `REST2` → `BINOP` |
| 67 | `BINOP ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `BINOP` → `/` |
| 68 | `/ ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Casa: `/` |
| 69 | `) BODY $` | `) ( 10 3 % ) ( 2 5 ^ …` | Casa: `)` |
| 70 | `BODY $` | `( 10 3 % ) ( 2 5 ^ ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 71 | `( BODY_TAIL $` | `( 10 3 % ) ( 2 5 ^ ) …` | Casa: `(` |
| 72 | `BODY_TAIL $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 73 | `EXPR_BODY ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 74 | `ITEM REST1 ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `ITEM` → `numero` |
| 75 | `numero REST1 ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Casa: `numero` |
| 76 | `REST1 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Expande: `REST1` → `ITEM REST2` |
| 77 | `ITEM REST2 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Expande: `ITEM` → `numero` |
| 78 | `numero REST2 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 20 …` | Casa: `numero` |
| 79 | `REST2 ) BODY $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Expande: `REST2` → `BINOP` |
| 80 | `BINOP ) BODY $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Expande: `BINOP` → `%` |
| 81 | `% ) BODY $` | `% ) ( 2 5 ^ ) ( 20 VARA …` | Casa: `%` |
| 82 | `) BODY $` | `) ( 2 5 ^ ) ( 20 VARA ) …` | Casa: `)` |
| 83 | `BODY $` | `( 2 5 ^ ) ( 20 VARA ) ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 84 | `( BODY_TAIL $` | `( 2 5 ^ ) ( 20 VARA ) ( …` | Casa: `(` |
| 85 | `BODY_TAIL $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 86 | `EXPR_BODY ) BODY $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 87 | `ITEM REST1 ) BODY $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Expande: `ITEM` → `numero` |
| 88 | `numero REST1 ) BODY $` | `2 5 ^ ) ( 20 VARA ) ( ( …` | Casa: `numero` |
| 89 | `REST1 ) BODY $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Expande: `REST1` → `ITEM REST2` |
| 90 | `ITEM REST2 ) BODY $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Expande: `ITEM` → `numero` |
| 91 | `numero REST2 ) BODY $` | `5 ^ ) ( 20 VARA ) ( ( VARA …` | Casa: `numero` |
| 92 | `REST2 ) BODY $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Expande: `REST2` → `BINOP` |
| 93 | `BINOP ) BODY $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Expande: `BINOP` → `^` |
| 94 | `^ ) BODY $` | `^ ) ( 20 VARA ) ( ( VARA ) …` | Casa: `^` |
| 95 | `) BODY $` | `) ( 20 VARA ) ( ( VARA ) 2 …` | Casa: `)` |
| 96 | `BODY $` | `( 20 VARA ) ( ( VARA ) 2 \| …` | Expande: `BODY` → `( BODY_TAIL` |
| 97 | `( BODY_TAIL $` | `( 20 VARA ) ( ( VARA ) 2 \| …` | Casa: `(` |
| 98 | `BODY_TAIL $` | `20 VARA ) ( ( VARA ) 2 \| ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 99 | `EXPR_BODY ) BODY $` | `20 VARA ) ( ( VARA ) 2 \| ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 100 | `ITEM REST1 ) BODY $` | `20 VARA ) ( ( VARA ) 2 \| ) …` | Expande: `ITEM` → `numero` |
| 101 | `numero REST1 ) BODY $` | `20 VARA ) ( ( VARA ) 2 \| ) …` | Casa: `numero` |
| 102 | `REST1 ) BODY $` | `VARA ) ( ( VARA ) 2 \| ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 103 | `ITEM REST2 ) BODY $` | `VARA ) ( ( VARA ) 2 \| ) ( …` | Expande: `ITEM` → `ident` |
| 104 | `ident REST2 ) BODY $` | `VARA ) ( ( VARA ) 2 \| ) ( …` | Casa: `ident` |
| 105 | `REST2 ) BODY $` | `) ( ( VARA ) 2 \| ) ( 2 …` | Expande: `REST2` → `ε` |
| 106 | `) BODY $` | `) ( ( VARA ) 2 \| ) ( 2 …` | Casa: `)` |
| 107 | `BODY $` | `( ( VARA ) 2 \| ) ( 2 RES …` | Expande: `BODY` → `( BODY_TAIL` |
| 108 | `( BODY_TAIL $` | `( ( VARA ) 2 \| ) ( 2 RES …` | Casa: `(` |
| 109 | `BODY_TAIL $` | `( VARA ) 2 \| ) ( 2 RES ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 110 | `EXPR_BODY ) BODY $` | `( VARA ) 2 \| ) ( 2 RES ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 111 | `ITEM REST1 ) BODY $` | `( VARA ) 2 \| ) ( 2 RES ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 112 | `( EXPR_BODY ) REST1 ) BODY $` | `( VARA ) 2 \| ) ( 2 RES ) …` | Casa: `(` |
| 113 | `EXPR_BODY ) REST1 ) BODY $` | `VARA ) 2 \| ) ( 2 RES ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 114 | `ITEM REST1 ) REST1 ) BODY $` | `VARA ) 2 \| ) ( 2 RES ) ( …` | Expande: `ITEM` → `ident` |
| 115 | `ident REST1 ) REST1 ) BODY $` | `VARA ) 2 \| ) ( 2 RES ) ( …` | Casa: `ident` |
| 116 | `REST1 ) REST1 ) BODY $` | `) 2 \| ) ( 2 RES ) ( ( …` | Expande: `REST1` → `ε` |
| 117 | `) REST1 ) BODY $` | `) 2 \| ) ( 2 RES ) ( ( …` | Casa: `)` |
| 118 | `REST1 ) BODY $` | `2 \| ) ( 2 RES ) ( ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 119 | `ITEM REST2 ) BODY $` | `2 \| ) ( 2 RES ) ( ( ( …` | Expande: `ITEM` → `numero` |
| 120 | `numero REST2 ) BODY $` | `2 \| ) ( 2 RES ) ( ( ( …` | Casa: `numero` |
| 121 | `REST2 ) BODY $` | `\| ) ( 2 RES ) ( ( ( VARA …` | Expande: `REST2` → `BINOP` |
| 122 | `BINOP ) BODY $` | `\| ) ( 2 RES ) ( ( ( VARA …` | Expande: `BINOP` → `\|` |
| 123 | `\| ) BODY $` | `\| ) ( 2 RES ) ( ( ( VARA …` | Casa: `\|` |
| 124 | `) BODY $` | `) ( 2 RES ) ( ( ( VARA ) …` | Casa: `)` |
| 125 | `BODY $` | `( 2 RES ) ( ( ( VARA ) 0 …` | Expande: `BODY` → `( BODY_TAIL` |
| 126 | `( BODY_TAIL $` | `( 2 RES ) ( ( ( VARA ) 0 …` | Casa: `(` |
| 127 | `BODY_TAIL $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 128 | `EXPR_BODY ) BODY $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 129 | `ITEM REST1 ) BODY $` | `2 RES ) ( ( ( VARA ) 0 > …` | Expande: `ITEM` → `numero` |
| 130 | `numero REST1 ) BODY $` | `2 RES ) ( ( ( VARA ) 0 > …` | Casa: `numero` |
| 131 | `REST1 ) BODY $` | `RES ) ( ( ( VARA ) 0 > ) …` | Expande: `REST1` → `ITEM REST2` |
| 132 | `ITEM REST2 ) BODY $` | `RES ) ( ( ( VARA ) 0 > ) …` | Expande: `ITEM` → `res` |
| 133 | `res REST2 ) BODY $` | `RES ) ( ( ( VARA ) 0 > ) …` | Casa: `res` |
| 134 | `REST2 ) BODY $` | `) ( ( ( VARA ) 0 > ) ( …` | Expande: `REST2` → `ε` |
| 135 | `) BODY $` | `) ( ( ( VARA ) 0 > ) ( …` | Casa: `)` |
| 136 | `BODY $` | `( ( ( VARA ) 0 > ) ( ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 137 | `( BODY_TAIL $` | `( ( ( VARA ) 0 > ) ( ( …` | Casa: `(` |
| 138 | `BODY_TAIL $` | `( ( VARA ) 0 > ) ( ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 139 | `EXPR_BODY ) BODY $` | `( ( VARA ) 0 > ) ( ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 140 | `ITEM REST1 ) BODY $` | `( ( VARA ) 0 > ) ( ( ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 141 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( VARA ) 0 > ) ( ( ( …` | Casa: `(` |
| 142 | `EXPR_BODY ) REST1 ) BODY $` | `( VARA ) 0 > ) ( ( ( VARA …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 143 | `ITEM REST1 ) REST1 ) BODY $` | `( VARA ) 0 > ) ( ( ( VARA …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 144 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( VARA ) 0 > ) ( ( ( VARA …` | Casa: `(` |
| 145 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `VARA ) 0 > ) ( ( ( VARA ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 146 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `VARA ) 0 > ) ( ( ( VARA ) …` | Expande: `ITEM` → `ident` |
| 147 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `VARA ) 0 > ) ( ( ( VARA ) …` | Casa: `ident` |
| 148 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 0 > ) ( ( ( VARA ) 10 …` | Expande: `REST1` → `ε` |
| 149 | `) REST1 ) REST1 ) BODY $` | `) 0 > ) ( ( ( VARA ) 10 …` | Casa: `)` |
| 150 | `REST1 ) REST1 ) BODY $` | `0 > ) ( ( ( VARA ) 10 - …` | Expande: `REST1` → `ITEM REST2` |
| 151 | `ITEM REST2 ) REST1 ) BODY $` | `0 > ) ( ( ( VARA ) 10 - …` | Expande: `ITEM` → `numero` |
| 152 | `numero REST2 ) REST1 ) BODY $` | `0 > ) ( ( ( VARA ) 10 - …` | Casa: `numero` |
| 153 | `REST2 ) REST1 ) BODY $` | `> ) ( ( ( VARA ) 10 - ) …` | Expande: `REST2` → `BINOP` |
| 154 | `BINOP ) REST1 ) BODY $` | `> ) ( ( ( VARA ) 10 - ) …` | Expande: `BINOP` → `>` |
| 155 | `> ) REST1 ) BODY $` | `> ) ( ( ( VARA ) 10 - ) …` | Casa: `>` |
| 156 | `) REST1 ) BODY $` | `) ( ( ( VARA ) 10 - ) VARA …` | Casa: `)` |
| 157 | `REST1 ) BODY $` | `( ( ( VARA ) 10 - ) VARA ) …` | Expande: `REST1` → `ITEM REST2` |
| 158 | `ITEM REST2 ) BODY $` | `( ( ( VARA ) 10 - ) VARA ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 159 | `( EXPR_BODY ) REST2 ) BODY $` | `( ( ( VARA ) 10 - ) VARA ) …` | Casa: `(` |
| 160 | `EXPR_BODY ) REST2 ) BODY $` | `( ( VARA ) 10 - ) VARA ) WHILE …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 161 | `ITEM REST1 ) REST2 ) BODY $` | `( ( VARA ) 10 - ) VARA ) WHILE …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 162 | `( EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( ( VARA ) 10 - ) VARA ) WHILE …` | Casa: `(` |
| 163 | `EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( VARA ) 10 - ) VARA ) WHILE ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 164 | `ITEM REST1 ) REST1 ) REST2 ) BODY $` | `( VARA ) 10 - ) VARA ) WHILE ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 165 | `( EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `( VARA ) 10 - ) VARA ) WHILE ) …` | Casa: `(` |
| 166 | `EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `VARA ) 10 - ) VARA ) WHILE ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 167 | `ITEM REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `VARA ) 10 - ) VARA ) WHILE ) ( …` | Expande: `ITEM` → `ident` |
| 168 | `ident REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `VARA ) 10 - ) VARA ) WHILE ) ( …` | Casa: `ident` |
| 169 | `REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `) 10 - ) VARA ) WHILE ) ( ( …` | Expande: `REST1` → `ε` |
| 170 | `) REST1 ) REST1 ) REST2 ) BODY $` | `) 10 - ) VARA ) WHILE ) ( ( …` | Casa: `)` |
| 171 | `REST1 ) REST1 ) REST2 ) BODY $` | `10 - ) VARA ) WHILE ) ( ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 172 | `ITEM REST2 ) REST1 ) REST2 ) BODY $` | `10 - ) VARA ) WHILE ) ( ( ( …` | Expande: `ITEM` → `numero` |
| 173 | `numero REST2 ) REST1 ) REST2 ) BODY $` | `10 - ) VARA ) WHILE ) ( ( ( …` | Casa: `numero` |
| 174 | `REST2 ) REST1 ) REST2 ) BODY $` | `- ) VARA ) WHILE ) ( ( ( VARA …` | Expande: `REST2` → `BINOP` |
| 175 | `BINOP ) REST1 ) REST2 ) BODY $` | `- ) VARA ) WHILE ) ( ( ( VARA …` | Expande: `BINOP` → `-` |
| 176 | `- ) REST1 ) REST2 ) BODY $` | `- ) VARA ) WHILE ) ( ( ( VARA …` | Casa: `-` |
| 177 | `) REST1 ) REST2 ) BODY $` | `) VARA ) WHILE ) ( ( ( VARA ) …` | Casa: `)` |
| 178 | `REST1 ) REST2 ) BODY $` | `VARA ) WHILE ) ( ( ( VARA ) 5 …` | Expande: `REST1` → `ITEM REST2` |
| 179 | `ITEM REST2 ) REST2 ) BODY $` | `VARA ) WHILE ) ( ( ( VARA ) 5 …` | Expande: `ITEM` → `ident` |
| 180 | `ident REST2 ) REST2 ) BODY $` | `VARA ) WHILE ) ( ( ( VARA ) 5 …` | Casa: `ident` |
| 181 | `REST2 ) REST2 ) BODY $` | `) WHILE ) ( ( ( VARA ) 5 >= …` | Expande: `REST2` → `ε` |
| 182 | `) REST2 ) BODY $` | `) WHILE ) ( ( ( VARA ) 5 >= …` | Casa: `)` |
| 183 | `REST2 ) BODY $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Expande: `REST2` → `KW_CTRL3` |
| 184 | `KW_CTRL3 ) BODY $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Expande: `KW_CTRL3` → `while` |
| 185 | `while ) BODY $` | `WHILE ) ( ( ( VARA ) 5 >= ) …` | Casa: `while` |
| 186 | `) BODY $` | `) ( ( ( VARA ) 5 >= ) ( …` | Casa: `)` |
| 187 | `BODY $` | `( ( ( VARA ) 5 >= ) ( 1 …` | Expande: `BODY` → `( BODY_TAIL` |
| 188 | `( BODY_TAIL $` | `( ( ( VARA ) 5 >= ) ( 1 …` | Casa: `(` |
| 189 | `BODY_TAIL $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 190 | `EXPR_BODY ) BODY $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 191 | `ITEM REST1 ) BODY $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 192 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( VARA ) 5 >= ) ( 1 FLAG …` | Casa: `(` |
| 193 | `EXPR_BODY ) REST1 ) BODY $` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 194 | `ITEM REST1 ) REST1 ) BODY $` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 195 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( VARA ) 5 >= ) ( 1 FLAG ) …` | Casa: `(` |
| 196 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 197 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Expande: `ITEM` → `ident` |
| 198 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `VARA ) 5 >= ) ( 1 FLAG ) ( …` | Casa: `ident` |
| 199 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 5 >= ) ( 1 FLAG ) ( 0 …` | Expande: `REST1` → `ε` |
| 200 | `) REST1 ) REST1 ) BODY $` | `) 5 >= ) ( 1 FLAG ) ( 0 …` | Casa: `)` |
| 201 | `REST1 ) REST1 ) BODY $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Expande: `REST1` → `ITEM REST2` |
| 202 | `ITEM REST2 ) REST1 ) BODY $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Expande: `ITEM` → `numero` |
| 203 | `numero REST2 ) REST1 ) BODY $` | `5 >= ) ( 1 FLAG ) ( 0 FLAG …` | Casa: `numero` |
| 204 | `REST2 ) REST1 ) BODY $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Expande: `REST2` → `BINOP` |
| 205 | `BINOP ) REST1 ) BODY $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Expande: `BINOP` → `>=` |
| 206 | `>= ) REST1 ) BODY $` | `>= ) ( 1 FLAG ) ( 0 FLAG ) …` | Casa: `>=` |
| 207 | `) REST1 ) BODY $` | `) ( 1 FLAG ) ( 0 FLAG ) IFELSE …` | Casa: `)` |
| 208 | `REST1 ) BODY $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Expande: `REST1` → `ITEM REST2` |
| 209 | `ITEM REST2 ) BODY $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 210 | `( EXPR_BODY ) REST2 ) BODY $` | `( 1 FLAG ) ( 0 FLAG ) IFELSE ) …` | Casa: `(` |
| 211 | `EXPR_BODY ) REST2 ) BODY $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 212 | `ITEM REST1 ) REST2 ) BODY $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Expande: `ITEM` → `numero` |
| 213 | `numero REST1 ) REST2 ) BODY $` | `1 FLAG ) ( 0 FLAG ) IFELSE ) ( …` | Casa: `numero` |
| 214 | `REST1 ) REST2 ) BODY $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 215 | `ITEM REST2 ) REST2 ) BODY $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Expande: `ITEM` → `ident` |
| 216 | `ident REST2 ) REST2 ) BODY $` | `FLAG ) ( 0 FLAG ) IFELSE ) ( ( …` | Casa: `ident` |
| 217 | `REST2 ) REST2 ) BODY $` | `) ( 0 FLAG ) IFELSE ) ( ( FLAG …` | Expande: `REST2` → `ε` |
| 218 | `) REST2 ) BODY $` | `) ( 0 FLAG ) IFELSE ) ( ( FLAG …` | Casa: `)` |
| 219 | `REST2 ) BODY $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Expande: `REST2` → `ITEM ITEM_TAIL` |
| 220 | `ITEM ITEM_TAIL ) BODY $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 221 | `( EXPR_BODY ) ITEM_TAIL ) BODY $` | `( 0 FLAG ) IFELSE ) ( ( FLAG ) …` | Casa: `(` |
| 222 | `EXPR_BODY ) ITEM_TAIL ) BODY $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 223 | `ITEM REST1 ) ITEM_TAIL ) BODY $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Expande: `ITEM` → `numero` |
| 224 | `numero REST1 ) ITEM_TAIL ) BODY $` | `0 FLAG ) IFELSE ) ( ( FLAG ) 0 …` | Casa: `numero` |
| 225 | `REST1 ) ITEM_TAIL ) BODY $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Expande: `REST1` → `ITEM REST2` |
| 226 | `ITEM REST2 ) ITEM_TAIL ) BODY $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Expande: `ITEM` → `ident` |
| 227 | `ident REST2 ) ITEM_TAIL ) BODY $` | `FLAG ) IFELSE ) ( ( FLAG ) 0 == …` | Casa: `ident` |
| 228 | `REST2 ) ITEM_TAIL ) BODY $` | `) IFELSE ) ( ( FLAG ) 0 == ) …` | Expande: `REST2` → `ε` |
| 229 | `) ITEM_TAIL ) BODY $` | `) IFELSE ) ( ( FLAG ) 0 == ) …` | Casa: `)` |
| 230 | `ITEM_TAIL ) BODY $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Expande: `ITEM_TAIL` → `KW_CTRL4` |
| 231 | `KW_CTRL4 ) BODY $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Expande: `KW_CTRL4` → `ifelse` |
| 232 | `ifelse ) BODY $` | `IFELSE ) ( ( FLAG ) 0 == ) ( …` | Casa: `ifelse` |
| 233 | `) BODY $` | `) ( ( FLAG ) 0 == ) ( ( …` | Casa: `)` |
| 234 | `BODY $` | `( ( FLAG ) 0 == ) ( ( 10 …` | Expande: `BODY` → `( BODY_TAIL` |
| 235 | `( BODY_TAIL $` | `( ( FLAG ) 0 == ) ( ( 10 …` | Casa: `(` |
| 236 | `BODY_TAIL $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 237 | `EXPR_BODY ) BODY $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 238 | `ITEM REST1 ) BODY $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 239 | `( EXPR_BODY ) REST1 ) BODY $` | `( FLAG ) 0 == ) ( ( 10 3 …` | Casa: `(` |
| 240 | `EXPR_BODY ) REST1 ) BODY $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 241 | `ITEM REST1 ) REST1 ) BODY $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Expande: `ITEM` → `ident` |
| 242 | `ident REST1 ) REST1 ) BODY $` | `FLAG ) 0 == ) ( ( 10 3 + …` | Casa: `ident` |
| 243 | `REST1 ) REST1 ) BODY $` | `) 0 == ) ( ( 10 3 + ) …` | Expande: `REST1` → `ε` |
| 244 | `) REST1 ) BODY $` | `) 0 == ) ( ( 10 3 + ) …` | Casa: `)` |
| 245 | `REST1 ) BODY $` | `0 == ) ( ( 10 3 + ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 246 | `ITEM REST2 ) BODY $` | `0 == ) ( ( 10 3 + ) ( …` | Expande: `ITEM` → `numero` |
| 247 | `numero REST2 ) BODY $` | `0 == ) ( ( 10 3 + ) ( …` | Casa: `numero` |
| 248 | `REST2 ) BODY $` | `== ) ( ( 10 3 + ) ( 2 …` | Expande: `REST2` → `BINOP` |
| 249 | `BINOP ) BODY $` | `== ) ( ( 10 3 + ) ( 2 …` | Expande: `BINOP` → `==` |
| 250 | `== ) BODY $` | `== ) ( ( 10 3 + ) ( 2 …` | Casa: `==` |
| 251 | `) BODY $` | `) ( ( 10 3 + ) ( 2 4 …` | Casa: `)` |
| 252 | `BODY $` | `( ( 10 3 + ) ( 2 4 * …` | Expande: `BODY` → `( BODY_TAIL` |
| 253 | `( BODY_TAIL $` | `( ( 10 3 + ) ( 2 4 * …` | Casa: `(` |
| 254 | `BODY_TAIL $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 255 | `EXPR_BODY ) BODY $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 256 | `ITEM REST1 ) BODY $` | `( 10 3 + ) ( 2 4 * ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 257 | `( EXPR_BODY ) REST1 ) BODY $` | `( 10 3 + ) ( 2 4 * ) …` | Casa: `(` |
| 258 | `EXPR_BODY ) REST1 ) BODY $` | `10 3 + ) ( 2 4 * ) - …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 259 | `ITEM REST1 ) REST1 ) BODY $` | `10 3 + ) ( 2 4 * ) - …` | Expande: `ITEM` → `numero` |
| 260 | `numero REST1 ) REST1 ) BODY $` | `10 3 + ) ( 2 4 * ) - …` | Casa: `numero` |
| 261 | `REST1 ) REST1 ) BODY $` | `3 + ) ( 2 4 * ) - ) …` | Expande: `REST1` → `ITEM REST2` |
| 262 | `ITEM REST2 ) REST1 ) BODY $` | `3 + ) ( 2 4 * ) - ) …` | Expande: `ITEM` → `numero` |
| 263 | `numero REST2 ) REST1 ) BODY $` | `3 + ) ( 2 4 * ) - ) …` | Casa: `numero` |
| 264 | `REST2 ) REST1 ) BODY $` | `+ ) ( 2 4 * ) - ) ( …` | Expande: `REST2` → `BINOP` |
| 265 | `BINOP ) REST1 ) BODY $` | `+ ) ( 2 4 * ) - ) ( …` | Expande: `BINOP` → `+` |
| 266 | `+ ) REST1 ) BODY $` | `+ ) ( 2 4 * ) - ) ( …` | Casa: `+` |
| 267 | `) REST1 ) BODY $` | `) ( 2 4 * ) - ) ( END …` | Casa: `)` |
| 268 | `REST1 ) BODY $` | `( 2 4 * ) - ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 269 | `ITEM REST2 ) BODY $` | `( 2 4 * ) - ) ( END )` | Expande: `ITEM` → `( EXPR_BODY )` |
| 270 | `( EXPR_BODY ) REST2 ) BODY $` | `( 2 4 * ) - ) ( END )` | Casa: `(` |
| 271 | `EXPR_BODY ) REST2 ) BODY $` | `2 4 * ) - ) ( END )` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 272 | `ITEM REST1 ) REST2 ) BODY $` | `2 4 * ) - ) ( END )` | Expande: `ITEM` → `numero` |
| 273 | `numero REST1 ) REST2 ) BODY $` | `2 4 * ) - ) ( END )` | Casa: `numero` |
| 274 | `REST1 ) REST2 ) BODY $` | `4 * ) - ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 275 | `ITEM REST2 ) REST2 ) BODY $` | `4 * ) - ) ( END )` | Expande: `ITEM` → `numero` |
| 276 | `numero REST2 ) REST2 ) BODY $` | `4 * ) - ) ( END )` | Casa: `numero` |
| 277 | `REST2 ) REST2 ) BODY $` | `* ) - ) ( END )` | Expande: `REST2` → `BINOP` |
| 278 | `BINOP ) REST2 ) BODY $` | `* ) - ) ( END )` | Expande: `BINOP` → `*` |
| 279 | `* ) REST2 ) BODY $` | `* ) - ) ( END )` | Casa: `*` |
| 280 | `) REST2 ) BODY $` | `) - ) ( END )` | Casa: `)` |
| 281 | `REST2 ) BODY $` | `- ) ( END )` | Expande: `REST2` → `BINOP` |
| 282 | `BINOP ) BODY $` | `- ) ( END )` | Expande: `BINOP` → `-` |
| 283 | `- ) BODY $` | `- ) ( END )` | Casa: `-` |
| 284 | `) BODY $` | `) ( END )` | Casa: `)` |
| 285 | `BODY $` | `( END )` | Expande: `BODY` → `( BODY_TAIL` |
| 286 | `( BODY_TAIL $` | `( END )` | Casa: `(` |
| 287 | `BODY_TAIL $` | `END )` | Expande: `BODY_TAIL` → `end )` |
| 288 | `end ) $` | `END )` | Casa: `end` |
| 289 | `) $` | `)` | Casa: `)` |
| 290 | `$` | `$` | Casa: `$` |
