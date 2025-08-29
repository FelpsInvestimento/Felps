import time
from datetime import datetime, timedelta
import statistics

class ProfitOptimizationIA:
    def __init__(self, novadax_api):
        self.novadax_api = novadax_api
        self.trade_history = []
        self.profit_targets = {}
        self.risk_tolerance = 0.02  # 2% padrão
        
    def calculate_optimal_entry_amount(self, symbol, available_balance, trading_mode="AUTOMATIC", custom_entry_value=None):
        """
        Calcula o valor ótimo de entrada para maximizar lucro e minimizar risco
        """
        try:
            if custom_entry_value and custom_entry_value > 0:
                # Se o usuário definiu um valor específico, usar esse valor
                entry_amount = min(custom_entry_value, available_balance * 0.95)  # Máximo 95% do saldo
                return {
                    "entry_amount": entry_amount,
                    "percentage_of_balance": (entry_amount / available_balance) * 100 if available_balance > 0 else 0,
                    "strategy": "user_defined",
                    "risk_level": "custom"
                }
            
            # Estratégias baseadas no modo de trading
            strategies = {
                "LIGHT": {"max_percentage": 10, "risk_multiplier": 0.5},
                "MODERATE": {"max_percentage": 25, "risk_multiplier": 1.0},
                "AGGRESSIVE": {"max_percentage": 50, "risk_multiplier": 2.0},
                "AUTOMATIC": {"max_percentage": 20, "risk_multiplier": 1.2}
            }
            
            strategy = strategies.get(trading_mode, strategies["AUTOMATIC"])
            
            # Calcular valor base
            base_percentage = strategy["max_percentage"]
            
            # Ajustar baseado no histórico de performance
            performance_multiplier = self._calculate_performance_multiplier(symbol)
            
            # Ajustar baseado na volatilidade do ativo
            volatility_multiplier = self._calculate_volatility_multiplier(symbol)
            
            # Calcular percentual final
            final_percentage = base_percentage * performance_multiplier * volatility_multiplier
            final_percentage = max(1, min(final_percentage, 80))  # Entre 1% e 80%
            
            entry_amount = (available_balance * final_percentage) / 100
            
            return {
                "entry_amount": entry_amount,
                "percentage_of_balance": final_percentage,
                "strategy": f"{trading_mode.lower()}_optimized",
                "risk_level": self._classify_risk_level(final_percentage),
                "performance_factor": performance_multiplier,
                "volatility_factor": volatility_multiplier
            }
            
        except Exception as e:
            print(f"Erro no cálculo de entrada ótima: {e}")
            # Fallback seguro
            safe_amount = available_balance * 0.05  # 5% como fallback
            return {
                "entry_amount": safe_amount,
                "percentage_of_balance": 5.0,
                "strategy": "safe_fallback",
                "risk_level": "very_low"
            }
    
    def _calculate_performance_multiplier(self, symbol):
        """
        Calcula multiplicador baseado na performance histórica do símbolo
        """
        # Filtrar trades do símbolo específico
        symbol_trades = [trade for trade in self.trade_history if trade.get('symbol') == symbol]
        
        if len(symbol_trades) < 3:
            return 1.0  # Neutro se poucos dados
        
        # Calcular taxa de sucesso
        successful_trades = [trade for trade in symbol_trades if trade.get('profit', 0) > 0]
        success_rate = len(successful_trades) / len(symbol_trades)
        
        # Calcular lucro médio
        profits = [trade.get('profit', 0) for trade in symbol_trades]
        avg_profit = statistics.mean(profits) if profits else 0
        
        # Multiplicador baseado na performance
        if success_rate > 0.7 and avg_profit > 0:
            return 1.3  # Aumentar exposição para ativos performáticos
        elif success_rate > 0.5:
            return 1.0  # Manter neutro
        else:
            return 0.7  # Reduzir exposição para ativos com baixa performance
    
    def _calculate_volatility_multiplier(self, symbol):
        """
        Ajusta entrada baseado na volatilidade do ativo
        """
        try:
            # Obter dados de preço recentes
            ticker_data = self.novadax_api.get_ticker(symbol)
            if not ticker_data or ticker_data.get("code") != "A10000":
                return 1.0
            
            data = ticker_data.get("data", {})
            high_24h = float(data.get("high24h", 0))
            low_24h = float(data.get("low24h", 0))
            last_price = float(data.get("lastPrice", 0))
            
            if last_price == 0:
                return 1.0
            
            # Calcular volatilidade (amplitude de 24h)
            volatility = ((high_24h - low_24h) / last_price) * 100
            
            # Ajustar multiplicador baseado na volatilidade
            if volatility > 15:  # Alta volatilidade
                return 0.8  # Reduzir exposição
            elif volatility > 8:  # Volatilidade moderada
                return 1.0  # Manter neutro
            else:  # Baixa volatilidade
                return 1.2  # Aumentar exposição
                
        except Exception as e:
            print(f"Erro no cálculo de volatilidade: {e}")
            return 1.0
    
    def _classify_risk_level(self, percentage):
        """
        Classifica o nível de risco baseado no percentual do saldo
        """
        if percentage <= 5:
            return "very_low"
        elif percentage <= 15:
            return "low"
        elif percentage <= 30:
            return "moderate"
        elif percentage <= 50:
            return "high"
        else:
            return "very_high"
    
    def calculate_optimal_exit_strategy(self, symbol, entry_price, current_price, position_size, daily_profit_target=None):
        """
        Calcula a estratégia ótima de saída para maximizar lucro
        """
        try:
            current_profit_percentage = ((current_price - entry_price) / entry_price) * 100
            current_profit_value = (current_price - entry_price) * position_size
            
            # Verificar se atingiu meta de lucro diário
            if daily_profit_target and current_profit_value >= daily_profit_target:
                return {
                    "action": "SELL",
                    "reason": "daily_profit_target_reached",
                    "confidence": 0.95,
                    "current_profit": current_profit_value,
                    "profit_percentage": current_profit_percentage
                }
            
            # Estratégia de take profit dinâmico
            if current_profit_percentage > 0:
                # Lucro pequeno (0-2%): aguardar mais
                if current_profit_percentage < 2:
                    return {
                        "action": "HOLD",
                        "reason": "small_profit_wait_for_more",
                        "confidence": 0.6,
                        "current_profit": current_profit_value,
                        "profit_percentage": current_profit_percentage
                    }
                
                # Lucro moderado (2-5%): considerar venda parcial
                elif current_profit_percentage < 5:
                    return {
                        "action": "PARTIAL_SELL",
                        "sell_percentage": 50,  # Vender 50% da posição
                        "reason": "moderate_profit_partial_exit",
                        "confidence": 0.75,
                        "current_profit": current_profit_value,
                        "profit_percentage": current_profit_percentage
                    }
                
                # Lucro alto (5%+): vender tudo
                else:
                    return {
                        "action": "SELL",
                        "reason": "high_profit_full_exit",
                        "confidence": 0.9,
                        "current_profit": current_profit_value,
                        "profit_percentage": current_profit_percentage
                    }
            
            # Se está no prejuízo, manter posição (stop loss será gerenciado pela IA específica)
            else:
                return {
                    "action": "HOLD",
                    "reason": "negative_profit_wait_recovery",
                    "confidence": 0.4,
                    "current_profit": current_profit_value,
                    "profit_percentage": current_profit_percentage
                }
                
        except Exception as e:
            print(f"Erro no cálculo de estratégia de saída: {e}")
            return {
                "action": "HOLD",
                "reason": "calculation_error",
                "confidence": 0.3,
                "current_profit": 0,
                "profit_percentage": 0
            }
    
    def update_trade_history(self, trade_data):
        """
        Atualiza o histórico de trades para melhorar futuras decisões
        """
        trade_record = {
            "timestamp": datetime.now().isoformat(),
            "symbol": trade_data.get("symbol"),
            "action": trade_data.get("action"),
            "entry_price": trade_data.get("entry_price"),
            "exit_price": trade_data.get("exit_price"),
            "position_size": trade_data.get("position_size"),
            "profit": trade_data.get("profit", 0),
            "profit_percentage": trade_data.get("profit_percentage", 0),
            "duration_minutes": trade_data.get("duration_minutes", 0)
        }
        
        self.trade_history.append(trade_record)
        
        # Manter apenas os últimos 100 trades para performance
        if len(self.trade_history) > 100:
            self.trade_history = self.trade_history[-100:]
    
    def get_performance_metrics(self):
        """
        Calcula métricas de performance do robô
        """
        if not self.trade_history:
            return {
                "total_trades": 0,
                "success_rate": 0,
                "total_profit": 0,
                "average_profit": 0,
                "best_trade": 0,
                "worst_trade": 0
            }
        
        completed_trades = [trade for trade in self.trade_history if trade.get("exit_price")]
        
        if not completed_trades:
            return {
                "total_trades": len(self.trade_history),
                "success_rate": 0,
                "total_profit": 0,
                "average_profit": 0,
                "best_trade": 0,
                "worst_trade": 0
            }
        
        profits = [trade.get("profit", 0) for trade in completed_trades]
        successful_trades = [p for p in profits if p > 0]
        
        return {
            "total_trades": len(completed_trades),
            "success_rate": (len(successful_trades) / len(completed_trades)) * 100,
            "total_profit": sum(profits),
            "average_profit": statistics.mean(profits),
            "best_trade": max(profits),
            "worst_trade": min(profits),
            "profit_factor": sum(successful_trades) / abs(sum([p for p in profits if p < 0])) if any(p < 0 for p in profits) else float('inf')
        }
    
    def should_continue_trading(self, daily_profit_target=None, current_daily_profit=0):
        """
        Determina se deve continuar operando baseado na meta de lucro diário
        """
        if daily_profit_target and current_daily_profit >= daily_profit_target:
            return {
                "continue": False,
                "reason": "daily_target_reached",
                "current_profit": current_daily_profit,
                "target": daily_profit_target
            }
        
        # Verificar se está muito no prejuízo (proteção adicional)
        if daily_profit_target and current_daily_profit < -(daily_profit_target * 0.5):
            return {
                "continue": False,
                "reason": "daily_loss_limit_reached",
                "current_profit": current_daily_profit,
                "loss_limit": -(daily_profit_target * 0.5)
            }
        
        return {
            "continue": True,
            "reason": "within_limits",
            "current_profit": current_daily_profit
        }


