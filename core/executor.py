import threading
from core.protection import verificar_protecao
from core.relatorio import registrar_operacao
from database.novadax_api import comprar_ativo, vender_ativo

def executar_operacao(ia_id, ativo, acao, valor, confianca):
    if not verificar_protecao(ia_id, ativo, acao, valor):
        print(f"[{ia_id}] Operação BLOQUEADA pelo sistema de proteção.")
        return False

    print(f"[{ia_id}] Executando: {acao.upper()} {valor} em {ativo} (Confiança: {confianca}%)")

    try:
        if acao == 'comprar':
            resposta = comprar_ativo(ativo, valor)
        elif acao == 'vender':
            resposta = vender_ativo(ativo, valor)
        else:
            print(f"[{ia_id}] Ação desconhecida: {acao}")
            return False
    except Exception as e:
        print(f"[{ia_id}] ERRO ao executar operação: {e}")
        return False

    registrar_operacao(ia_id, ativo, acao, valor, confianca, resposta)
    return True

def executar_em_thread(ia_id, ativo, acao, valor, confianca):
    thread = threading.Thread(
        target=executar_operacao,
        args=(ia_id, ativo, acao, valor, confianca)
    )
    thread.start()
