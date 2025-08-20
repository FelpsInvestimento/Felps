# backend/trade_engine.py
import time
from novadax_api import NovaDAXAPI
from strategies import analyze_market
from utils import format_report

class TradeEngine:
    def __init__(self, api_key, api_secret, mode="moderado", stop_loss_pct=0.02):
        self.novadax = NovaDAXAPI(api_key, api_secret)
        self.mode = mode
        self.stop_loss_pct = stop_loss_pct
        self.running = True

    def run(self):
        print("🚀 Felps Trade iniciado! Operando na NovaDAX...")
        while self.running:
            try:
                # 1️⃣ Pega saldo em tempo real
                balances = self.novadax.get_balance()
                print(f"💰 Saldo atualizado: {balances}")

                # 2️⃣ Lista de ativos para analisar (exemplo: BTC, ETH, USDT)
                ativos = ["BTC_BRL", "ETH_BRL", "USDT_BRL"]

                for ativo in ativos:
                    # 3️⃣ Chama a função de análise (5 IAs aqui dentro)
                    signal, price = analyze_market(ativo, self.mode)

                    if signal == "BUY":
                        amount = self._calcular_quantidade(ativo, balances)
                        if amount > 0:
                            print(f"🟢 Comprando {amount} de {ativo} a {price}")
                            self.novadax.buy(ativo, amount, price)

                    elif signal == "SELL":
                        amount = self._pegar_saldo_disponivel(ativo, balances)
                        if amount > 0:
                            print(f"🔴 Vendendo {amount} de {ativo} a {price}")
                            self.novadax.sell(ativo, amount, price)

                    # 4️⃣ Stop loss inteligente
                    self._check_stop_loss(ativo, price, balances)

                # 5️⃣ Relatório resumido
                print(format_report(balances))

                # Aguarda 60 segundos antes de nova análise
                time.sleep(60)

            except Exception as e:
                print(f"❌ Erro no motor de trade: {e}")
                time.sleep(10)

    def _calcular_quantidade(self, symbol, balances):
        """Calcula a quantidade para compra com base no saldo disponível."""
        saldo_brl = next((b['balance'] for b in balances['data'] if b['currency'] == "BRL"), 0)
        if saldo_brl > 50:  # Valor mínimo para compra
            return round((saldo_brl * 0.95) / 5, 6)  # Divide entre ativos
        return 0

    def _pegar_saldo_disponivel(self, symbol, balances):
        """Retorna saldo disponível para venda."""
        moeda = symbol.split("_")[0]
        saldo = next((b['balance'] for b in balances['data'] if b['currency'] == moeda), 0)
        return round(float(saldo), 6)

    def _check_stop_loss(self, symbol, current_price, balances):
        """Verifica e aciona stop loss inteligente."""
        moeda = symbol.split("_")[0]
        saldo = self._pegar_saldo_disponivel(symbol, balances)
        if saldo > 0:
            preco_compra = current_price * 1.02  # Exemplo fictício
            stop_price = preco_compra * (1 - self.stop_loss_pct)
            if current_price <= stop_price:
                print(f"⚠ Stop loss acionado para {symbol} a {current_price}")
                self.novadax.sell(symbol, saldo, current_price)
