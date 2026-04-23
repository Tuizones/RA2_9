# Derivação LL(1) — Passo a Passo

| Passo | Pilha (topo →) | Entrada (→) | Ação |
|------:|---|---|---|
| 1 | `PROGRAM $` | `( START ) ( 1.25 3.75 + ) ( 10.0 …` | Expande: `PROGRAM` → `( start ) BODY` |
| 2 | `( start ) BODY $` | `( START ) ( 1.25 3.75 + ) ( 10.0 …` | Casa: `(` |
| 3 | `start ) BODY $` | `START ) ( 1.25 3.75 + ) ( 10.0 4.0 …` | Casa: `start` |
| 4 | `) BODY $` | `) ( 1.25 3.75 + ) ( 10.0 4.0 - …` | Casa: `)` |
| 5 | `BODY $` | `( 1.25 3.75 + ) ( 10.0 4.0 - ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 6 | `( BODY_TAIL $` | `( 1.25 3.75 + ) ( 10.0 4.0 - ) …` | Casa: `(` |
| 7 | `BODY_TAIL $` | `1.25 3.75 + ) ( 10.0 4.0 - ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 8 | `EXPR_BODY ) BODY $` | `1.25 3.75 + ) ( 10.0 4.0 - ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 9 | `ITEM REST1 ) BODY $` | `1.25 3.75 + ) ( 10.0 4.0 - ) ( …` | Expande: `ITEM` → `numero` |
| 10 | `numero REST1 ) BODY $` | `1.25 3.75 + ) ( 10.0 4.0 - ) ( …` | Casa: `numero` |
| 11 | `REST1 ) BODY $` | `3.75 + ) ( 10.0 4.0 - ) ( 2.0 …` | Expande: `REST1` → `ITEM REST2` |
| 12 | `ITEM REST2 ) BODY $` | `3.75 + ) ( 10.0 4.0 - ) ( 2.0 …` | Expande: `ITEM` → `numero` |
| 13 | `numero REST2 ) BODY $` | `3.75 + ) ( 10.0 4.0 - ) ( 2.0 …` | Casa: `numero` |
| 14 | `REST2 ) BODY $` | `+ ) ( 10.0 4.0 - ) ( 2.0 3.5 …` | Expande: `REST2` → `BINOP` |
| 15 | `BINOP ) BODY $` | `+ ) ( 10.0 4.0 - ) ( 2.0 3.5 …` | Expande: `BINOP` → `+` |
| 16 | `+ ) BODY $` | `+ ) ( 10.0 4.0 - ) ( 2.0 3.5 …` | Casa: `+` |
| 17 | `) BODY $` | `) ( 10.0 4.0 - ) ( 2.0 3.5 * …` | Casa: `)` |
| 18 | `BODY $` | `( 10.0 4.0 - ) ( 2.0 3.5 * ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 19 | `( BODY_TAIL $` | `( 10.0 4.0 - ) ( 2.0 3.5 * ) …` | Casa: `(` |
| 20 | `BODY_TAIL $` | `10.0 4.0 - ) ( 2.0 3.5 * ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 21 | `EXPR_BODY ) BODY $` | `10.0 4.0 - ) ( 2.0 3.5 * ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 22 | `ITEM REST1 ) BODY $` | `10.0 4.0 - ) ( 2.0 3.5 * ) ( …` | Expande: `ITEM` → `numero` |
| 23 | `numero REST1 ) BODY $` | `10.0 4.0 - ) ( 2.0 3.5 * ) ( …` | Casa: `numero` |
| 24 | `REST1 ) BODY $` | `4.0 - ) ( 2.0 3.5 * ) ( 9.0 …` | Expande: `REST1` → `ITEM REST2` |
| 25 | `ITEM REST2 ) BODY $` | `4.0 - ) ( 2.0 3.5 * ) ( 9.0 …` | Expande: `ITEM` → `numero` |
| 26 | `numero REST2 ) BODY $` | `4.0 - ) ( 2.0 3.5 * ) ( 9.0 …` | Casa: `numero` |
| 27 | `REST2 ) BODY $` | `- ) ( 2.0 3.5 * ) ( 9.0 2.0 …` | Expande: `REST2` → `BINOP` |
| 28 | `BINOP ) BODY $` | `- ) ( 2.0 3.5 * ) ( 9.0 2.0 …` | Expande: `BINOP` → `-` |
| 29 | `- ) BODY $` | `- ) ( 2.0 3.5 * ) ( 9.0 2.0 …` | Casa: `-` |
| 30 | `) BODY $` | `) ( 2.0 3.5 * ) ( 9.0 2.0 \| …` | Casa: `)` |
| 31 | `BODY $` | `( 2.0 3.5 * ) ( 9.0 2.0 \| ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 32 | `( BODY_TAIL $` | `( 2.0 3.5 * ) ( 9.0 2.0 \| ) …` | Casa: `(` |
| 33 | `BODY_TAIL $` | `2.0 3.5 * ) ( 9.0 2.0 \| ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 34 | `EXPR_BODY ) BODY $` | `2.0 3.5 * ) ( 9.0 2.0 \| ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 35 | `ITEM REST1 ) BODY $` | `2.0 3.5 * ) ( 9.0 2.0 \| ) ( …` | Expande: `ITEM` → `numero` |
| 36 | `numero REST1 ) BODY $` | `2.0 3.5 * ) ( 9.0 2.0 \| ) ( …` | Casa: `numero` |
| 37 | `REST1 ) BODY $` | `3.5 * ) ( 9.0 2.0 \| ) ( 9 …` | Expande: `REST1` → `ITEM REST2` |
| 38 | `ITEM REST2 ) BODY $` | `3.5 * ) ( 9.0 2.0 \| ) ( 9 …` | Expande: `ITEM` → `numero` |
| 39 | `numero REST2 ) BODY $` | `3.5 * ) ( 9.0 2.0 \| ) ( 9 …` | Casa: `numero` |
| 40 | `REST2 ) BODY $` | `* ) ( 9.0 2.0 \| ) ( 9 2 …` | Expande: `REST2` → `BINOP` |
| 41 | `BINOP ) BODY $` | `* ) ( 9.0 2.0 \| ) ( 9 2 …` | Expande: `BINOP` → `*` |
| 42 | `* ) BODY $` | `* ) ( 9.0 2.0 \| ) ( 9 2 …` | Casa: `*` |
| 43 | `) BODY $` | `) ( 9.0 2.0 \| ) ( 9 2 / …` | Casa: `)` |
| 44 | `BODY $` | `( 9.0 2.0 \| ) ( 9 2 / ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 45 | `( BODY_TAIL $` | `( 9.0 2.0 \| ) ( 9 2 / ) …` | Casa: `(` |
| 46 | `BODY_TAIL $` | `9.0 2.0 \| ) ( 9 2 / ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 47 | `EXPR_BODY ) BODY $` | `9.0 2.0 \| ) ( 9 2 / ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 48 | `ITEM REST1 ) BODY $` | `9.0 2.0 \| ) ( 9 2 / ) ( …` | Expande: `ITEM` → `numero` |
| 49 | `numero REST1 ) BODY $` | `9.0 2.0 \| ) ( 9 2 / ) ( …` | Casa: `numero` |
| 50 | `REST1 ) BODY $` | `2.0 \| ) ( 9 2 / ) ( 9 …` | Expande: `REST1` → `ITEM REST2` |
| 51 | `ITEM REST2 ) BODY $` | `2.0 \| ) ( 9 2 / ) ( 9 …` | Expande: `ITEM` → `numero` |
| 52 | `numero REST2 ) BODY $` | `2.0 \| ) ( 9 2 / ) ( 9 …` | Casa: `numero` |
| 53 | `REST2 ) BODY $` | `\| ) ( 9 2 / ) ( 9 2 …` | Expande: `REST2` → `BINOP` |
| 54 | `BINOP ) BODY $` | `\| ) ( 9 2 / ) ( 9 2 …` | Expande: `BINOP` → `\|` |
| 55 | `\| ) BODY $` | `\| ) ( 9 2 / ) ( 9 2 …` | Casa: `\|` |
| 56 | `) BODY $` | `) ( 9 2 / ) ( 9 2 % …` | Casa: `)` |
| 57 | `BODY $` | `( 9 2 / ) ( 9 2 % ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 58 | `( BODY_TAIL $` | `( 9 2 / ) ( 9 2 % ) …` | Casa: `(` |
| 59 | `BODY_TAIL $` | `9 2 / ) ( 9 2 % ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 60 | `EXPR_BODY ) BODY $` | `9 2 / ) ( 9 2 % ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 61 | `ITEM REST1 ) BODY $` | `9 2 / ) ( 9 2 % ) ( …` | Expande: `ITEM` → `numero` |
| 62 | `numero REST1 ) BODY $` | `9 2 / ) ( 9 2 % ) ( …` | Casa: `numero` |
| 63 | `REST1 ) BODY $` | `2 / ) ( 9 2 % ) ( 2 …` | Expande: `REST1` → `ITEM REST2` |
| 64 | `ITEM REST2 ) BODY $` | `2 / ) ( 9 2 % ) ( 2 …` | Expande: `ITEM` → `numero` |
| 65 | `numero REST2 ) BODY $` | `2 / ) ( 9 2 % ) ( 2 …` | Casa: `numero` |
| 66 | `REST2 ) BODY $` | `/ ) ( 9 2 % ) ( 2 8 …` | Expande: `REST2` → `BINOP` |
| 67 | `BINOP ) BODY $` | `/ ) ( 9 2 % ) ( 2 8 …` | Expande: `BINOP` → `/` |
| 68 | `/ ) BODY $` | `/ ) ( 9 2 % ) ( 2 8 …` | Casa: `/` |
| 69 | `) BODY $` | `) ( 9 2 % ) ( 2 8 ^ …` | Casa: `)` |
| 70 | `BODY $` | `( 9 2 % ) ( 2 8 ^ ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 71 | `( BODY_TAIL $` | `( 9 2 % ) ( 2 8 ^ ) …` | Casa: `(` |
| 72 | `BODY_TAIL $` | `9 2 % ) ( 2 8 ^ ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 73 | `EXPR_BODY ) BODY $` | `9 2 % ) ( 2 8 ^ ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 74 | `ITEM REST1 ) BODY $` | `9 2 % ) ( 2 8 ^ ) ( …` | Expande: `ITEM` → `numero` |
| 75 | `numero REST1 ) BODY $` | `9 2 % ) ( 2 8 ^ ) ( …` | Casa: `numero` |
| 76 | `REST1 ) BODY $` | `2 % ) ( 2 8 ^ ) ( 3.1415 …` | Expande: `REST1` → `ITEM REST2` |
| 77 | `ITEM REST2 ) BODY $` | `2 % ) ( 2 8 ^ ) ( 3.1415 …` | Expande: `ITEM` → `numero` |
| 78 | `numero REST2 ) BODY $` | `2 % ) ( 2 8 ^ ) ( 3.1415 …` | Casa: `numero` |
| 79 | `REST2 ) BODY $` | `% ) ( 2 8 ^ ) ( 3.1415 PI …` | Expande: `REST2` → `BINOP` |
| 80 | `BINOP ) BODY $` | `% ) ( 2 8 ^ ) ( 3.1415 PI …` | Expande: `BINOP` → `%` |
| 81 | `% ) BODY $` | `% ) ( 2 8 ^ ) ( 3.1415 PI …` | Casa: `%` |
| 82 | `) BODY $` | `) ( 2 8 ^ ) ( 3.1415 PI ) …` | Casa: `)` |
| 83 | `BODY $` | `( 2 8 ^ ) ( 3.1415 PI ) ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 84 | `( BODY_TAIL $` | `( 2 8 ^ ) ( 3.1415 PI ) ( …` | Casa: `(` |
| 85 | `BODY_TAIL $` | `2 8 ^ ) ( 3.1415 PI ) ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 86 | `EXPR_BODY ) BODY $` | `2 8 ^ ) ( 3.1415 PI ) ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 87 | `ITEM REST1 ) BODY $` | `2 8 ^ ) ( 3.1415 PI ) ( ( …` | Expande: `ITEM` → `numero` |
| 88 | `numero REST1 ) BODY $` | `2 8 ^ ) ( 3.1415 PI ) ( ( …` | Casa: `numero` |
| 89 | `REST1 ) BODY $` | `8 ^ ) ( 3.1415 PI ) ( ( PI …` | Expande: `REST1` → `ITEM REST2` |
| 90 | `ITEM REST2 ) BODY $` | `8 ^ ) ( 3.1415 PI ) ( ( PI …` | Expande: `ITEM` → `numero` |
| 91 | `numero REST2 ) BODY $` | `8 ^ ) ( 3.1415 PI ) ( ( PI …` | Casa: `numero` |
| 92 | `REST2 ) BODY $` | `^ ) ( 3.1415 PI ) ( ( PI ) …` | Expande: `REST2` → `BINOP` |
| 93 | `BINOP ) BODY $` | `^ ) ( 3.1415 PI ) ( ( PI ) …` | Expande: `BINOP` → `^` |
| 94 | `^ ) BODY $` | `^ ) ( 3.1415 PI ) ( ( PI ) …` | Casa: `^` |
| 95 | `) BODY $` | `) ( 3.1415 PI ) ( ( PI ) 2.0 …` | Casa: `)` |
| 96 | `BODY $` | `( 3.1415 PI ) ( ( PI ) 2.0 * …` | Expande: `BODY` → `( BODY_TAIL` |
| 97 | `( BODY_TAIL $` | `( 3.1415 PI ) ( ( PI ) 2.0 * …` | Casa: `(` |
| 98 | `BODY_TAIL $` | `3.1415 PI ) ( ( PI ) 2.0 * ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 99 | `EXPR_BODY ) BODY $` | `3.1415 PI ) ( ( PI ) 2.0 * ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 100 | `ITEM REST1 ) BODY $` | `3.1415 PI ) ( ( PI ) 2.0 * ) …` | Expande: `ITEM` → `numero` |
| 101 | `numero REST1 ) BODY $` | `3.1415 PI ) ( ( PI ) 2.0 * ) …` | Casa: `numero` |
| 102 | `REST1 ) BODY $` | `PI ) ( ( PI ) 2.0 * ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 103 | `ITEM REST2 ) BODY $` | `PI ) ( ( PI ) 2.0 * ) ( …` | Expande: `ITEM` → `ident` |
| 104 | `ident REST2 ) BODY $` | `PI ) ( ( PI ) 2.0 * ) ( …` | Casa: `ident` |
| 105 | `REST2 ) BODY $` | `) ( ( PI ) 2.0 * ) ( 1 …` | Expande: `REST2` → `ε` |
| 106 | `) BODY $` | `) ( ( PI ) 2.0 * ) ( 1 …` | Casa: `)` |
| 107 | `BODY $` | `( ( PI ) 2.0 * ) ( 1 RES …` | Expande: `BODY` → `( BODY_TAIL` |
| 108 | `( BODY_TAIL $` | `( ( PI ) 2.0 * ) ( 1 RES …` | Casa: `(` |
| 109 | `BODY_TAIL $` | `( PI ) 2.0 * ) ( 1 RES ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 110 | `EXPR_BODY ) BODY $` | `( PI ) 2.0 * ) ( 1 RES ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 111 | `ITEM REST1 ) BODY $` | `( PI ) 2.0 * ) ( 1 RES ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 112 | `( EXPR_BODY ) REST1 ) BODY $` | `( PI ) 2.0 * ) ( 1 RES ) …` | Casa: `(` |
| 113 | `EXPR_BODY ) REST1 ) BODY $` | `PI ) 2.0 * ) ( 1 RES ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 114 | `ITEM REST1 ) REST1 ) BODY $` | `PI ) 2.0 * ) ( 1 RES ) ( …` | Expande: `ITEM` → `ident` |
| 115 | `ident REST1 ) REST1 ) BODY $` | `PI ) 2.0 * ) ( 1 RES ) ( …` | Casa: `ident` |
| 116 | `REST1 ) REST1 ) BODY $` | `) 2.0 * ) ( 1 RES ) ( ( …` | Expande: `REST1` → `ε` |
| 117 | `) REST1 ) BODY $` | `) 2.0 * ) ( 1 RES ) ( ( …` | Casa: `)` |
| 118 | `REST1 ) BODY $` | `2.0 * ) ( 1 RES ) ( ( PI …` | Expande: `REST1` → `ITEM REST2` |
| 119 | `ITEM REST2 ) BODY $` | `2.0 * ) ( 1 RES ) ( ( PI …` | Expande: `ITEM` → `numero` |
| 120 | `numero REST2 ) BODY $` | `2.0 * ) ( 1 RES ) ( ( PI …` | Casa: `numero` |
| 121 | `REST2 ) BODY $` | `* ) ( 1 RES ) ( ( PI ) …` | Expande: `REST2` → `BINOP` |
| 122 | `BINOP ) BODY $` | `* ) ( 1 RES ) ( ( PI ) …` | Expande: `BINOP` → `*` |
| 123 | `* ) BODY $` | `* ) ( 1 RES ) ( ( PI ) …` | Casa: `*` |
| 124 | `) BODY $` | `) ( 1 RES ) ( ( PI ) RAIO …` | Casa: `)` |
| 125 | `BODY $` | `( 1 RES ) ( ( PI ) RAIO ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 126 | `( BODY_TAIL $` | `( 1 RES ) ( ( PI ) RAIO ) …` | Casa: `(` |
| 127 | `BODY_TAIL $` | `1 RES ) ( ( PI ) RAIO ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 128 | `EXPR_BODY ) BODY $` | `1 RES ) ( ( PI ) RAIO ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 129 | `ITEM REST1 ) BODY $` | `1 RES ) ( ( PI ) RAIO ) ( …` | Expande: `ITEM` → `numero` |
| 130 | `numero REST1 ) BODY $` | `1 RES ) ( ( PI ) RAIO ) ( …` | Casa: `numero` |
| 131 | `REST1 ) BODY $` | `RES ) ( ( PI ) RAIO ) ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 132 | `ITEM REST2 ) BODY $` | `RES ) ( ( PI ) RAIO ) ( ( …` | Expande: `ITEM` → `res` |
| 133 | `res REST2 ) BODY $` | `RES ) ( ( PI ) RAIO ) ( ( …` | Casa: `res` |
| 134 | `REST2 ) BODY $` | `) ( ( PI ) RAIO ) ( ( ( …` | Expande: `REST2` → `ε` |
| 135 | `) BODY $` | `) ( ( PI ) RAIO ) ( ( ( …` | Casa: `)` |
| 136 | `BODY $` | `( ( PI ) RAIO ) ( ( ( RAIO …` | Expande: `BODY` → `( BODY_TAIL` |
| 137 | `( BODY_TAIL $` | `( ( PI ) RAIO ) ( ( ( RAIO …` | Casa: `(` |
| 138 | `BODY_TAIL $` | `( PI ) RAIO ) ( ( ( RAIO ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 139 | `EXPR_BODY ) BODY $` | `( PI ) RAIO ) ( ( ( RAIO ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 140 | `ITEM REST1 ) BODY $` | `( PI ) RAIO ) ( ( ( RAIO ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 141 | `( EXPR_BODY ) REST1 ) BODY $` | `( PI ) RAIO ) ( ( ( RAIO ) …` | Casa: `(` |
| 142 | `EXPR_BODY ) REST1 ) BODY $` | `PI ) RAIO ) ( ( ( RAIO ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 143 | `ITEM REST1 ) REST1 ) BODY $` | `PI ) RAIO ) ( ( ( RAIO ) ( …` | Expande: `ITEM` → `ident` |
| 144 | `ident REST1 ) REST1 ) BODY $` | `PI ) RAIO ) ( ( ( RAIO ) ( …` | Casa: `ident` |
| 145 | `REST1 ) REST1 ) BODY $` | `) RAIO ) ( ( ( RAIO ) ( PI …` | Expande: `REST1` → `ε` |
| 146 | `) REST1 ) BODY $` | `) RAIO ) ( ( ( RAIO ) ( PI …` | Casa: `)` |
| 147 | `REST1 ) BODY $` | `RAIO ) ( ( ( RAIO ) ( PI ) …` | Expande: `REST1` → `ITEM REST2` |
| 148 | `ITEM REST2 ) BODY $` | `RAIO ) ( ( ( RAIO ) ( PI ) …` | Expande: `ITEM` → `ident` |
| 149 | `ident REST2 ) BODY $` | `RAIO ) ( ( ( RAIO ) ( PI ) …` | Casa: `ident` |
| 150 | `REST2 ) BODY $` | `) ( ( ( RAIO ) ( PI ) * …` | Expande: `REST2` → `ε` |
| 151 | `) BODY $` | `) ( ( ( RAIO ) ( PI ) * …` | Casa: `)` |
| 152 | `BODY $` | `( ( ( RAIO ) ( PI ) * ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 153 | `( BODY_TAIL $` | `( ( ( RAIO ) ( PI ) * ) …` | Casa: `(` |
| 154 | `BODY_TAIL $` | `( ( RAIO ) ( PI ) * ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 155 | `EXPR_BODY ) BODY $` | `( ( RAIO ) ( PI ) * ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 156 | `ITEM REST1 ) BODY $` | `( ( RAIO ) ( PI ) * ) ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 157 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( RAIO ) ( PI ) * ) ( …` | Casa: `(` |
| 158 | `EXPR_BODY ) REST1 ) BODY $` | `( RAIO ) ( PI ) * ) ( RAIO …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 159 | `ITEM REST1 ) REST1 ) BODY $` | `( RAIO ) ( PI ) * ) ( RAIO …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 160 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( RAIO ) ( PI ) * ) ( RAIO …` | Casa: `(` |
| 161 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `RAIO ) ( PI ) * ) ( RAIO ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 162 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `RAIO ) ( PI ) * ) ( RAIO ) …` | Expande: `ITEM` → `ident` |
| 163 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `RAIO ) ( PI ) * ) ( RAIO ) …` | Casa: `ident` |
| 164 | `REST1 ) REST1 ) REST1 ) BODY $` | `) ( PI ) * ) ( RAIO ) * …` | Expande: `REST1` → `ε` |
| 165 | `) REST1 ) REST1 ) BODY $` | `) ( PI ) * ) ( RAIO ) * …` | Casa: `)` |
| 166 | `REST1 ) REST1 ) BODY $` | `( PI ) * ) ( RAIO ) * ) …` | Expande: `REST1` → `ITEM REST2` |
| 167 | `ITEM REST2 ) REST1 ) BODY $` | `( PI ) * ) ( RAIO ) * ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 168 | `( EXPR_BODY ) REST2 ) REST1 ) BODY $` | `( PI ) * ) ( RAIO ) * ) …` | Casa: `(` |
| 169 | `EXPR_BODY ) REST2 ) REST1 ) BODY $` | `PI ) * ) ( RAIO ) * ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 170 | `ITEM REST1 ) REST2 ) REST1 ) BODY $` | `PI ) * ) ( RAIO ) * ) ( …` | Expande: `ITEM` → `ident` |
| 171 | `ident REST1 ) REST2 ) REST1 ) BODY $` | `PI ) * ) ( RAIO ) * ) ( …` | Casa: `ident` |
| 172 | `REST1 ) REST2 ) REST1 ) BODY $` | `) * ) ( RAIO ) * ) ( ( …` | Expande: `REST1` → `ε` |
| 173 | `) REST2 ) REST1 ) BODY $` | `) * ) ( RAIO ) * ) ( ( …` | Casa: `)` |
| 174 | `REST2 ) REST1 ) BODY $` | `* ) ( RAIO ) * ) ( ( ( …` | Expande: `REST2` → `BINOP` |
| 175 | `BINOP ) REST1 ) BODY $` | `* ) ( RAIO ) * ) ( ( ( …` | Expande: `BINOP` → `*` |
| 176 | `* ) REST1 ) BODY $` | `* ) ( RAIO ) * ) ( ( ( …` | Casa: `*` |
| 177 | `) REST1 ) BODY $` | `) ( RAIO ) * ) ( ( ( RAIO …` | Casa: `)` |
| 178 | `REST1 ) BODY $` | `( RAIO ) * ) ( ( ( RAIO ) …` | Expande: `REST1` → `ITEM REST2` |
| 179 | `ITEM REST2 ) BODY $` | `( RAIO ) * ) ( ( ( RAIO ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 180 | `( EXPR_BODY ) REST2 ) BODY $` | `( RAIO ) * ) ( ( ( RAIO ) …` | Casa: `(` |
| 181 | `EXPR_BODY ) REST2 ) BODY $` | `RAIO ) * ) ( ( ( RAIO ) 0.0 …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 182 | `ITEM REST1 ) REST2 ) BODY $` | `RAIO ) * ) ( ( ( RAIO ) 0.0 …` | Expande: `ITEM` → `ident` |
| 183 | `ident REST1 ) REST2 ) BODY $` | `RAIO ) * ) ( ( ( RAIO ) 0.0 …` | Casa: `ident` |
| 184 | `REST1 ) REST2 ) BODY $` | `) * ) ( ( ( RAIO ) 0.0 > …` | Expande: `REST1` → `ε` |
| 185 | `) REST2 ) BODY $` | `) * ) ( ( ( RAIO ) 0.0 > …` | Casa: `)` |
| 186 | `REST2 ) BODY $` | `* ) ( ( ( RAIO ) 0.0 > ) …` | Expande: `REST2` → `BINOP` |
| 187 | `BINOP ) BODY $` | `* ) ( ( ( RAIO ) 0.0 > ) …` | Expande: `BINOP` → `*` |
| 188 | `* ) BODY $` | `* ) ( ( ( RAIO ) 0.0 > ) …` | Casa: `*` |
| 189 | `) BODY $` | `) ( ( ( RAIO ) 0.0 > ) ( …` | Casa: `)` |
| 190 | `BODY $` | `( ( ( RAIO ) 0.0 > ) ( ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 191 | `( BODY_TAIL $` | `( ( ( RAIO ) 0.0 > ) ( ( …` | Casa: `(` |
| 192 | `BODY_TAIL $` | `( ( RAIO ) 0.0 > ) ( ( RAIO …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 193 | `EXPR_BODY ) BODY $` | `( ( RAIO ) 0.0 > ) ( ( RAIO …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 194 | `ITEM REST1 ) BODY $` | `( ( RAIO ) 0.0 > ) ( ( RAIO …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 195 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( RAIO ) 0.0 > ) ( ( RAIO …` | Casa: `(` |
| 196 | `EXPR_BODY ) REST1 ) BODY $` | `( RAIO ) 0.0 > ) ( ( RAIO ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 197 | `ITEM REST1 ) REST1 ) BODY $` | `( RAIO ) 0.0 > ) ( ( RAIO ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 198 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( RAIO ) 0.0 > ) ( ( RAIO ) …` | Casa: `(` |
| 199 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `RAIO ) 0.0 > ) ( ( RAIO ) 0.5 …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 200 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `RAIO ) 0.0 > ) ( ( RAIO ) 0.5 …` | Expande: `ITEM` → `ident` |
| 201 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `RAIO ) 0.0 > ) ( ( RAIO ) 0.5 …` | Casa: `ident` |
| 202 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 0.0 > ) ( ( RAIO ) 0.5 \| …` | Expande: `REST1` → `ε` |
| 203 | `) REST1 ) REST1 ) BODY $` | `) 0.0 > ) ( ( RAIO ) 0.5 \| …` | Casa: `)` |
| 204 | `REST1 ) REST1 ) BODY $` | `0.0 > ) ( ( RAIO ) 0.5 \| ) …` | Expande: `REST1` → `ITEM REST2` |
| 205 | `ITEM REST2 ) REST1 ) BODY $` | `0.0 > ) ( ( RAIO ) 0.5 \| ) …` | Expande: `ITEM` → `numero` |
| 206 | `numero REST2 ) REST1 ) BODY $` | `0.0 > ) ( ( RAIO ) 0.5 \| ) …` | Casa: `numero` |
| 207 | `REST2 ) REST1 ) BODY $` | `> ) ( ( RAIO ) 0.5 \| ) IF …` | Expande: `REST2` → `BINOP` |
| 208 | `BINOP ) REST1 ) BODY $` | `> ) ( ( RAIO ) 0.5 \| ) IF …` | Expande: `BINOP` → `>` |
| 209 | `> ) REST1 ) BODY $` | `> ) ( ( RAIO ) 0.5 \| ) IF …` | Casa: `>` |
| 210 | `) REST1 ) BODY $` | `) ( ( RAIO ) 0.5 \| ) IF ) …` | Casa: `)` |
| 211 | `REST1 ) BODY $` | `( ( RAIO ) 0.5 \| ) IF ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 212 | `ITEM REST2 ) BODY $` | `( ( RAIO ) 0.5 \| ) IF ) ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 213 | `( EXPR_BODY ) REST2 ) BODY $` | `( ( RAIO ) 0.5 \| ) IF ) ( …` | Casa: `(` |
| 214 | `EXPR_BODY ) REST2 ) BODY $` | `( RAIO ) 0.5 \| ) IF ) ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 215 | `ITEM REST1 ) REST2 ) BODY $` | `( RAIO ) 0.5 \| ) IF ) ( ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 216 | `( EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( RAIO ) 0.5 \| ) IF ) ( ( …` | Casa: `(` |
| 217 | `EXPR_BODY ) REST1 ) REST2 ) BODY $` | `RAIO ) 0.5 \| ) IF ) ( ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 218 | `ITEM REST1 ) REST1 ) REST2 ) BODY $` | `RAIO ) 0.5 \| ) IF ) ( ( ( …` | Expande: `ITEM` → `ident` |
| 219 | `ident REST1 ) REST1 ) REST2 ) BODY $` | `RAIO ) 0.5 \| ) IF ) ( ( ( …` | Casa: `ident` |
| 220 | `REST1 ) REST1 ) REST2 ) BODY $` | `) 0.5 \| ) IF ) ( ( ( PI …` | Expande: `REST1` → `ε` |
| 221 | `) REST1 ) REST2 ) BODY $` | `) 0.5 \| ) IF ) ( ( ( PI …` | Casa: `)` |
| 222 | `REST1 ) REST2 ) BODY $` | `0.5 \| ) IF ) ( ( ( PI ) …` | Expande: `REST1` → `ITEM REST2` |
| 223 | `ITEM REST2 ) REST2 ) BODY $` | `0.5 \| ) IF ) ( ( ( PI ) …` | Expande: `ITEM` → `numero` |
| 224 | `numero REST2 ) REST2 ) BODY $` | `0.5 \| ) IF ) ( ( ( PI ) …` | Casa: `numero` |
| 225 | `REST2 ) REST2 ) BODY $` | `\| ) IF ) ( ( ( PI ) 3.0 …` | Expande: `REST2` → `BINOP` |
| 226 | `BINOP ) REST2 ) BODY $` | `\| ) IF ) ( ( ( PI ) 3.0 …` | Expande: `BINOP` → `\|` |
| 227 | `\| ) REST2 ) BODY $` | `\| ) IF ) ( ( ( PI ) 3.0 …` | Casa: `\|` |
| 228 | `) REST2 ) BODY $` | `) IF ) ( ( ( PI ) 3.0 > …` | Casa: `)` |
| 229 | `REST2 ) BODY $` | `IF ) ( ( ( PI ) 3.0 > ) …` | Expande: `REST2` → `KW_CTRL3` |
| 230 | `KW_CTRL3 ) BODY $` | `IF ) ( ( ( PI ) 3.0 > ) …` | Expande: `KW_CTRL3` → `if` |
| 231 | `if ) BODY $` | `IF ) ( ( ( PI ) 3.0 > ) …` | Casa: `if` |
| 232 | `) BODY $` | `) ( ( ( PI ) 3.0 > ) ( …` | Casa: `)` |
| 233 | `BODY $` | `( ( ( PI ) 3.0 > ) ( 1 …` | Expande: `BODY` → `( BODY_TAIL` |
| 234 | `( BODY_TAIL $` | `( ( ( PI ) 3.0 > ) ( 1 …` | Casa: `(` |
| 235 | `BODY_TAIL $` | `( ( PI ) 3.0 > ) ( 1 MAIOR …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 236 | `EXPR_BODY ) BODY $` | `( ( PI ) 3.0 > ) ( 1 MAIOR …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 237 | `ITEM REST1 ) BODY $` | `( ( PI ) 3.0 > ) ( 1 MAIOR …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 238 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( PI ) 3.0 > ) ( 1 MAIOR …` | Casa: `(` |
| 239 | `EXPR_BODY ) REST1 ) BODY $` | `( PI ) 3.0 > ) ( 1 MAIOR ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 240 | `ITEM REST1 ) REST1 ) BODY $` | `( PI ) 3.0 > ) ( 1 MAIOR ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 241 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( PI ) 3.0 > ) ( 1 MAIOR ) …` | Casa: `(` |
| 242 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `PI ) 3.0 > ) ( 1 MAIOR ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 243 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `PI ) 3.0 > ) ( 1 MAIOR ) ( …` | Expande: `ITEM` → `ident` |
| 244 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `PI ) 3.0 > ) ( 1 MAIOR ) ( …` | Casa: `ident` |
| 245 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 3.0 > ) ( 1 MAIOR ) ( 0 …` | Expande: `REST1` → `ε` |
| 246 | `) REST1 ) REST1 ) BODY $` | `) 3.0 > ) ( 1 MAIOR ) ( 0 …` | Casa: `)` |
| 247 | `REST1 ) REST1 ) BODY $` | `3.0 > ) ( 1 MAIOR ) ( 0 MAIOR …` | Expande: `REST1` → `ITEM REST2` |
| 248 | `ITEM REST2 ) REST1 ) BODY $` | `3.0 > ) ( 1 MAIOR ) ( 0 MAIOR …` | Expande: `ITEM` → `numero` |
| 249 | `numero REST2 ) REST1 ) BODY $` | `3.0 > ) ( 1 MAIOR ) ( 0 MAIOR …` | Casa: `numero` |
| 250 | `REST2 ) REST1 ) BODY $` | `> ) ( 1 MAIOR ) ( 0 MAIOR ) …` | Expande: `REST2` → `BINOP` |
| 251 | `BINOP ) REST1 ) BODY $` | `> ) ( 1 MAIOR ) ( 0 MAIOR ) …` | Expande: `BINOP` → `>` |
| 252 | `> ) REST1 ) BODY $` | `> ) ( 1 MAIOR ) ( 0 MAIOR ) …` | Casa: `>` |
| 253 | `) REST1 ) BODY $` | `) ( 1 MAIOR ) ( 0 MAIOR ) IFELSE …` | Casa: `)` |
| 254 | `REST1 ) BODY $` | `( 1 MAIOR ) ( 0 MAIOR ) IFELSE ) …` | Expande: `REST1` → `ITEM REST2` |
| 255 | `ITEM REST2 ) BODY $` | `( 1 MAIOR ) ( 0 MAIOR ) IFELSE ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 256 | `( EXPR_BODY ) REST2 ) BODY $` | `( 1 MAIOR ) ( 0 MAIOR ) IFELSE ) …` | Casa: `(` |
| 257 | `EXPR_BODY ) REST2 ) BODY $` | `1 MAIOR ) ( 0 MAIOR ) IFELSE ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 258 | `ITEM REST1 ) REST2 ) BODY $` | `1 MAIOR ) ( 0 MAIOR ) IFELSE ) ( …` | Expande: `ITEM` → `numero` |
| 259 | `numero REST1 ) REST2 ) BODY $` | `1 MAIOR ) ( 0 MAIOR ) IFELSE ) ( …` | Casa: `numero` |
| 260 | `REST1 ) REST2 ) BODY $` | `MAIOR ) ( 0 MAIOR ) IFELSE ) ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 261 | `ITEM REST2 ) REST2 ) BODY $` | `MAIOR ) ( 0 MAIOR ) IFELSE ) ( ( …` | Expande: `ITEM` → `ident` |
| 262 | `ident REST2 ) REST2 ) BODY $` | `MAIOR ) ( 0 MAIOR ) IFELSE ) ( ( …` | Casa: `ident` |
| 263 | `REST2 ) REST2 ) BODY $` | `) ( 0 MAIOR ) IFELSE ) ( ( ( …` | Expande: `REST2` → `ε` |
| 264 | `) REST2 ) BODY $` | `) ( 0 MAIOR ) IFELSE ) ( ( ( …` | Casa: `)` |
| 265 | `REST2 ) BODY $` | `( 0 MAIOR ) IFELSE ) ( ( ( MAIOR …` | Expande: `REST2` → `ITEM ITEM_TAIL` |
| 266 | `ITEM ITEM_TAIL ) BODY $` | `( 0 MAIOR ) IFELSE ) ( ( ( MAIOR …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 267 | `( EXPR_BODY ) ITEM_TAIL ) BODY $` | `( 0 MAIOR ) IFELSE ) ( ( ( MAIOR …` | Casa: `(` |
| 268 | `EXPR_BODY ) ITEM_TAIL ) BODY $` | `0 MAIOR ) IFELSE ) ( ( ( MAIOR ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 269 | `ITEM REST1 ) ITEM_TAIL ) BODY $` | `0 MAIOR ) IFELSE ) ( ( ( MAIOR ) …` | Expande: `ITEM` → `numero` |
| 270 | `numero REST1 ) ITEM_TAIL ) BODY $` | `0 MAIOR ) IFELSE ) ( ( ( MAIOR ) …` | Casa: `numero` |
| 271 | `REST1 ) ITEM_TAIL ) BODY $` | `MAIOR ) IFELSE ) ( ( ( MAIOR ) 0 …` | Expande: `REST1` → `ITEM REST2` |
| 272 | `ITEM REST2 ) ITEM_TAIL ) BODY $` | `MAIOR ) IFELSE ) ( ( ( MAIOR ) 0 …` | Expande: `ITEM` → `ident` |
| 273 | `ident REST2 ) ITEM_TAIL ) BODY $` | `MAIOR ) IFELSE ) ( ( ( MAIOR ) 0 …` | Casa: `ident` |
| 274 | `REST2 ) ITEM_TAIL ) BODY $` | `) IFELSE ) ( ( ( MAIOR ) 0 != …` | Expande: `REST2` → `ε` |
| 275 | `) ITEM_TAIL ) BODY $` | `) IFELSE ) ( ( ( MAIOR ) 0 != …` | Casa: `)` |
| 276 | `ITEM_TAIL ) BODY $` | `IFELSE ) ( ( ( MAIOR ) 0 != ) …` | Expande: `ITEM_TAIL` → `KW_CTRL4` |
| 277 | `KW_CTRL4 ) BODY $` | `IFELSE ) ( ( ( MAIOR ) 0 != ) …` | Expande: `KW_CTRL4` → `ifelse` |
| 278 | `ifelse ) BODY $` | `IFELSE ) ( ( ( MAIOR ) 0 != ) …` | Casa: `ifelse` |
| 279 | `) BODY $` | `) ( ( ( MAIOR ) 0 != ) ( …` | Casa: `)` |
| 280 | `BODY $` | `( ( ( MAIOR ) 0 != ) ( ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 281 | `( BODY_TAIL $` | `( ( ( MAIOR ) 0 != ) ( ( …` | Casa: `(` |
| 282 | `BODY_TAIL $` | `( ( MAIOR ) 0 != ) ( ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 283 | `EXPR_BODY ) BODY $` | `( ( MAIOR ) 0 != ) ( ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 284 | `ITEM REST1 ) BODY $` | `( ( MAIOR ) 0 != ) ( ( ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 285 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( MAIOR ) 0 != ) ( ( ( …` | Casa: `(` |
| 286 | `EXPR_BODY ) REST1 ) BODY $` | `( MAIOR ) 0 != ) ( ( ( MAIOR …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 287 | `ITEM REST1 ) REST1 ) BODY $` | `( MAIOR ) 0 != ) ( ( ( MAIOR …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 288 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( MAIOR ) 0 != ) ( ( ( MAIOR …` | Casa: `(` |
| 289 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `MAIOR ) 0 != ) ( ( ( MAIOR ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 290 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `MAIOR ) 0 != ) ( ( ( MAIOR ) …` | Expande: `ITEM` → `ident` |
| 291 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `MAIOR ) 0 != ) ( ( ( MAIOR ) …` | Casa: `ident` |
| 292 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 0 != ) ( ( ( MAIOR ) 1 …` | Expande: `REST1` → `ε` |
| 293 | `) REST1 ) REST1 ) BODY $` | `) 0 != ) ( ( ( MAIOR ) 1 …` | Casa: `)` |
| 294 | `REST1 ) REST1 ) BODY $` | `0 != ) ( ( ( MAIOR ) 1 - …` | Expande: `REST1` → `ITEM REST2` |
| 295 | `ITEM REST2 ) REST1 ) BODY $` | `0 != ) ( ( ( MAIOR ) 1 - …` | Expande: `ITEM` → `numero` |
| 296 | `numero REST2 ) REST1 ) BODY $` | `0 != ) ( ( ( MAIOR ) 1 - …` | Casa: `numero` |
| 297 | `REST2 ) REST1 ) BODY $` | `!= ) ( ( ( MAIOR ) 1 - ) …` | Expande: `REST2` → `BINOP` |
| 298 | `BINOP ) REST1 ) BODY $` | `!= ) ( ( ( MAIOR ) 1 - ) …` | Expande: `BINOP` → `!=` |
| 299 | `!= ) REST1 ) BODY $` | `!= ) ( ( ( MAIOR ) 1 - ) …` | Casa: `!=` |
| 300 | `) REST1 ) BODY $` | `) ( ( ( MAIOR ) 1 - ) MAIOR …` | Casa: `)` |
| 301 | `REST1 ) BODY $` | `( ( ( MAIOR ) 1 - ) MAIOR ) …` | Expande: `REST1` → `ITEM REST2` |
| 302 | `ITEM REST2 ) BODY $` | `( ( ( MAIOR ) 1 - ) MAIOR ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 303 | `( EXPR_BODY ) REST2 ) BODY $` | `( ( ( MAIOR ) 1 - ) MAIOR ) …` | Casa: `(` |
| 304 | `EXPR_BODY ) REST2 ) BODY $` | `( ( MAIOR ) 1 - ) MAIOR ) WHILE …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 305 | `ITEM REST1 ) REST2 ) BODY $` | `( ( MAIOR ) 1 - ) MAIOR ) WHILE …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 306 | `( EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( ( MAIOR ) 1 - ) MAIOR ) WHILE …` | Casa: `(` |
| 307 | `EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( MAIOR ) 1 - ) MAIOR ) WHILE ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 308 | `ITEM REST1 ) REST1 ) REST2 ) BODY $` | `( MAIOR ) 1 - ) MAIOR ) WHILE ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 309 | `( EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `( MAIOR ) 1 - ) MAIOR ) WHILE ) …` | Casa: `(` |
| 310 | `EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `MAIOR ) 1 - ) MAIOR ) WHILE ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 311 | `ITEM REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `MAIOR ) 1 - ) MAIOR ) WHILE ) ( …` | Expande: `ITEM` → `ident` |
| 312 | `ident REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `MAIOR ) 1 - ) MAIOR ) WHILE ) ( …` | Casa: `ident` |
| 313 | `REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `) 1 - ) MAIOR ) WHILE ) ( END …` | Expande: `REST1` → `ε` |
| 314 | `) REST1 ) REST1 ) REST2 ) BODY $` | `) 1 - ) MAIOR ) WHILE ) ( END …` | Casa: `)` |
| 315 | `REST1 ) REST1 ) REST2 ) BODY $` | `1 - ) MAIOR ) WHILE ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 316 | `ITEM REST2 ) REST1 ) REST2 ) BODY $` | `1 - ) MAIOR ) WHILE ) ( END )` | Expande: `ITEM` → `numero` |
| 317 | `numero REST2 ) REST1 ) REST2 ) BODY $` | `1 - ) MAIOR ) WHILE ) ( END )` | Casa: `numero` |
| 318 | `REST2 ) REST1 ) REST2 ) BODY $` | `- ) MAIOR ) WHILE ) ( END )` | Expande: `REST2` → `BINOP` |
| 319 | `BINOP ) REST1 ) REST2 ) BODY $` | `- ) MAIOR ) WHILE ) ( END )` | Expande: `BINOP` → `-` |
| 320 | `- ) REST1 ) REST2 ) BODY $` | `- ) MAIOR ) WHILE ) ( END )` | Casa: `-` |
| 321 | `) REST1 ) REST2 ) BODY $` | `) MAIOR ) WHILE ) ( END )` | Casa: `)` |
| 322 | `REST1 ) REST2 ) BODY $` | `MAIOR ) WHILE ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 323 | `ITEM REST2 ) REST2 ) BODY $` | `MAIOR ) WHILE ) ( END )` | Expande: `ITEM` → `ident` |
| 324 | `ident REST2 ) REST2 ) BODY $` | `MAIOR ) WHILE ) ( END )` | Casa: `ident` |
| 325 | `REST2 ) REST2 ) BODY $` | `) WHILE ) ( END )` | Expande: `REST2` → `ε` |
| 326 | `) REST2 ) BODY $` | `) WHILE ) ( END )` | Casa: `)` |
| 327 | `REST2 ) BODY $` | `WHILE ) ( END )` | Expande: `REST2` → `KW_CTRL3` |
| 328 | `KW_CTRL3 ) BODY $` | `WHILE ) ( END )` | Expande: `KW_CTRL3` → `while` |
| 329 | `while ) BODY $` | `WHILE ) ( END )` | Casa: `while` |
| 330 | `) BODY $` | `) ( END )` | Casa: `)` |
| 331 | `BODY $` | `( END )` | Expande: `BODY` → `( BODY_TAIL` |
| 332 | `( BODY_TAIL $` | `( END )` | Casa: `(` |
| 333 | `BODY_TAIL $` | `END )` | Expande: `BODY_TAIL` → `end )` |
| 334 | `end ) $` | `END )` | Casa: `end` |
| 335 | `) $` | `)` | Casa: `)` |
| 336 | `$` | `$` | Casa: `$` |
