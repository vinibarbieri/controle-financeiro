# Sistema de Controle Financeiro

Um sistema de controle financeiro pessoal desenvolvido em Python que permite gerenciar despesas, categorias e gerar relatórios mensais.

## Funcionalidades

- Cadastro e gerenciamento de categorias de despesas
- Registro de despesas com data, valor e descrição
- Geração de relatórios mensais
- Comparação de gastos entre meses
- Exportação de relatórios em PDF
- Sistema de alertas para gastos excessivos

## Estrutura do Projeto

```
.
├── main.py                  # Arquivo principal de execução
├── models/                  # Modelos de dados
│   ├── categoria.py        # Classe Categoria
│   ├── despesa.py          # Classe Despesa
│   └── usuario.py          # Classe Usuário
└── services/               # Serviços do sistema
    └── controle_financeiro.py  # Lógica principal do sistema
```

## Requisitos

- Python 3.x
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o programa principal:
```bash
python main.py
```

O sistema irá:
1. Cadastrar categorias de despesas
2. Registrar despesas
3. Gerar relatórios mensais
4. Comparar gastos com o mês anterior
5. Exportar relatórios em PDF

## Exemplo de Uso

```python
from models.despesa import Despesa
from services.controle_financeiro import ControleFinanceiro

# Inicializa o controle financeiro
cf = ControleFinanceiro()

# Adiciona categorias
cf.adicionar_categoria("Alimentação", 1000)
cf.adicionar_categoria("Transporte", 500)

# Adiciona despesas
cf.adicionar_despesa(Despesa(250, "Alimentação", "02/04/2025", "Compras do mês"))
cf.adicionar_despesa(Despesa(300, "Transporte", "03/04/2025", "Gasolina"))

# Gera relatório
relatorio = cf.gerar_relatorio_mensal(4, 2025)
cf.exportar_pdf(relatorio, 4, 2025)
```

## Contribuição

Contribuições são bem-vindas! Para contribuir com o projeto:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 