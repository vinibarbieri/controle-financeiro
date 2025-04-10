from models.despesa import Despesa
from services.controle_financeiro import ControleFinanceiro

def exibir_menu():
    print("\n=== Sistema de Controle Financeiro ===")
    print("1. Cadastrar nova categoria")
    print("2. Adicionar despesa")
    print("3. Gerar relatório mensal")
    print("4. Comparar com mês anterior")
    print("5. Exportar relatório para PDF")
    print("6. Listar categorias e gastos")
    print("7. Sair")

def input_data():
    while True:
        data_str = input("Data da despesa (DD/MM/AAAA): ")
        try:
            return data_str
        except ValueError:
            print("Data inválida. Tente novamente.")

if __name__ == "__main__":
    cf = ControleFinanceiro()
    relatorio_atual = None
    mes_atual = None
    ano_atual = None

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome da categoria: ")
            limite = float(input("Limite de gasto para a categoria: "))
            cf.adicionar_categoria(nome, limite)
            print("Categoria cadastrada com sucesso.")

        elif opcao == "2":
            categoria = input("Categoria: ")
            valor = float(input("Valor da despesa: "))
            data = input_data()
            descricao = input("Descrição da despesa: ")
            try:
                cf.adicionar_despesa(Despesa(valor, categoria, data, descricao))
                print("Despesa adicionada com sucesso.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "3":
            mes_atual = int(input("Digite o mês (1-12): "))
            ano_atual = int(input("Digite o ano (ex: 2025): "))
            relatorio_atual = cf.gerar_relatorio_mensal(mes_atual, ano_atual)

            print(f"\n=== Relatório de {mes_atual:02}/{ano_atual} ===")
            for cat, dados in relatorio_atual.items():
                print(f"\nCategoria: {cat}")
                print(f"Total Gasto: R$ {dados['total']:.2f}")

                if cf.categorias[cat].ultrapassou_limite_mensal(mes_atual, ano_atual):
                    print("⚠️ Limite ultrapassado!")
                else:
                    print("✅ Dentro do limite.")

                for d in dados["despesas"]:
                    print(f" - {d}")


        elif opcao == "4":
            if not relatorio_atual:
                print("⚠️ Gere primeiro um relatório mensal.")
                continue
            try:
                mes = int(input("Digite o mês atual (1-12): "))
                ano = int(input("Digite o ano atual (ex: 2025): "))
            except ValueError:
                print("❌ Entrada inválida. Use números inteiros.")
                continue

            comparacao = cf.comparar_meses(mes, ano)
            print(f"\n📊 Comparação de {mes:02}/{ano} com mês anterior:")
            for cat, aumento in comparacao.items():
                if aumento > 0:
                    print(f"⬆️ Gasto em {cat} aumentou R$ {aumento:.2f}")
                elif aumento < 0:
                    print(f"⬇️ Gasto em {cat} reduziu R$ {abs(aumento):.2f}")
                else:
                    print(f"🔁 Gasto em {cat} permaneceu igual.")

        elif opcao == "5":
            if not relatorio_atual:
                print("⚠️ Gere primeiro um relatório mensal.")
                continue
            nome_pdf = f"relatorio_{mes_atual:02}_{ano_atual}.pdf"
            cf.exportar_pdf(relatorio_atual, mes_atual, ano_atual, nome_pdf)

        elif opcao == "6":
            mes = int(input("Digite o mês (1-12): "))
            ano = int(input("Digite o ano (ex: 2025): "))
            for nome, categoria in cf.categorias.items():
                gasto = categoria.gasto_mensal(mes, ano)
                print(f"{nome} | Limite: R$ {categoria.limite:.2f} | Gasto em {mes:02}/{ano}: R$ {gasto:.2f}")
                for d in categoria.despesas:
                    if d.data.month == mes and d.data.year == ano:
                        print(f"  - {d}")


        elif opcao == "7":
            print("Saindo... Até mais!")
            break

        else:
            print("❌ Opção inválida. Tente novamente.")
