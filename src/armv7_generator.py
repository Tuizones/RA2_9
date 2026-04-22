# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA2 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Gerador de código Assembly ARMv7 para o CPUlator DE1-SoC.
# Recebe a AST produzida por parser_ll1.gerarArvore() e percorre
# recursivamente cada nó, emitindo instruções ARM.
#
# Estratégia: pilha de variáveis duplas (d-registers, VFPv3)
#   todos os valores são tratados como double (IEEE 754 64-bit)
#   operações empilham o resultado em d0 e usam VMOV+PUSH para salvar
#
# Operadores suportados:
#   +, -, *  -> VADD/VSUB/VMUL.F64
#   |        -> VDIV.F64 (divisão real)
#   /        -> __op_idiv (divisão inteira via rotina auxiliar)
#   %        -> __op_mod
#   ^        -> __op_pow (expoente inteiro por multiplicações sucessivas)
#   >, <, ==, !=, >=, <= -> VCMP.F64 + desvio condicional -> empilha 1.0 ou 0.0
#
# Estruturas de controle:
#   IF    -> testa condição e desvia sobre o bloco se falso
#   IFELSE-> dois rótulos (else + fim), executa um dos dois ramos
#   WHILE -> rótulo de início + rótulo de saída, desvio condicional


def _normalizar_nome_mem(nome: str) -> str:
    return nome.lower()


def _coletar_memorias(no: dict, memorias: set[str]) -> None:
    tipo = no["tipo"]
    if tipo == "program":
        for s in no["stmts"]:
            _coletar_memorias(s, memorias)
        return
    if tipo == "mem_write":
        memorias.add(_normalizar_nome_mem(no["nome"]))
        _coletar_memorias(no["valor"], memorias)
        return
    if tipo == "mem_read":
        memorias.add(_normalizar_nome_mem(no["nome"]))
        return
    if tipo == "binary":
        _coletar_memorias(no["esq"], memorias)
        _coletar_memorias(no["dir"], memorias)
        return
    if tipo == "if":
        _coletar_memorias(no["cond"], memorias)
        _coletar_memorias(no["then_block"], memorias)
        return
    if tipo == "ifelse":
        _coletar_memorias(no["cond"], memorias)
        _coletar_memorias(no["then_block"], memorias)
        _coletar_memorias(no["else_block"], memorias)
        return
    if tipo == "while":
        _coletar_memorias(no["cond"], memorias)
        _coletar_memorias(no["body"], memorias)
        return


def _emit_push_d0(linhas: list[str]) -> None:
    linhas.append("    VMOV r4, r5, d0")
    linhas.append("    PUSH {r4, r5}")


def _emit_pop_para_d(linhas: list[str], reg_d: str) -> None:
    linhas.append("    POP {r4, r5}")
    linhas.append(f"    VMOV {reg_d}, r4, r5")


def _novo_rotulo(ctx: dict, base: str) -> str:
    ctx["contador_rotulos"] += 1
    return f"L_{base}_{ctx['contador_rotulos']}"


def _emit_expressao(no: dict, linhas: list[str], ctx: dict) -> None:
    tipo = no["tipo"]

    if tipo == "number":
        valor = no["valor"]
        mapa = ctx["constantes"]
        if valor not in mapa:
            rotulo = f"const_{ctx['contador_const'][0]}"
            mapa[valor] = rotulo
            ctx["contador_const"][0] += 1
        else:
            rotulo = mapa[valor]
        linhas.append(f"    LDR r0, ={rotulo}")
        linhas.append("    VLDR.F64 d0, [r0]")
        _emit_push_d0(linhas)
        return

    if tipo == "mem_read":
        mem = _normalizar_nome_mem(no["nome"])
        linhas.append(f"    LDR r0, =mem_{mem}")
        linhas.append("    VLDR.F64 d0, [r0]")
        _emit_push_d0(linhas)
        return

    if tipo == "res_ref":
        alvo = ctx["indice_linha"] - no["linhas_atras"]
        if alvo < 0:
            alvo = 0
        linhas.append(f"    LDR r0, =resultado_{alvo}")
        linhas.append("    VLDR.F64 d0, [r0]")
        _emit_push_d0(linhas)
        return

    if tipo == "mem_write":
        _emit_expressao(no["valor"], linhas, ctx)
        _emit_pop_para_d(linhas, "d0")
        mem = _normalizar_nome_mem(no["nome"])
        linhas.append(f"    LDR r0, =mem_{mem}")
        linhas.append("    VSTR.F64 d0, [r0]")
        _emit_push_d0(linhas)
        return

    if tipo == "binary":
        _emit_binario(no, linhas, ctx)
        return

    if tipo == "if":
        _emit_if(no, linhas, ctx)
        return
    if tipo == "ifelse":
        _emit_ifelse(no, linhas, ctx)
        return
    if tipo == "while":
        _emit_while(no, linhas, ctx)
        return

    raise ValueError(f"Nó inválido: {tipo}")


