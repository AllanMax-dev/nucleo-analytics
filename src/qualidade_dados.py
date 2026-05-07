"""Valida a qualidade dos dados tratados do projeto Núcleo Analytics.

O script lê os arquivos de ``data/processed``, executa validações gerais,
validações de chaves, integridade referencial e regras simples de negócio.
Ao final, gera um relatório estruturado em JSON e um resumo em Markdown.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"
JSON_REPORT = REPORTS_DIR / "qualidade_dados.json"
MARKDOWN_REPORT = REPORTS_DIR / "relatorio_qualidade_dados.md"


SCHEMAS_ESPERADOS = {
    "clientes": [
        "cliente_id",
        "nome_empresa",
        "segmento",
        "porte_empresa",
        "cidade",
        "estado",
        "data_cadastro",
        "status_cliente",
    ],
    "planos": [
        "plano_id",
        "nome_plano",
        "valor_mensal",
        "limite_usuarios",
        "categoria_plano",
    ],
    "assinaturas": [
        "assinatura_id",
        "cliente_id",
        "plano_id",
        "data_inicio",
        "data_fim",
        "status_assinatura",
    ],
    "pagamentos": [
        "pagamento_id",
        "assinatura_id",
        "cliente_id",
        "data_pagamento",
        "mes_referencia",
        "valor_pago",
        "status_pagamento",
        "metodo_pagamento",
    ],
    "campanhas_marketing": [
        "campanha_id",
        "nome_campanha",
        "canal",
        "data_inicio",
        "data_fim",
        "investimento",
        "leads_gerados",
        "clientes_convertidos",
    ],
    "tickets_suporte": [
        "ticket_id",
        "cliente_id",
        "data_abertura",
        "data_fechamento",
        "categoria",
        "prioridade",
        "status_ticket",
        "tempo_resolucao_horas",
        "satisfacao_cliente",
    ],
    "eventos_uso": [
        "evento_id",
        "cliente_id",
        "data_evento",
        "tipo_evento",
        "quantidade_eventos",
    ],
}


CHAVES_PRIMARIAS = {
    "clientes": "cliente_id",
    "planos": "plano_id",
    "assinaturas": "assinatura_id",
    "pagamentos": "pagamento_id",
    "campanhas_marketing": "campanha_id",
    "tickets_suporte": "ticket_id",
    "eventos_uso": "evento_id",
}


def carregar_tabelas() -> dict[str, pd.DataFrame]:
    """Carrega todos os arquivos tratados esperados."""
    tabelas = {}
    for tabela in SCHEMAS_ESPERADOS:
        caminho = PROCESSED_DIR / f"{tabela}.csv"
        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo tratado não encontrado: {caminho}")
        tabelas[tabela] = pd.read_csv(caminho)

    return tabelas


def criar_resultado(
    tabela: str,
    validacao: str,
    status: str,
    severidade: str,
    quantidade_problemas: int,
    detalhes: str,
) -> dict[str, Any]:
    """Cria um registro padronizado para o relatório de qualidade."""
    return {
        "tabela": tabela,
        "validacao": validacao,
        "status": status,
        "severidade": severidade,
        "quantidade_problemas": int(quantidade_problemas),
        "detalhes": detalhes,
    }


def validar_estrutura(tabela: str, dados: pd.DataFrame) -> list[dict[str, Any]]:
    """Valida colunas, nulos, duplicidades e tipos identificados."""
    esperadas = SCHEMAS_ESPERADOS[tabela]
    existentes = list(dados.columns)
    faltantes = [coluna for coluna in esperadas if coluna not in existentes]
    extras = [coluna for coluna in existentes if coluna not in esperadas]
    nulos = dados.isna().sum()
    nulos_com_problema = {coluna: int(total) for coluna, total in nulos.items() if total > 0}
    percentual_nulos = {
        coluna: round((total / len(dados)) * 100, 2) if len(dados) else 0.0
        for coluna, total in nulos.items()
        if total > 0
    }
    duplicidades = int(dados.duplicated().sum())
    tipos = {coluna: str(tipo) for coluna, tipo in dados.dtypes.items()}

    resultados = [
        criar_resultado(
            tabela,
            "quantidade_linhas_colunas",
            "OK",
            "INFORMATIVO",
            0,
            f"{len(dados)} linhas e {len(dados.columns)} colunas.",
        ),
        criar_resultado(
            tabela,
            "colunas_esperadas",
            "OK" if not faltantes and not extras else "FALHA",
            "CRÍTICO" if faltantes else "ALERTA" if extras else "INFORMATIVO",
            len(faltantes) + len(extras),
            f"faltantes={faltantes}; extras={extras}",
        ),
        criar_resultado(
            tabela,
            "valores_nulos",
            "OK" if not nulos_com_problema else "ALERTA",
            "ALERTA" if nulos_com_problema else "INFORMATIVO",
            sum(nulos_com_problema.values()),
            f"nulos={nulos_com_problema}; percentual={percentual_nulos}",
        ),
        criar_resultado(
            tabela,
            "duplicidades_exatas",
            "OK" if duplicidades == 0 else "FALHA",
            "CRÍTICO" if duplicidades else "INFORMATIVO",
            duplicidades,
            f"{duplicidades} linha(s) duplicada(s).",
        ),
        criar_resultado(
            tabela,
            "tipos_identificados",
            "OK",
            "INFORMATIVO",
            0,
            json.dumps(tipos, ensure_ascii=False),
        ),
    ]

    return resultados


def validar_chaves_primarias(tabelas: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    """Valida unicidade e preenchimento das chaves primárias esperadas."""
    resultados = []

    for tabela, coluna in CHAVES_PRIMARIAS.items():
        dados = tabelas[tabela]
        nulos = int(dados[coluna].isna().sum())
        duplicados = int(dados[coluna].duplicated().sum())
        problemas = nulos + duplicados
        status = "OK" if problemas == 0 else "FALHA"

        resultados.append(
            criar_resultado(
                tabela,
                f"chave_primaria_{coluna}",
                status,
                "CRÍTICO" if problemas else "INFORMATIVO",
                problemas,
                f"nulos={nulos}; duplicados={duplicados}",
            )
        )

    return resultados


def validar_referencia(
    tabelas: dict[str, pd.DataFrame],
    tabela_origem: str,
    coluna_origem: str,
    tabela_referencia: str,
    coluna_referencia: str,
) -> dict[str, Any]:
    """Valida se os IDs de origem existem na tabela de referência."""
    origem = set(tabelas[tabela_origem][coluna_origem].dropna())
    referencia = set(tabelas[tabela_referencia][coluna_referencia].dropna())
    ausentes = sorted(origem - referencia)
    detalhes = f"{tabela_origem}.{coluna_origem} -> {tabela_referencia}.{coluna_referencia}"

    if ausentes:
        exemplos = ", ".join(str(valor) for valor in ausentes[:5])
        detalhes = f"{detalhes}; exemplos_sem_referencia={exemplos}"

    return criar_resultado(
        tabela_origem,
        f"integridade_{coluna_origem}",
        "OK" if not ausentes else "FALHA",
        "CRÍTICO" if ausentes else "INFORMATIVO",
        len(ausentes),
        detalhes,
    )


def validar_integridade_referencial(tabelas: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    """Executa validações entre tabelas relacionadas."""
    return [
        validar_referencia(tabelas, "assinaturas", "cliente_id", "clientes", "cliente_id"),
        validar_referencia(tabelas, "assinaturas", "plano_id", "planos", "plano_id"),
        validar_referencia(tabelas, "pagamentos", "assinatura_id", "assinaturas", "assinatura_id"),
        validar_referencia(tabelas, "pagamentos", "cliente_id", "clientes", "cliente_id"),
        validar_referencia(tabelas, "tickets_suporte", "cliente_id", "clientes", "cliente_id"),
        validar_referencia(tabelas, "eventos_uso", "cliente_id", "clientes", "cliente_id"),
    ]


def contar_condicao(condicao: pd.Series) -> int:
    """Conta ocorrências verdadeiras em uma regra de qualidade."""
    return int(condicao.fillna(False).sum())


def resultado_regra(tabela: str, regra: str, problemas: int, detalhes: str) -> dict[str, Any]:
    """Cria o resultado de uma regra de negócio."""
    return criar_resultado(
        tabela,
        regra,
        "OK" if problemas == 0 else "FALHA",
        "CRÍTICO" if problemas else "INFORMATIVO",
        problemas,
        detalhes,
    )


def validar_regras_negocio(tabelas: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    """Valida regras de negócio simples nos dados tratados."""
    planos = tabelas["planos"]
    pagamentos = tabelas["pagamentos"]
    campanhas = tabelas["campanhas_marketing"]
    tickets = tabelas["tickets_suporte"]
    eventos = tabelas["eventos_uso"]
    assinaturas = tabelas["assinaturas"]

    data_inicio_assinatura = pd.to_datetime(assinaturas["data_inicio"], errors="coerce")
    data_fim_assinatura = pd.to_datetime(assinaturas["data_fim"], errors="coerce")
    data_abertura = pd.to_datetime(tickets["data_abertura"], errors="coerce")
    data_fechamento = pd.to_datetime(tickets["data_fechamento"], errors="coerce")
    data_inicio_campanha = pd.to_datetime(campanhas["data_inicio"], errors="coerce")
    data_fim_campanha = pd.to_datetime(campanhas["data_fim"], errors="coerce")

    return [
        resultado_regra(
            "planos",
            "valor_mensal_maior_que_zero",
            contar_condicao(planos["valor_mensal"] <= 0),
            "valor_mensal não pode ser menor ou igual a zero.",
        ),
        resultado_regra(
            "pagamentos",
            "valor_pago_nao_negativo",
            contar_condicao(pagamentos["valor_pago"] < 0),
            "valor_pago não pode ser negativo.",
        ),
        resultado_regra(
            "campanhas_marketing",
            "investimento_nao_negativo",
            contar_condicao(campanhas["investimento"] < 0),
            "investimento não pode ser negativo.",
        ),
        resultado_regra(
            "campanhas_marketing",
            "leads_gerados_nao_negativo",
            contar_condicao(campanhas["leads_gerados"] < 0),
            "leads_gerados não pode ser negativo.",
        ),
        resultado_regra(
            "campanhas_marketing",
            "clientes_convertidos_nao_negativo",
            contar_condicao(campanhas["clientes_convertidos"] < 0),
            "clientes_convertidos não pode ser negativo.",
        ),
        resultado_regra(
            "campanhas_marketing",
            "clientes_convertidos_ate_leads",
            contar_condicao(campanhas["clientes_convertidos"] > campanhas["leads_gerados"]),
            "clientes_convertidos não pode ser maior que leads_gerados.",
        ),
        resultado_regra(
            "tickets_suporte",
            "tempo_resolucao_nao_negativo",
            contar_condicao(tickets["tempo_resolucao_horas"] < 0),
            "tempo_resolucao_horas não pode ser negativo.",
        ),
        resultado_regra(
            "tickets_suporte",
            "satisfacao_cliente_entre_1_e_5",
            contar_condicao(tickets["satisfacao_cliente"].notna() & ~tickets["satisfacao_cliente"].between(1, 5)),
            "satisfacao_cliente deve estar entre 1 e 5 quando existir.",
        ),
        resultado_regra(
            "eventos_uso",
            "quantidade_eventos_nao_negativa",
            contar_condicao(eventos["quantidade_eventos"] < 0),
            "quantidade_eventos não pode ser negativa.",
        ),
        resultado_regra(
            "assinaturas",
            "data_fim_assinatura_apos_inicio",
            contar_condicao(data_fim_assinatura.notna() & (data_fim_assinatura < data_inicio_assinatura)),
            "data_fim não pode ser anterior à data_inicio.",
        ),
        resultado_regra(
            "tickets_suporte",
            "data_fechamento_apos_abertura",
            contar_condicao(data_fechamento.notna() & (data_fechamento < data_abertura)),
            "data_fechamento não pode ser anterior à data_abertura.",
        ),
        resultado_regra(
            "campanhas_marketing",
            "data_fim_campanha_apos_inicio",
            contar_condicao(data_fim_campanha < data_inicio_campanha),
            "data_fim de campanha não pode ser anterior à data_inicio.",
        ),
    ]


def executar_validacoes(tabelas: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    """Executa todas as validações de qualidade."""
    resultados = []

    for tabela, dados in tabelas.items():
        resultados.extend(validar_estrutura(tabela, dados))

    resultados.extend(validar_chaves_primarias(tabelas))
    resultados.extend(validar_integridade_referencial(tabelas))
    resultados.extend(validar_regras_negocio(tabelas))

    return resultados


def contar_por(resultados: list[dict[str, Any]], campo: str, valor: str) -> int:
    """Conta resultados por status ou severidade."""
    return sum(1 for resultado in resultados if resultado[campo] == valor)


def salvar_json(resultados: list[dict[str, Any]]) -> None:
    """Salva o relatório estruturado em JSON."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    conteudo = {
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "total_validacoes": len(resultados),
        "resultados": resultados,
    }
    JSON_REPORT.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")


