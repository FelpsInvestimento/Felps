from supervisora.ia_supervisora import ia_supervisora_aprova
from painel.configuracoes import get_modo_operacao, get_stop_global, get_saldo_disponivel

def verificar_protecao(ia_id, ativo, acao, valor):
    saldo = get_saldo_disponivel()
    stop_global = get_stop_global()
    modo = get_modo_operacao()

    if valor > saldo:
        print(f"[{ia_id}] ❌ Valor excede o saldo disponível.")
        return False

    if stop_global['ativo'] and stop_global['atingido']:
        print(f"[{ia_id}] ⚠️ Stop Global ATIVADO. Operações bloqueadas.")
        return False

    if not ia_supervisora_aprova(ia_id, ativo, acao, valor, modo):
        print(f"[{ia_id}] ❌ Operação não aprovada pela IA Supervisora.")
        return False

    # Segurança adicional: bloquear valor muito alto em modo leve
    if modo == 'leve' and valor > saldo * 0.1:
        print(f"[{ia_id}] ⚠️ Valor alto demais para o modo Leve.")
        return False

    return True
