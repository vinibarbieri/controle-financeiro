from models.despesa import Despesa
from services.controle_financeiro import ControleFinanceiro

if __name__ == "__main__":
    cf = ControleFinanceiro()

    # Cadastrando categorias
    cf.adicionar_categoria("Alimentação", 1000)
    cf.adicionar_categoria("Transporte", 500)

    # Adicionando despesas
    cf.adicionar_despesa(Despesa(250, "Alimentação", "02/04/2025", "Compras do mês"))
    cf.adicionar_despesa(Despesa(300, "Transporte", "03/04/2025", "Gasolina"))
    cf.adicionar_despesa(Despesa(800, "Alimentação", "10/04/2025", "Restaurante"))  # Gera alerta

    # Gerando relatório
    relatorio_abril = cf.gerar_relatorio_mensal(4, 2025)
    cf.exportar_pdf(relatorio_abril, 4, 2025)

    # Comparando com mês anterior (março)
    relatorio_marco = cf.gerar_relatorio_mensal(3, 2025)
    comparacao = cf.comparar_meses(4, 2025)
    print("\nComparação com mês anterior:")
    for cat, aumento in comparacao.items():
        if aumento > 0:
            print(f"Gasto em {cat} aumentou R$ {aumento:.2f} em relação a março.")