def separar_por_severidade(resultados: list[dict[str, Any]], severidade: str) -> list[dict[str, Any]]:
    """Filtra resultados por severidade."""
    return [resultado for resultado in resultados if resultado["severidade"] == severidade]


def formatar_lista_resultados(resultados: list[dict[str, Any]]) -> str:
    """Formata uma lista de validações para o relatório Markdown."""
    if not resultados:
        return "- Nenhuma ocorrência.\n"

    linhas = []
    for resultado in resultados:
        linhas.append(
            f"- `{resultado['tabela']}` | {resultado['validacao']} | "
            f"status={resultado['status']} | problemas={resultado['quantidade_problemas']} | "
            f"{resultado['detalhes']}"
        )
    return "\n".join(linhas) + "\n"


def definir_conclusao(resultados: list[dict[str, Any]]) -> str:
    """Define a conclusão geral do relatório."""
    criticos = [
        resultado
        for resultado in resultados
        if resultado["severidade"] == "CRÍTICO" and resultado["quantidade_problemas"] > 0
    ]
    if criticos:
        return "Os dados ainda não estão aptos para a próxima etapa, pois existem problemas críticos."

    return "Os dados estão aptos para a próxima etapa do projeto."


def salvar_markdown(resultados: list[dict[str, Any]], tabelas: dict[str, pd.DataFrame]) -> None:
    """Gera o relatório de qualidade em Markdown."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    gerado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    criticos = separar_por_severidade(resultados, "CRÍTICO")
    alertas = separar_por_severidade(resultados, "ALERTA")
    informativos = separar_por_severidade(resultados, "INFORMATIVO")
    criticos_com_problema = [item for item in criticos if item["quantidade_problemas"] > 0]
    alertas_com_problema = [item for item in alertas if item["quantidade_problemas"] > 0]
    conclusao = definir_conclusao(resultados)

    texto = f"""# Relatório de qualidade dos dados

