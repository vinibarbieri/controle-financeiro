from models.despesa import Despesa

class Categoria:
    def __init__(self, nome: str, limite: float):
        self.nome = nome
        self.limite = limite
        self.despesas = []

    def adicionar_despesa(self, despesa: Despesa):
        if despesa.categoria != self.nome:
            raise ValueError("Categoria da despesa não corresponde")
        self.despesas.append(despesa)

    def total_gasto(self):
        return sum(d.valor for d in self.despesas)

    def ultrapassou_limite(self):
        return self.total_gasto() > self.limite

    def gasto_mensal(self, mes: int, ano: int):
        return sum(d.valor for d in self.despesas if d.data.month == mes and d.data.year == ano)

    def ultrapassou_limite_mensal(self, mes: int, ano: int):
        total_mes = sum(d.valor for d in self.despesas if d.data.month == mes and d.data.year == ano)
        return total_mes > self.limite


