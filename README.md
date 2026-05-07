# Núcleo Analytics

Plataforma corporativa de dados, indicadores e inteligência de negócio.

## Descrição

O Núcleo Analytics é um projeto de portfólio voltado à construção de uma base de dados analítica para uma empresa SaaS fictícia. A proposta é simular um cenário corporativo em que dados de clientes, assinaturas, pagamentos, campanhas, suporte e uso da plataforma precisam ser organizados para apoiar decisões de negócio.

Nesta primeira etapa, o projeto contém apenas a estrutura inicial do repositório. As implementações de geração de dados, tratamento, carga em banco, validação, indicadores e dashboard serão adicionadas aos poucos.

## Objetivo

Construir uma solução de analytics com aparência profissional, organizada em camadas e com documentação suficiente para demonstrar domínio prático de dados, SQL, Python, PostgreSQL e indicadores de negócio.

## Contexto de negócio

A empresa fictícia deste projeto vende uma plataforma por assinatura para clientes corporativos. Como acontece em ambientes reais, os dados estão distribuídos em diferentes áreas:

- clientes;
- assinaturas;
- planos;
- pagamentos;
- cancelamentos;
- campanhas de marketing;
- tickets de suporte;
- eventos de uso da plataforma.

O objetivo da solução é transformar esses dados em uma visão executiva com métricas úteis para acompanhamento de receita, retenção, inadimplência, suporte e crescimento.

## Tecnologias previstas

- Python;
- Pandas;
- SQL;
- PostgreSQL;
- Docker;
- Jupyter Notebook;
- Power BI;
- Git e GitHub.

## Como gerar os dados sintéticos

Para criar as bases fictícias usadas no projeto, execute:

```bash
python src/gerar_dados_ficticios.py
```

Os arquivos completos são salvos em `data/raw/`. Amostras menores são salvas em `data/sample/` para facilitar a visualização no GitHub.

## Arquitetura conceitual

```text
Dados sintéticos
   ↓
Tratamento com Python/Pandas
   ↓
Carga em PostgreSQL
   ↓
Modelagem analítica com SQL
   ↓
Validação de qualidade dos dados
   ↓
Geração de indicadores corporativos
   ↓
Dashboard executivo
   ↓
Documentação técnica no GitHub
```

## Estrutura inicial de pastas

```text
nucleo-analytics/
│
├── README.md
├── requirements.txt
├── .gitignore
├── docker-compose.yml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── notebooks/
│   └── 01_analise_exploratoria.ipynb
│
├── src/
│   ├── __init__.py
│   ├── gerar_dados_ficticios.py
│   ├── extracao.py
│   ├── tratamento.py
│   ├── carga_postgres.py
│   ├── qualidade_dados.py
│   └── calcular_indicadores.py
│
├── sql/
│   ├── 01_criar_tabelas.sql
│   ├── 02_carga_dados.sql
│   ├── 03_modelagem_analytics.sql
│   └── 04_consultas_indicadores.sql
│
├── dashboards/
│   ├── powerbi/
│   └── prints/
│
├── docs/
│   ├── arquitetura.md
│   ├── dicionario_dados.md
│   ├── regras_negocio.md
│   └── metricas.md
│
└── reports/
    └── resumo_indicadores.md
```

## Status do projeto

Projeto em fase inicial. A estrutura base do repositório e a geração de dados sintéticos já foram criadas, mas as regras de negócio detalhadas, os pipelines de tratamento, a carga em banco, a modelagem analítica e os indicadores ainda não foram implementados.

## Próximas etapas

- Definir o modelo conceitual dos dados.
- Implementar o pipeline de tratamento com Python.
- Criar as tabelas no PostgreSQL.
- Desenvolver a modelagem analítica em SQL.
- Documentar as regras de negócio e as métricas.
- Construir o dashboard executivo.