# Exemplo de uso e teste
if __name__ == "__main__":
    # Para teste, criar uma instância mock da API
    class MockAPI:
        def get_ticker(self, symbol):
            return {
                "code": "A10000",
                "data": {
                    "lastPrice": "100000",
                    "high24h": "105000",
                    "low24h": "95000"
                }
            }
    
    profit_ia = ProfitOptimizationIA(MockAPI())
    
    print("=== TESTE DA IA DE OTIMIZAÇÃO DE LUCRO ===")
    
    # Testar cálculo de entrada ótima
    entry_calc = profit_ia.calculate_optimal_entry_amount("BTC_BRL", 1000, "MODERATE")
    print(f"\nEntrada Ótima para BTC_BRL (Saldo: R$ 1000):")
    print(f"  Valor: R$ {entry_calc['entry_amount']:.2f}")
    print(f"  Percentual: {entry_calc['percentage_of_balance']:.1f}%")
    print(f"  Estratégia: {entry_calc['strategy']}")
    print(f"  Risco: {entry_calc['risk_level']}")
    
    # Testar estratégia de saída
    exit_strategy = profit_ia.calculate_optimal_exit_strategy("BTC_BRL", 100000, 103000, 0.01)
    print(f"\nEstratégia de Saída (Entrada: R$ 100k, Atual: R$ 103k):")
    print(f"  Ação: {exit_strategy['action']}")
    print(f"  Razão: {exit_strategy['reason']}")
    print(f"  Lucro: R$ {exit_strategy['current_profit']:.2f}")
    print(f"  Percentual: {exit_strategy['profit_percentage']:.2f}%")
    
    # Simular alguns trades para testar métricas
    sample_trades = [
        {"symbol": "BTC_BRL", "profit": 150, "profit_percentage": 3.0},
        {"symbol": "ETH_BRL", "profit": -50, "profit_percentage": -1.5},
        {"symbol": "BTC_BRL", "profit": 200, "profit_percentage": 4.2}
    ]
    
    for trade in sample_trades:
        profit_ia.update_trade_history(trade)
    
    # Testar métricas de performance
    metrics = profit_ia.get_performance_metrics()
    print(f"\n=== MÉTRICAS DE PERFORMANCE ===")
    print(f"Total de Trades: {metrics['total_trades']}")
    print(f"Taxa de Sucesso: {metrics['success_rate']:.1f}%")
    print(f"Lucro Total: R$ {metrics['total_profit']:.2f}")
    print(f"Lucro Médio: R$ {metrics['average_profit']:.2f}")
    print(f"Melhor Trade: R$ {metrics['best_trade']:.2f}")
    print(f"Pior Trade: R$ {metrics['worst_trade']:.2f}")

