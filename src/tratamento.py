"""Tratamento básico dos dados sintéticos do projeto Núcleo Analytics.

Este script lê os arquivos CSV de ``data/raw``, aplica padronizações simples
de tipos, datas, categorias e duplicidades, valida chaves relacionais básicas
e salva os arquivos tratados em ``data/processed``.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


ARQUIVOS = {
    "clientes": "clientes.csv",
    "planos": "planos.csv",
    "assinaturas": "assinaturas.csv",
    "pagamentos": "pagamentos.csv",
    "campanhas_marketing": "campanhas_marketing.csv",
    "tickets_suporte": "tickets_suporte.csv",
    "eventos_uso": "eventos_uso.csv",
}


def garantir_pasta_saida() -> None:
    """Garante que a pasta de dados tratados exista antes da gravação."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def carregar_csv(nome_arquivo: str) -> pd.DataFrame:
    """Carrega um arquivo bruto como texto para controlar as conversões."""
    caminho = RAW_DIR / nome_arquivo
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo bruto não encontrado: {caminho}")

    return pd.read_csv(caminho, dtype="string")


def salvar_csv(tabela: pd.DataFrame, nome_arquivo: str) -> None:
    """Salva a tabela tratada mantendo o mesmo nome do arquivo bruto."""
    tabela.to_csv(PROCESSED_DIR / nome_arquivo, index=False, encoding="utf-8")


def para_snake_case(texto: str) -> str:
    """Converte um texto para snake_case simples."""
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_ascii = texto_normalizado.encode("ascii", "ignore").decode("ascii")
    texto_ascii = re.sub(r"[^a-zA-Z0-9]+", "_", texto_ascii)
    return texto_ascii.strip("_").lower()


def padronizar_colunas(tabela: pd.DataFrame) -> pd.DataFrame:
    """Padroniza os nomes das colunas para snake_case."""
    tabela = tabela.copy()
    tabela.columns = [para_snake_case(coluna) for coluna in tabela.columns]
    return tabela


def padronizar_id(serie: pd.Series) -> pd.Series:
    """Padroniza identificadores como texto sem espaços extras."""
    return serie.astype("string").str.strip().str.upper()


def padronizar_categoria(serie: pd.Series) -> pd.Series:
    """Padroniza categorias sem inventar valores ausentes."""
    texto = serie.astype("string").str.strip().str.lower()
    texto = texto.str.replace(r"\s+", "_", regex=True)
    texto = texto.str.replace("-", "_", regex=False)
    texto = texto.str.replace(r"_+", "_", regex=True)
    return texto


def padronizar_texto_livre(serie: pd.Series) -> pd.Series:
    """Remove espaços excedentes de textos descritivos, sem alterar conteúdo."""
    return serie.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)


def converter_data(serie: pd.Series) -> pd.Series:
    """Converte datas para o formato ISO yyyy-mm-dd, preservando nulos."""
    datas = pd.to_datetime(serie, errors="coerce", format="mixed")
    return datas.dt.strftime("%Y-%m-%d").astype("string")


def converter_mes_referencia(serie: pd.Series) -> pd.Series:
    """Converte competência mensal para o formato yyyy-mm."""
    texto = serie.astype("string").str.strip()
    texto = texto.where(texto.notna() & (texto != ""))
    datas = pd.to_datetime(texto + "-01", errors="coerce")
    return datas.dt.to_period("M").astype("string")


def converter_numero(serie: pd.Series, casas_decimais: int | None = None) -> pd.Series:
    """Converte campos numéricos, mantendo nulos quando a conversão falhar."""
    numeros = pd.to_numeric(serie, errors="coerce")
    if casas_decimais is not None:
        numeros = numeros.round(casas_decimais)
    return numeros


def converter_inteiro(serie: pd.Series) -> pd.Series:
    """Converte quantidades para inteiro anulável do Pandas."""
    return pd.to_numeric(serie, errors="coerce").astype("Int64")