Data/hora da execução: {gerado_em}

## Resumo executivo

- Tabelas avaliadas: {len(tabelas)}
- Total de validações executadas: {len(resultados)}
- Validações aprovadas: {contar_por(resultados, "status", "OK")}
- Alertas com ocorrência: {len(alertas_com_problema)}
- Problemas críticos com ocorrência: {len(criticos_com_problema)}

## Tabelas avaliadas

{formatar_lista_resultados([
    criar_resultado(nome, "volume_tabela", "OK", "INFORMATIVO", 0, f"{len(dados)} linhas e {len(dados.columns)} colunas.")
    for nome, dados in tabelas.items()
])}
## Principais problemas encontrados

{formatar_lista_resultados(criticos_com_problema + alertas_com_problema)}
## Validações críticas

{formatar_lista_resultados(criticos)}
## Validações de alerta

{formatar_lista_resultados(alertas)}
## Observações informativas

{formatar_lista_resultados(informativos)}
## Conclusão geral

{conclusao}
"""

    MARKDOWN_REPORT.write_text(texto, encoding="utf-8")


def imprimir_resumo(resultados: list[dict[str, Any]], tabelas: dict[str, pd.DataFrame]) -> None:
    """Exibe um resumo claro da execução no terminal."""
    criticos_com_problema = [
        resultado
        for resultado in resultados
        if resultado["severidade"] == "CRÍTICO" and resultado["quantidade_problemas"] > 0
    ]
    alertas_com_problema = [
        resultado
        for resultado in resultados
        if resultado["severidade"] == "ALERTA" and resultado["quantidade_problemas"] > 0
    ]

    print("\nResumo da qualidade dos dados:")
    print(f"- Tabelas avaliadas: {len(tabelas)}")
    print(f"- Total de validações executadas: {len(resultados)}")
    print(f"- Validações aprovadas: {contar_por(resultados, 'status', 'OK')}")
    print(f"- Alertas: {len(alertas_com_problema)}")
    print(f"- Problemas críticos: {len(criticos_com_problema)}")
    print(f"- Relatório JSON: {JSON_REPORT}")
    print(f"- Relatório Markdown: {MARKDOWN_REPORT}")


def main() -> None:
    """Executa a validação de qualidade dos dados tratados."""
    tabelas = carregar_tabelas()
    resultados = executar_validacoes(tabelas)
    salvar_json(resultados)
    salvar_markdown(resultados, tabelas)
    imprimir_resumo(resultados, tabelas)


if __name__ == "__main__":
    main()
