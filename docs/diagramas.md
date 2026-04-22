# Diagramas do Projeto — RA2 9 (Fase 2)

Este arquivo reúne os diagramas em **Mermaid** que ajudam a entender a
arquitetura, o fluxo de dados e a execução do analisador sintático LL(1).
Todos podem ser visualizados diretamente no GitHub ou no VS Code com a
extensão *Markdown Preview Mermaid Support*.

> Sumário rápido: [Pipeline](#1-pipeline-end-to-end-fluxograma) ·
> [Módulos](#2-arquitetura-de-módulos-relação-entre-arquivos) ·
> [Construção da gramática](#3-construirgramatica--first--follow--tabela) ·
> [Parser LL(1)](#4-parser-ll1-com-pilha-passo-a-passo) ·
> [AFD da Fase 1](#5-afd-do-lexer-fase-1) ·
> [Estruturas de controle](#6-estruturas-de-controle-state-diagram) ·
> [AST](#7-tipos-de-nó-da-ast-classes) ·
> [Sequência completa](#8-sequência-completa-de-uma-execução)

---

## 1. Pipeline end-to-end (fluxograma)

Visão macro do que acontece ao executar `python main.py teste1.txt`.

```mermaid
flowchart LR
    A[("teste1.txt")] --> B["lerArquivo()"]
    B --> C["tokenizar_linha()<br/>(AFD da Fase 1)"]
    C --> D[("output/tokens_<br/>ultima_execucao.txt")]
    D --> E["lerTokens()"]
    F["construirGramatica()<br/>FIRST · FOLLOW · Tabela"] --> G
    E --> G["parsear()<br/>(LL(1) com pilha)"]
    G --> H["gerarArvore()"]
    H --> I[("arvore_ultima_execucao.json<br/>+ arvore_ultima_execucao.md")]
    H --> J["gerarAssembly()"]
    J --> K[("output/ultima_execucao.s")]
    H --> L["exibirResultados()"]
    L --> M(["console"])
    F --> N[("gramatica_dump.md")]
    G --> O[("derivacao_ultima_execucao.md")]

    classDef io fill:#fef3c7,stroke:#d97706
    classDef step fill:#dbeafe,stroke:#1d4ed8
    class A,D,I,K,N,O io
    class B,C,E,G,H,J,L,F step
```

---

## 2. Arquitetura de módulos (relação entre arquivos)

```mermaid
flowchart TB
    subgraph CLI
        main["main.py"]
    end

    subgraph src
        pipe["pipeline.py<br/><i>funções obrigatórias</i>"]
        lex["lexer_fsm.py<br/><i>AFD + Token + Erros</i>"]
        par["parser_ll1.py<br/><i>gramática + parser + AST</i>"]
        gen["armv7_generator.py<br/><i>Assembly ARMv7</i>"]
    end

    subgraph docs
        gram["gramatica.md"]
        diag["docs/diagramas.md"]
    end

    main --> pipe
    pipe --> lex
    pipe --> par
    pipe --> gen
    par  --> lex
    gen  --> par
    main --> gram
```

---

## 3. `construirGramatica()` — FIRST → FOLLOW → Tabela

Como a estrutura de dados retornada por `construirGramatica()` é montada.

```mermaid
flowchart LR
    R[("Regras de produção<br/>(31 produções)")] --> F1["calcularFIRST()"]
    F1 --> F2["calcularFOLLOW()"]
    F2 --> T["construirTabelaLL1()"]
    T -->|sem conflitos| OK[("dict {regras, FIRST,<br/>FOLLOW, tabela}")]
    T -->|conflito| ERR(["Erros('Conflito LL(1) ...')"])

    classDef ok fill:#dcfce7,stroke:#16a34a
    classDef err fill:#fee2e2,stroke:#dc2626
    class OK ok
    class ERR err
```

---

## 4. Parser LL(1) com pilha (passo a passo)

Algoritmo executado por `parsear(tokens, gram)`.

```mermaid
flowchart TD
    A([Início]) --> B["pilha = ['program', '$']<br/>buffer = tokens + ['$']"]
    B --> C{"topo == '$' ?"}
    C -- sim --> D{"token == '$' ?"}
    D -- sim --> OK([aceita])
    D -- não --> E1(["erro: tokens sobrando"])
    C -- não --> F{"topo é<br/>terminal?"}
    F -- sim --> G{"casa com<br/>token corrente?"}
    G -- sim --> H["consome token<br/>desempilha topo"]
    H --> C
    G -- não --> E2(["erro sintático<br/>(esperado X, achou Y)"])
    F -- não --> I["consulta tabela[A][a]"]
    I --> J{"existe<br/>produção?"}
    J -- não --> E3(["erro sintático"])
    J -- sim --> K["registra regra<br/>na derivação"]
    K --> L["empilha lado<br/>direito invertido"]
    L --> C

    classDef err fill:#fee2e2,stroke:#dc2626
    classDef ok  fill:#dcfce7,stroke:#16a34a
    class E1,E2,E3 err
    class OK ok
```

---

## 5. AFD do lexer (Fase 1)

Diagrama dos 5 estados que continuam em uso na Fase 2 (com a adição dos
operadores relacionais e das keywords `IF`, `IFELSE`, `WHILE`, `START`, `END`).

```mermaid
stateDiagram-v2
    [*] --> inicial

    inicial --> inicial: ws<br/>( )<br/>+ - * % ^ \|
    inicial --> numero: dígito
    inicial --> identificador: A-Z
    inicial --> barra: /
    inicial --> rel: > < = !
    inicial --> ERRO: caractere inválido

    numero --> numero: dígito
    numero --> numero_decimal: .
    numero --> inicial: outro<br/>(emite NUMERO)

    numero_decimal --> numero_decimal: dígito
    numero_decimal --> inicial: outro<br/>(emite NUMERO)
    numero_decimal --> ERRO: . ou letra

    identificador --> identificador: A-Z
    identificador --> inicial: outro<br/>(emite IDENT/KEYWORD)
    identificador --> ERRO: a-z ou dígito

    barra --> inicial: / (emite //)
    barra --> inicial: outro (emite /)

    rel --> inicial: '=' (emite >= <= == !=)
    rel --> inicial: outro (emite > < ou erro p/ '!')
```

---

## 6. Estruturas de controle (state diagram)

Como o parser interpreta cada construção depois que a AST é montada.

### 6.1. IF / IFELSE

```mermaid
stateDiagram-v2
    [*] --> avalia_cond
    avalia_cond --> exec_then: cond ≠ 0
    avalia_cond --> exec_else: cond == 0 (apenas IFELSE)
    avalia_cond --> [*]: cond == 0 (IF)
    exec_then --> [*]
    exec_else --> [*]
```

### 6.2. WHILE

```mermaid
stateDiagram-v2
    [*] --> avalia_cond
    avalia_cond --> exec_body: cond ≠ 0
    avalia_cond --> [*]:    cond == 0
    exec_body --> avalia_cond
```

---

## 7. Tipos de nó da AST (classes)

Estrutura dos `dict`s produzidos por `gerarArvore()`. Útil para quem for
consumir `output/arvore_ultima_execucao.json`.

```mermaid
classDiagram
    class Program {
        +string tipo = "program"
        +Stmt[] stmts
    }
    class Binary {
        +string tipo = "binary"
        +string op
        +Node esq
        +Node dir
    }
    class Number {
        +string tipo = "number"
        +float valor
    }
    class MemRead {
        +string tipo = "mem_read"
        +string nome
    }
    class MemWrite {
        +string tipo = "mem_write"
        +string nome
        +Node expr
    }
    class ResRef {
        +string tipo = "res_ref"
        +int linhas_atras
    }
    class If {
        +string tipo = "if"
        +Node cond
        +Node then
    }
    class IfElse {
        +string tipo = "ifelse"
        +Node cond
        +Node then
        +Node else_
    }
    class While {
        +string tipo = "while"
        +Node cond
        +Node body
    }

    Program "1" o-- "*" Binary
    Program "1" o-- "*" Number
    Program "1" o-- "*" MemRead
    Program "1" o-- "*" MemWrite
    Program "1" o-- "*" ResRef
    Program "1" o-- "*" If
    Program "1" o-- "*" IfElse
    Program "1" o-- "*" While
```

---

## 8. Sequência completa de uma execução

Interação entre os principais módulos quando o usuário roda
`python main.py teste1.txt`.

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant M as main.py
    participant P as pipeline.py
    participant L as lexer_fsm.py
    participant G as parser_ll1.py
    participant A as armv7_generator.py
    participant FS as Sistema de arquivos

    U->>M: python main.py teste1.txt
    M->>P: executar_fase2(...)
    P->>FS: lerArquivo("teste1.txt")
    FS-->>P: linhas[]
    P->>L: tokenizar_linha(linha) ×N
    L-->>P: Token[]
    P->>FS: salvarTokens(tokens, "tokens_...txt")
    P->>FS: lerTokens("tokens_...txt")
    FS-->>P: Token[] (round-trip)
    P->>G: construirGramatica()
    G-->>P: {regras, FIRST, FOLLOW, tabela}
    P->>G: parsear(tokens, gram)
    G-->>P: {derivacao, tokens}
    P->>G: gerarArvore(resultado)
    G-->>P: ast (dict "program")
    P->>FS: salvar arvore.json + arvore.md
    P->>A: gerarAssembly(ast)
    A-->>P: string ".s"
    P->>FS: salvar ultima_execucao.s
    P-->>M: resultado
    M->>FS: salvar gramatica_dump.md
    M->>FS: salvar derivacao_ultima_execucao.md
    M->>U: imprime resumo + árvore
```

---

## 9. Como atualizar este documento

Sempre que a gramática, o parser ou a AST mudarem:

1. Atualize o(s) diagrama(s) afetado(s) neste arquivo.
2. Rode `python main.py teste1.txt` para regenerar todos os artefatos em `output/`
   (inclui `gramatica_dump.md`, `derivacao_ultima_execucao.md`, `arvore_ultima_execucao.json/.md`).
3. Rode `python -m pytest tests/ -q` para garantir que os 37 testes continuam passando.