def _emit_binario(no: dict, linhas: list[str], ctx: dict) -> None:
    _emit_expressao(no["esq"], linhas, ctx)
    _emit_expressao(no["dir"], linhas, ctx)
    _emit_pop_para_d(linhas, "d1")
    _emit_pop_para_d(linhas, "d0")

    op = no["op"]

    if op == "+":
        linhas.append("    VADD.F64 d0, d0, d1")
    elif op == "-":
        linhas.append("    VSUB.F64 d0, d0, d1")
    elif op == "*":
        linhas.append("    VMUL.F64 d0, d0, d1")
    elif op == "|":
        linhas.append("    VDIV.F64 d0, d0, d1")
    elif op == "/":
        linhas.append("    BL __op_idiv")
    elif op == "%":
        linhas.append("    BL __op_mod")
    elif op == "^":
        linhas.append("    BL __op_pow")
    elif op in (">", "<", "==", "!=", ">=", "<="):
        _emit_comparacao(op, linhas, ctx)
    else:
        raise ValueError(f"Operador não suportado: {op}")

    _emit_push_d0(linhas)


def _emit_comparacao(op: str, linhas: list[str], ctx: dict) -> None:
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")

    rotulo_true = _novo_rotulo(ctx, "cmp_t")
    rotulo_end = _novo_rotulo(ctx, "cmp_e")

    if op == ">":
        linhas.append(f"    BGT {rotulo_true}")
    elif op == "<":
        linhas.append(f"    BLT {rotulo_true}")
    elif op == ">=":
        linhas.append(f"    BGE {rotulo_true}")
    elif op == "<=":
        linhas.append(f"    BLE {rotulo_true}")
    elif op == "==":
        linhas.append(f"    BEQ {rotulo_true}")
    elif op == "!=":
        linhas.append(f"    BNE {rotulo_true}")

    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d0, [r0]")
    linhas.append(f"    B {rotulo_end}")
    linhas.append(f"{rotulo_true}:")
    linhas.append("    LDR r0, =const_one")
    linhas.append("    VLDR.F64 d0, [r0]")
    linhas.append(f"{rotulo_end}:")


def _emit_cond_valor(no: dict, linhas: list[str], ctx: dict) -> None:
    _emit_expressao(no, linhas, ctx)


