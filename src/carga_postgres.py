"""Cria as tabelas e carrega os dados tratados no PostgreSQL.

O script usa os arquivos CSV de ``data/processed`` e o DDL definido em
``sql/01_criar_tabelas.sql``. A carga é feita em uma ordem fixa para respeitar
as chaves estrangeiras entre as tabelas.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CREATE_TABLES_SQL = BASE_DIR / "sql" / "01_criar_tabelas.sql"


ORDEM_CARGA = [
    "clientes",
    "planos",
    "assinaturas",
    "pagamentos",
    "campanhas_marketing",
    "tickets_suporte",
    "eventos_uso",
]


def obter_configuracao_banco() -> dict[str, str | int]:
    """Lê as variáveis de ambiente com valores padrão para uso local."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "nucleo_analytics"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }


def conectar_postgres():
    """Abre conexão com o PostgreSQL e apresenta erro claro em caso de falha."""
    try:
        conexao = psycopg2.connect(**obter_configuracao_banco())
        conexao.autocommit = False
        print("Conexão com PostgreSQL realizada com sucesso.")
        return conexao
    except Exception as erro:
        raise RuntimeError(
            "Não foi possível conectar ao PostgreSQL. "
            "Verifique se o Docker está em execução e se o serviço postgres subiu."
        ) from erro


def criar_tabelas(conexao) -> None:
    """Executa o script SQL responsável por recriar as tabelas."""
    if not CREATE_TABLES_SQL.exists():
        raise FileNotFoundError(f"Script SQL não encontrado: {CREATE_TABLES_SQL}")

    try:
        with conexao.cursor() as cursor:
            cursor.execute(CREATE_TABLES_SQL.read_text(encoding="utf-8"))
        conexao.commit()
        print("Tabelas criadas ou recriadas com sucesso.")
    except Exception as erro:
        conexao.rollback()
        raise RuntimeError("Erro ao criar as tabelas no PostgreSQL.") from erro


def carregar_csv_tratado(tabela: str) -> pd.DataFrame:
    """Lê um CSV tratado da pasta data/processed."""
    caminho = PROCESSED_DIR / f"{tabela}.csv"
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo tratado não encontrado: {caminho}")

    dados = pd.read_csv(caminho)
    return dados.where(pd.notna(dados), None)


def inserir_dataframe(conexao, tabela: str, dados: pd.DataFrame) -> int:
    """Insere um DataFrame inteiro em uma tabela PostgreSQL."""
    if dados.empty:
        return 0

    colunas = list(dados.columns)
    registros = [tuple(linha) for linha in dados.to_numpy()]
    comando = sql.SQL("INSERT INTO {tabela} ({colunas}) VALUES %s").format(
        tabela=sql.Identifier(tabela),
        colunas=sql.SQL(", ").join(sql.Identifier(coluna) for coluna in colunas),
    )

    try:
        with conexao.cursor() as cursor:
            execute_values(cursor, comando.as_string(conexao), registros)
        conexao.commit()
        return len(dados)
    except Exception as erro:
        conexao.rollback()
        raise RuntimeError(f"Erro ao carregar dados na tabela {tabela}.") from erro


def carregar_tabelas(conexao) -> dict[str, int]:
    """Carrega as tabelas na ordem correta para respeitar relacionamentos."""
    linhas_carregadas = {}

    for tabela in ORDEM_CARGA:
        dados = carregar_csv_tratado(tabela)
        total = inserir_dataframe(conexao, tabela, dados)
        linhas_carregadas[tabela] = total
        print(f"Tabela {tabela}: {total} linha(s) carregada(s).")

    return linhas_carregadas


def validar_carga(conexao, tabelas: list[str]) -> dict[str, int]:
    """Confere no banco a quantidade de registros carregados por tabela."""
    totais = {}

    with conexao.cursor() as cursor:
        for tabela in tabelas:
            cursor.execute(sql.SQL("SELECT COUNT(*) FROM {tabela}").format(tabela=sql.Identifier(tabela)))
            totais[tabela] = int(cursor.fetchone()[0])

    return totais


def imprimir_resumo(totais_banco: dict[str, int]) -> None:
    """Exibe um resumo final da carga."""
    print("\nResumo da carga no PostgreSQL:")
    for tabela, total in totais_banco.items():
        print(f"- {tabela}: {total} registro(s) no banco")
    print("\nCarga finalizada com sucesso.")


def main() -> None:
    """Executa criação das tabelas e carga dos CSVs tratados."""
    conexao = conectar_postgres()

    try:
        criar_tabelas(conexao)
        carregar_tabelas(conexao)
        totais_banco = validar_carga(conexao, ORDEM_CARGA)
        imprimir_resumo(totais_banco)
    finally:
        conexao.close()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as erro:
        print(f"Erro: {erro}")
        sys.exit(1)
