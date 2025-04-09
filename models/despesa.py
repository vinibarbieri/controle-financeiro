from datetime import datetime

class Despesa:
    def __init__(self, valor: float, categoria: str, data: str, descricao: str):
        self.valor = valor
        self.categoria = categoria
        self.data = datetime.strptime(data, "%d/%m/%Y")
        self.descricao = descricao

    def __repr__(self):
        return f"{self.data.strftime('%d/%m/%Y')} - {self.categoria} - R$ {self.valor:.2f} - {self.descricao}"