def _emit_if(no: dict, linhas: list[str], ctx: dict) -> None:
    rotulo_fim = _novo_rotulo(ctx, "if_fim")
    _emit_cond_valor(no["cond"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")
    linhas.append(f"    BEQ {rotulo_fim}")
    _emit_expressao(no["then_block"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append(f"{rotulo_fim}:")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d0, [r0]")
    _emit_push_d0(linhas)


def _emit_ifelse(no: dict, linhas: list[str], ctx: dict) -> None:
    rotulo_else = _novo_rotulo(ctx, "else")
    rotulo_fim = _novo_rotulo(ctx, "ife_fim")
    _emit_cond_valor(no["cond"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")
    linhas.append(f"    BEQ {rotulo_else}")
    _emit_expressao(no["then_block"], linhas, ctx)
    linhas.append(f"    B {rotulo_fim}")
    linhas.append(f"{rotulo_else}:")
    _emit_expressao(no["else_block"], linhas, ctx)
    linhas.append(f"{rotulo_fim}:")


def _emit_while(no: dict, linhas: list[str], ctx: dict) -> None:
    rotulo_ini = _novo_rotulo(ctx, "while_i")
    rotulo_fim = _novo_rotulo(ctx, "while_f")
    linhas.append(f"{rotulo_ini}:")
    _emit_cond_valor(no["cond"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d1, [r0]")
    linhas.append("    VCMP.F64 d0, d1")
    linhas.append("    VMRS APSR_nzcv, FPSCR")
    linhas.append(f"    BEQ {rotulo_fim}")
    _emit_expressao(no["body"], linhas, ctx)
    _emit_pop_para_d(linhas, "d0")
    linhas.append(f"    B {rotulo_ini}")
    linhas.append(f"{rotulo_fim}:")
    linhas.append("    LDR r0, =const_zero")
    linhas.append("    VLDR.F64 d0, [r0]")
    _emit_push_d0(linhas)


def gerar_assembly_arvore(arvore_programa: dict) -> str:
    if arvore_programa.get("tipo") != "program":
        raise ValueError("Raiz da AST deve ser do tipo 'program'")
    stmts = arvore_programa["stmts"]

    memorias: set[str] = set()
    _coletar_memorias(arvore_programa, memorias)

    ctx = {
        "constantes": {},
        "contador_const": [0],
        "contador_rotulos": 0,
        "indice_linha": 0,
    }

    linhas: list[str] = []
    linhas.append(".syntax unified")
    linhas.append(".cpu cortex-a9")
    linhas.append(".fpu vfpv3")
    linhas.append(".global _start")
    linhas.append("")
    linhas.append(".text")
    linhas.append("_start:")

    for indice, stmt in enumerate(stmts):
        ctx["indice_linha"] = indice
        linhas.append(f"    @ Expressão {indice + 1}")
        _emit_expressao(stmt, linhas, ctx)
        _emit_pop_para_d(linhas, "d0")
        linhas.append(f"    LDR r0, =resultado_{indice}")
        linhas.append("    VSTR.F64 d0, [r0]")
        linhas.append(f"    @ Exibir resultado {indice + 1} nos HEX displays")
        linhas.append("    VCVT.S32.F64 s0, d0")
        linhas.append("    VMOV r0, s0")
        linhas.append("    BL __exibir_hex")

    linhas.append("")
    linhas.append("loop_final:")
    linhas.append("    B loop_final")

    linhas.extend(_rotinas_auxiliares())

    linhas.append(".data")
    for valor, rotulo in ctx["constantes"].items():
        linhas.append(f"{rotulo}: .double {valor}")
    linhas.append("const_zero: .double 0.0")
    linhas.append("const_one:  .double 1.0")
    for mem in sorted(memorias):
        linhas.append(f"mem_{mem}: .double 0.0")
    for indice in range(len(stmts)):
        linhas.append(f"resultado_{indice}: .double 0.0")
    if not stmts:
        linhas.append("resultado_0: .double 0.0")

    linhas.append("")
    linhas.append("@ Tabela 7-segmentos (0-9) para display HEX")
    linhas.append("__hex_tabela:")
    for byte, digito in zip(
        ("0x3F", "0x06", "0x5B", "0x4F", "0x66", "0x6D", "0x7D", "0x07", "0x7F", "0x6F"),
        range(10),
    ):
        linhas.append(f"    .byte {byte}  @ {digito}")

    return "\n".join(linhas) + "\n"


def _rotinas_auxiliares() -> list[str]:
    linhas: list[str] = []
    linhas.append("")
    linhas.append("__op_idiv:")
    linhas.append("    PUSH {lr}")
    linhas.append("    VCVT.S32.F64 s0, d0")
    linhas.append("    VCVT.S32.F64 s2, d1")
    linhas.append("    VMOV r0, s0")
    linhas.append("    VMOV r1, s2")
    linhas.append("    BL __sdiv32")
    linhas.append("    VMOV s0, r0")
    linhas.append("    VCVT.F64.S32 d0, s0")
    linhas.append("    POP {lr}")
    linhas.append("    BX lr")
    linhas.append("")
    linhas.append("__op_mod:")
    linhas.append("    PUSH {r4, lr}")
    linhas.append("    VCVT.S32.F64 s0, d0")
    linhas.append("    VCVT.S32.F64 s2, d1")
    linhas.append("    VMOV r2, s0")
    linhas.append("    VMOV r3, s2")
    linhas.append("    MOV r0, r2")
    linhas.append("    MOV r1, r3")
    linhas.append("    BL __sdiv32")
    linhas.append("    MUL r4, r0, r3")
    linhas.append("    SUB r2, r2, r4")
    linhas.append("    VMOV s0, r2")
    linhas.append("    VCVT.F64.S32 d0, s0")
    linhas.append("    POP {r4, lr}")
    linhas.append("    BX lr")
    linhas.append("")
    linhas.append("__op_pow:")
    linhas.append("    PUSH {lr}")
    linhas.append("    VCVT.S32.F64 s2, d1")
    linhas.append("    VMOV r3, s2")
    linhas.append("    CMP r3, #0")
    linhas.append("    BLE __pow_zero_ou_negativo")
    linhas.append("    VMOV.F64 d2, d0")
    linhas.append("    SUB r3, r3, #1")
    linhas.append("__pow_loop:")
    linhas.append("    CMP r3, #0")
    linhas.append("    BEQ __pow_done")
    linhas.append("    VMUL.F64 d2, d2, d0")
    linhas.append("    SUB r3, r3, #1")
    linhas.append("    B __pow_loop")
    linhas.append("__pow_done:")
    linhas.append("    VMOV.F64 d0, d2")
    linhas.append("    POP {lr}")
    linhas.append("    BX lr")
    linhas.append("__pow_zero_ou_negativo:")
    linhas.append("    LDR r0, =const_one")
    linhas.append("    VLDR.F64 d0, [r0]")
    linhas.append("    POP {lr}")
    linhas.append("    BX lr")
    linhas.append("")
    linhas.append("__sdiv32:")
    linhas.append("    PUSH {r2, r3, r4, lr}")
    linhas.append("    CMP r1, #0")
    linhas.append("    BEQ __sdiv32_divzero")
    linhas.append("    MOV r2, #0")
    linhas.append("    CMP r0, #0")
    linhas.append("    RSBMI r0, r0, #0")
    linhas.append("    EORMI r2, r2, #1")
    linhas.append("    CMP r1, #0")
    linhas.append("    RSBMI r1, r1, #0")
    linhas.append("    EORMI r2, r2, #1")
    linhas.append("    MOV r3, #0")
    linhas.append("__sdiv32_loop:")
    linhas.append("    CMP r0, r1")
    linhas.append("    BLT __sdiv32_done")
    linhas.append("    SUB r0, r0, r1")
    linhas.append("    ADD r3, r3, #1")
    linhas.append("    B __sdiv32_loop")
    linhas.append("__sdiv32_done:")
    linhas.append("    CMP r2, #0")
    linhas.append("    RSBNE r3, r3, #0")
    linhas.append("    MOV r0, r3")
    linhas.append("    POP {r2, r3, r4, lr}")
    linhas.append("    BX lr")
    linhas.append("__sdiv32_divzero:")
    linhas.append("    MOV r0, #0")
    linhas.append("    POP {r2, r3, r4, lr}")
    linhas.append("    BX lr")
    linhas.append("")
    linhas.append("__exibir_hex:")
    linhas.append("    PUSH {r1, r2, r3, r4, r5, r6, lr}")
    linhas.append("    LDR r1, =__hex_tabela")
    linhas.append("    LDR r6, =0xFF200020")
    linhas.append("    MOV r5, #0")
    linhas.append("    CMP r0, #0")
    linhas.append("    RSBMI r0, r0, #0")
    linhas.append("    MOVMI r5, #1")
    linhas.append("    MOV r4, #0")
    linhas.append("    MOV r2, #10")
    linhas.append("    BL __udiv_simples")
    linhas.append("    LDRB r3, [r1, r3]")
    linhas.append("    ORR r4, r4, r3")
    linhas.append("    MOV r2, #10")
    linhas.append("    BL __udiv_simples")
    linhas.append("    LDRB r3, [r1, r3]")
    linhas.append("    ORR r4, r4, r3, LSL #8")
    linhas.append("    MOV r2, #10")
    linhas.append("    BL __udiv_simples")
    linhas.append("    LDRB r3, [r1, r3]")
    linhas.append("    ORR r4, r4, r3, LSL #16")
    linhas.append("    CMP r5, #1")
    linhas.append("    MOVEQ r3, #0x40")
    linhas.append("    BEQ __exibir_hex_store")
    linhas.append("    MOV r2, #10")
    linhas.append("    BL __udiv_simples")
    linhas.append("    LDRB r3, [r1, r3]")
    linhas.append("    ORR r4, r4, r3, LSL #24")
    linhas.append("    B __exibir_hex_fim")
    linhas.append("__exibir_hex_store:")
    linhas.append("    ORR r4, r4, r3, LSL #24")
    linhas.append("__exibir_hex_fim:")
    linhas.append("    STR r4, [r6]")
    linhas.append("    POP {r1, r2, r3, r4, r5, r6, lr}")
    linhas.append("    BX lr")
    linhas.append("")
    linhas.append("__udiv_simples:")
    linhas.append("    MOV r3, #0")
    linhas.append("__udiv_simples_loop:")
    linhas.append("    CMP r0, r2")
    linhas.append("    BLT __udiv_simples_done")
    linhas.append("    SUB r0, r0, r2")
    linhas.append("    ADD r3, r3, #1")
    linhas.append("    B __udiv_simples_loop")
    linhas.append("__udiv_simples_done:")
    linhas.append("    MOV r12, r0")
    linhas.append("    MOV r0, r3")
    linhas.append("    MOV r3, r12")
    linhas.append("    BX lr")
    linhas.append("")
    return linhas


# Compatibilidade: assinatura usada internamente pelo pipeline da Fase 2
gerarAssembly = gerar_assembly_arvore