def remover_duplicidades(tabela: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove duplicidades exatas e informa quantas linhas foram removidas."""
    duplicidades = int(tabela.duplicated().sum())
    tabela = tabela.drop_duplicates().reset_index(drop=True)
    return tabela, duplicidades


def remover_linhas_sem_chaves(tabela: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    """Remove linhas sem chaves críticas, pois elas quebrariam relacionamentos."""
    return tabela.dropna(subset=colunas).reset_index(drop=True)


def resumo_nulos(tabela: pd.DataFrame) -> dict[str, int]:
    """Retorna apenas as colunas que possuem valores nulos."""
    nulos = tabela.isna().sum()
    return {coluna: int(total) for coluna, total in nulos.items() if total > 0}


def montar_resumo(
    nome_arquivo: str,
    linhas_entrada: int,
    tabela_saida: pd.DataFrame,
    duplicidades: int,
) -> dict[str, object]:
    """Monta o resumo de tratamento de uma tabela."""
    return {
        "arquivo": nome_arquivo,
        "linhas_entrada": linhas_entrada,
        "linhas_saida": len(tabela_saida),
        "duplicidades_removidas": duplicidades,
        "nulos": resumo_nulos(tabela_saida),
    }


def tratar_clientes() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de clientes."""
    nome_arquivo = ARQUIVOS["clientes"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["cliente_id"] = padronizar_id(tabela["cliente_id"])
    tabela["nome_empresa"] = padronizar_texto_livre(tabela["nome_empresa"])
    tabela["segmento"] = padronizar_categoria(tabela["segmento"])
    tabela["porte_empresa"] = padronizar_categoria(tabela["porte_empresa"])
    tabela["cidade"] = padronizar_texto_livre(tabela["cidade"])
    tabela["estado"] = tabela["estado"].astype("string").str.strip().str.upper()
    tabela["data_cadastro"] = converter_data(tabela["data_cadastro"])
    tabela["status_cliente"] = padronizar_categoria(tabela["status_cliente"])

    tabela = remover_linhas_sem_chaves(tabela, ["cliente_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_planos() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de planos."""
    nome_arquivo = ARQUIVOS["planos"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["plano_id"] = padronizar_id(tabela["plano_id"])
    tabela["nome_plano"] = padronizar_texto_livre(tabela["nome_plano"])
    tabela["valor_mensal"] = converter_numero(tabela["valor_mensal"], casas_decimais=2)
    tabela["limite_usuarios"] = converter_inteiro(tabela["limite_usuarios"])
    tabela["categoria_plano"] = padronizar_categoria(tabela["categoria_plano"])

    tabela = remover_linhas_sem_chaves(tabela, ["plano_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_assinaturas() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de assinaturas."""
    nome_arquivo = ARQUIVOS["assinaturas"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["assinatura_id"] = padronizar_id(tabela["assinatura_id"])
    tabela["cliente_id"] = padronizar_id(tabela["cliente_id"])
    tabela["plano_id"] = padronizar_id(tabela["plano_id"])
    tabela["data_inicio"] = converter_data(tabela["data_inicio"])
    tabela["data_fim"] = converter_data(tabela["data_fim"])
    tabela["status_assinatura"] = padronizar_categoria(tabela["status_assinatura"])

    # data_fim permanece nula para assinaturas ativas.
    tabela = remover_linhas_sem_chaves(tabela, ["assinatura_id", "cliente_id", "plano_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_pagamentos() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de pagamentos."""
    nome_arquivo = ARQUIVOS["pagamentos"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["pagamento_id"] = padronizar_id(tabela["pagamento_id"])
    tabela["assinatura_id"] = padronizar_id(tabela["assinatura_id"])
    tabela["cliente_id"] = padronizar_id(tabela["cliente_id"])
    tabela["data_pagamento"] = converter_data(tabela["data_pagamento"])
    tabela["mes_referencia"] = converter_mes_referencia(tabela["mes_referencia"])
    tabela["valor_pago"] = converter_numero(tabela["valor_pago"], casas_decimais=2)
    tabela["status_pagamento"] = padronizar_categoria(tabela["status_pagamento"])
    tabela["metodo_pagamento"] = padronizar_categoria(tabela["metodo_pagamento"])

    # data_pagamento fica nula quando o pagamento está inadimplente.
    tabela = remover_linhas_sem_chaves(tabela, ["pagamento_id", "assinatura_id", "cliente_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_campanhas_marketing() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de campanhas de marketing."""
    nome_arquivo = ARQUIVOS["campanhas_marketing"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["campanha_id"] = padronizar_id(tabela["campanha_id"])
    tabela["nome_campanha"] = padronizar_texto_livre(tabela["nome_campanha"])
    tabela["canal"] = padronizar_categoria(tabela["canal"])
    tabela["data_inicio"] = converter_data(tabela["data_inicio"])
    tabela["data_fim"] = converter_data(tabela["data_fim"])
    tabela["investimento"] = converter_numero(tabela["investimento"], casas_decimais=2)
    tabela["leads_gerados"] = converter_inteiro(tabela["leads_gerados"])
    tabela["clientes_convertidos"] = converter_inteiro(tabela["clientes_convertidos"])

    tabela = remover_linhas_sem_chaves(tabela, ["campanha_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_tickets_suporte() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de tickets de suporte."""
    nome_arquivo = ARQUIVOS["tickets_suporte"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["ticket_id"] = padronizar_id(tabela["ticket_id"])
    tabela["cliente_id"] = padronizar_id(tabela["cliente_id"])
    tabela["data_abertura"] = converter_data(tabela["data_abertura"])
    tabela["data_fechamento"] = converter_data(tabela["data_fechamento"])
    tabela["categoria"] = padronizar_categoria(tabela["categoria"])
    tabela["prioridade"] = padronizar_categoria(tabela["prioridade"])
    tabela["status_ticket"] = padronizar_categoria(tabela["status_ticket"])
    tabela["tempo_resolucao_horas"] = converter_numero(tabela["tempo_resolucao_horas"], casas_decimais=1)
    tabela["satisfacao_cliente"] = converter_inteiro(tabela["satisfacao_cliente"])

    # Campos de fechamento e satisfação permanecem nulos para tickets abertos.
    tabela = remover_linhas_sem_chaves(tabela, ["ticket_id", "cliente_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def tratar_eventos_uso() -> tuple[pd.DataFrame, dict[str, object]]:
    """Trata a tabela de eventos agregados de uso."""
    nome_arquivo = ARQUIVOS["eventos_uso"]
    tabela = padronizar_colunas(carregar_csv(nome_arquivo))
    linhas_entrada = len(tabela)

    tabela["evento_id"] = padronizar_id(tabela["evento_id"])
    tabela["cliente_id"] = padronizar_id(tabela["cliente_id"])
    tabela["data_evento"] = converter_data(tabela["data_evento"])
    tabela["tipo_evento"] = padronizar_categoria(tabela["tipo_evento"])
    tabela["quantidade_eventos"] = converter_inteiro(tabela["quantidade_eventos"])

    tabela = remover_linhas_sem_chaves(tabela, ["evento_id", "cliente_id"])
    tabela, duplicidades = remover_duplicidades(tabela)
    resumo = montar_resumo(nome_arquivo, linhas_entrada, tabela, duplicidades)
    return tabela, resumo


def validar_chave(
    tabela_origem: pd.DataFrame,
    coluna_origem: str,
    tabela_referencia: pd.DataFrame,
    coluna_referencia: str,
    descricao: str,
) -> str | None:
    """Verifica se os IDs de uma tabela existem na tabela de referência."""
    origem = set(tabela_origem[coluna_origem].dropna())
    referencia = set(tabela_referencia[coluna_referencia].dropna())
    ausentes = sorted(origem - referencia)

    if ausentes:
        exemplos = ", ".join(ausentes[:5])
        return f"{descricao}: {len(ausentes)} valor(es) sem referência. Exemplos: {exemplos}"

    return None


def validar_relacionamentos(tabelas: dict[str, pd.DataFrame]) -> list[str]:
    """Executa validações básicas de integridade entre as tabelas."""
    validacoes = [
        validar_chave(
            tabelas["assinaturas"],
            "cliente_id",
            tabelas["clientes"],
            "cliente_id",
            "assinaturas.cliente_id -> clientes.cliente_id",
        ),
        validar_chave(
            tabelas["assinaturas"],
            "plano_id",
            tabelas["planos"],
            "plano_id",
            "assinaturas.plano_id -> planos.plano_id",
        ),
        validar_chave(
            tabelas["pagamentos"],
            "assinatura_id",
            tabelas["assinaturas"],
            "assinatura_id",
            "pagamentos.assinatura_id -> assinaturas.assinatura_id",
        ),
        validar_chave(
            tabelas["pagamentos"],
            "cliente_id",
            tabelas["clientes"],
            "cliente_id",
            "pagamentos.cliente_id -> clientes.cliente_id",
        ),
        validar_chave(
            tabelas["tickets_suporte"],
            "cliente_id",
            tabelas["clientes"],
            "cliente_id",
            "tickets_suporte.cliente_id -> clientes.cliente_id",
        ),
        validar_chave(
            tabelas["eventos_uso"],
            "cliente_id",
            tabelas["clientes"],
            "cliente_id",
            "eventos_uso.cliente_id -> clientes.cliente_id",
        ),
    ]

    return [aviso for aviso in validacoes if aviso is not None]


def imprimir_resumo(resumos: list[dict[str, object]], avisos: list[str]) -> None:
    """Mostra no terminal o resultado geral do tratamento."""
    print("\nResumo do tratamento:")
    for item in resumos:
        nulos = item["nulos"]
        texto_nulos = (
            ", ".join(f"{coluna}={total}" for coluna, total in nulos.items())
            if nulos
            else "sem nulos"
        )
        print(
            f"- {item['arquivo']}: entrada={item['linhas_entrada']} | "
            f"saida={item['linhas_saida']} | "
            f"duplicidades_removidas={item['duplicidades_removidas']} | "
            f"nulos={texto_nulos}"
        )

    if avisos:
        print("\nAvisos de qualidade:")
        for aviso in avisos:
            print(f"- {aviso}")
    else:
        print("\nAvisos de qualidade: nenhum alerta crítico encontrado.")


def main() -> None:
    """Executa todo o tratamento dos dados sintéticos."""
    garantir_pasta_saida()

    clientes, resumo_clientes = tratar_clientes()
    planos, resumo_planos = tratar_planos()
    assinaturas, resumo_assinaturas = tratar_assinaturas()
    pagamentos, resumo_pagamentos = tratar_pagamentos()
    campanhas, resumo_campanhas = tratar_campanhas_marketing()
    tickets, resumo_tickets = tratar_tickets_suporte()
    eventos, resumo_eventos = tratar_eventos_uso()

    tabelas = {
        "clientes": clientes,
        "planos": planos,
        "assinaturas": assinaturas,
        "pagamentos": pagamentos,
        "campanhas_marketing": campanhas,
        "tickets_suporte": tickets,
        "eventos_uso": eventos,
    }

    for chave, tabela in tabelas.items():
        salvar_csv(tabela, ARQUIVOS[chave])

    avisos = validar_relacionamentos(tabelas)
    imprimir_resumo(
        [
            resumo_clientes,
            resumo_planos,
            resumo_assinaturas,
            resumo_pagamentos,
            resumo_campanhas,
            resumo_tickets,
            resumo_eventos,
        ],
        avisos,
    )


if __name__ == "__main__":
    main()
