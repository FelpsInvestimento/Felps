from app.ias.supervisor_ia import SupervisorIA

class TradeManager:
    def __init__(self, accounts_config):
        self.supervisor_ia = SupervisorIA(accounts_config)

    def start_robot(self):
        self.supervisor_ia.start_trading()

    def stop_robot(self):
        self.supervisor_ia.stop_trading()

    def get_robot_status(self):
        return self.supervisor_ia.get_status()

    def get_all_balances(self):
        return self.supervisor_ia.get_all_balances()

    def set_trading_mode(self, mode):
        self.supervisor_ia.set_trading_mode(mode)

    def get_trading_mode(self):
        return self.supervisor_ia.get_trading_mode()

    def get_operations_log(self):
        return self.supervisor_ia.get_operations_log()

    def check_ias_functioning(self):
        return self.supervisor_ia.check_ias_functioning()


