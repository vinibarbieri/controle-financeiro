from fpdf import FPDF
from datetime import datetime
import os
from models.despesa import Despesa
from models.categoria import Categoria

class ControleFinanceiro:
    def __init__(self):
        self.categorias = {}
        self.historico = {}

    def adicionar_categoria(self, nome: str, limite: float):
        self.categorias[nome] = Categoria(nome, limite)

    def adicionar_despesa(self, despesa: Despesa):
        if despesa.categoria not in self.categorias:
            raise ValueError("Categoria não cadastrada")
        self.categorias[despesa.categoria].adicionar_despesa(despesa)

        if self.categorias[despesa.categoria].ultrapassou_limite():
            print(f"ALERTA: A categoria '{despesa.categoria}' ultrapassou o limite!")

    def gerar_relatorio_mensal(self, mes: int, ano: int):
        relatorio = {}
        for cat, categoria in self.categorias.items():
            despesas_mes = [d for d in categoria.despesas if d.data.month == mes and d.data.year == ano]
            total = sum(d.valor for d in despesas_mes)
            relatorio[cat] = {
                "total": total,
                "despesas": despesas_mes
            }
        self.historico[(mes, ano)] = relatorio
        return relatorio

    def comparar_meses(self, mes_atual: int, ano_atual: int):
        mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
        ano_anterior = ano_atual if mes_atual > 1 else ano_atual - 1
        atual = self.historico.get((mes_atual, ano_atual), {})
        anterior = self.historico.get((mes_anterior, ano_anterior), {})

        comparacao = {}
        for cat in atual:
            gasto_atual = atual[cat]["total"]
            gasto_anterior = anterior.get(cat, {}).get("total", 0)
            aumento = gasto_atual - gasto_anterior
            comparacao[cat] = aumento
        return comparacao

    def exportar_pdf(self, relatorio, mes: int, ano: int, caminho: str = "relatorio.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório Financeiro - {mes:02}/{ano}", ln=True, align='C')

        for cat, dados in relatorio.items():
            pdf.cell(200, 10, txt=f"\nCategoria: {cat} - Total Gasto: R$ {dados['total']:.2f}", ln=True)
            for d in dados['despesas']:
                linha = f"  - {d.data.strftime('%d/%m/%Y')} | R$ {d.valor:.2f} | {d.descricao}"
                pdf.cell(200, 10, txt=linha, ln=True)

        pdf.output(caminho)
        print(f"PDF exportado para {os.path.abspath(caminho)}")
