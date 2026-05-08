# Arquitetura

Este documento vai descrever a arquitetura do Núcleo Analytics.

Nesta etapa inicial, a arquitetura prevista segue o fluxo:

```text
Dados sintéticos -> Tratamento -> PostgreSQL -> SQL analítico -> Indicadores -> Dashboard
```

A etapa de banco de dados usa PostgreSQL em Docker. O script `src/carga_postgres.py` recria as tabelas relacionais com `sql/01_criar_tabelas.sql` e carrega os arquivos tratados de `data/processed/`.

Nesta fase, o banco recebe somente a camada relacional de apoio. A modelagem analítica, consultas executivas e dashboard serão implementados em etapas futuras.
