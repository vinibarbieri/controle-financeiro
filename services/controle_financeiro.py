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

        comparacao = {}

        for cat, categoria in self.categorias.items():
            atual = sum(d.valor for d in categoria.despesas if d.data.month == mes_atual and d.data.year == ano_atual)
            anterior = sum(d.valor for d in categoria.despesas if d.data.month == mes_anterior and d.data.year == ano_anterior)
            comparacao[cat] = atual - anterior

        return comparacao


    def exportar_pdf(self, relatorio, mes: int, ano: int, caminho: str = "relatorio.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Relatório Financeiro Completo - {mes:02}/{ano}", ln=True, align='C')

        comparacao = self.comparar_meses(mes, ano)

        for cat, dados in relatorio.items():
            total = dados['total']
            despesas = dados['despesas']
            categoria = self.categorias[cat]

            pdf.ln(10)
            pdf.set_font("Arial", "B", size=12)
            pdf.cell(200, 10, txt=f"Categoria: {cat}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(200, 8, txt=f"Limite mensal: R$ {categoria.limite:.2f}", ln=True)
            pdf.cell(200, 8, txt=f"Gasto no mês: R$ {total:.2f}", ln=True)

            if total > categoria.limite:
                pdf.set_text_color(255, 0, 0)  # vermelho
                pdf.cell(200, 8, txt="Atenção: Gasto acima do limite!", ln=True)
            else:
                pdf.set_text_color(0, 128, 0)  # verde
                pdf.cell(200, 8, txt="Gasto dentro do limite.", ln=True)

            pdf.set_text_color(0, 0, 0)  # reset cor para preto

            # Comparação com mês anterior
            aumento = comparacao.get(cat, 0)
            if aumento > 0:
                pdf.cell(200, 8, txt=f"Aumento de R$ {aumento:.2f} em relação ao mês anterior.", ln=True)
            elif aumento < 0:
                pdf.cell(200, 8, txt=f"Redução de R$ {abs(aumento):.2f} em relação ao mês anterior.", ln=True)
            else:
                pdf.cell(200, 8, txt="Gasto igual ao mês anterior.", ln=True)

            # Lista de despesas
            pdf.ln(2)
            pdf.set_font("Arial", "I", size=11)
            pdf.cell(200, 8, txt="Despesas:", ln=True)
            pdf.set_font("Arial", size=10)

            if not despesas:
                pdf.cell(200, 8, txt="(Sem despesas registradas neste mês)", ln=True)
            else:
                for d in despesas:
                    linha = f" - {d.data.strftime('%d/%m/%Y')} | R$ {d.valor:.2f} | {d.descricao}"
                    pdf.cell(200, 8, txt=linha, ln=True)

            pdf.ln(5)  # espaçamento entre categorias

        pdf.output(caminho)
        print(f"PDF exportado com sucesso para: {os.path.abspath(caminho)}")

