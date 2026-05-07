"""Gera dados sintéticos para simular uma empresa SaaS corporativa.

O script cria bases relacionais simples para clientes, planos, assinaturas,
pagamentos, campanhas de marketing, tickets de suporte e eventos de uso.
Os arquivos completos são salvos em ``data/raw`` e amostras menores em
``data/sample`` para facilitar a visualização no GitHub.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
ANO_REFERENCIA = 2025
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
SAMPLE_DIR = BASE_DIR / "data" / "sample"


def garantir_pastas() -> None:
    """Garante que as pastas de saída existam antes de salvar os arquivos."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)


def escolher_datas(rng: np.random.Generator, inicio: str, fim: str, quantidade: int) -> pd.Series:
    """Sorteia datas dentro de um intervalo fechado."""
    datas = pd.date_range(inicio, fim, freq="D")
    escolhas = rng.choice(datas, size=quantidade, replace=True)
    return pd.Series(escolhas).sort_values(ignore_index=True)


def gerar_nome_empresas(rng: np.random.Generator, quantidade: int) -> list[str]:
    """Cria nomes fictícios com aparência de empresas brasileiras."""
    prefixos = [
        "Atlas",
        "Nexa",
        "Vértice",
        "Lumina",
        "Horizonte",
        "Vector",
        "Orion",
        "Sinergia",
        "Auge",
        "Prisma",
        "Datta",
        "Conecta",
    ]
    atividades = [
        "Tecnologia",
        "Soluções",
        "Consultoria",
        "Serviços",
        "Digital",
        "Sistemas",
        "Gestão",
        "Analytics",
        "Cloud",
        "Operações",
    ]
    sufixos = ["Ltda", "S.A.", "Brasil", "Group", "Corporativo", "Enterprise"]

    nomes = []
    nomes_usados = set()
    while len(nomes) < quantidade:
        nome = (
            f"{rng.choice(prefixos)} {rng.choice(atividades)} "
            f"{rng.choice(sufixos)} {rng.integers(10, 99)}"
        )
        if nome not in nomes_usados:
            nomes.append(nome)
            nomes_usados.add(nome)

    return nomes


def gerar_clientes(rng: np.random.Generator, quantidade: int = 500) -> pd.DataFrame:
    """Gera a base de clientes corporativos da empresa SaaS."""
    cidades_estados = [
        ("Recife", "PE"),
        ("Olinda", "PE"),
        ("Jaboatão dos Guararapes", "PE"),
        ("São Paulo", "SP"),
        ("Campinas", "SP"),
        ("Rio de Janeiro", "RJ"),
        ("Belo Horizonte", "MG"),
        ("Curitiba", "PR"),
        ("Porto Alegre", "RS"),
        ("Salvador", "BA"),
        ("Fortaleza", "CE"),
        ("Brasília", "DF"),
        ("Goiânia", "GO"),
        ("Florianópolis", "SC"),
    ]
    segmentos = [
        "Tecnologia",
        "Saúde",
        "Educação",
        "Varejo",
        "Indústria",
        "Serviços financeiros",
        "Logística",
        "Energia",
        "Telecomunicações",
        "Consultoria",
    ]
    portes = ["Pequena", "Média", "Grande"]
    nomes = gerar_nome_empresas(rng, quantidade)
    locais = rng.choice(len(cidades_estados), size=quantidade, replace=True)

    clientes = pd.DataFrame(
        {
            "cliente_id": [f"CLI{i:04d}" for i in range(1, quantidade + 1)],
            "nome_empresa": nomes,
            "segmento": rng.choice(segmentos, size=quantidade, replace=True),
            "porte_empresa": rng.choice(portes, size=quantidade, replace=True, p=[0.48, 0.36, 0.16]),
            "cidade": [cidades_estados[i][0] for i in locais],
            "estado": [cidades_estados[i][1] for i in locais],
            "data_cadastro": escolher_datas(rng, "2022-01-01", "2025-03-31", quantidade),
            "status_cliente": "ativo",
        }
    )

    clientes["data_cadastro"] = clientes["data_cadastro"].dt.date.astype(str)
    return clientes


def gerar_planos() -> pd.DataFrame:
    """Gera a tabela de planos comerciais disponíveis para contratação."""
    return pd.DataFrame(
        [
            ["PLA001", "Essencial", 199.00, 10, "Entrada"],
            ["PLA002", "Profissional", 499.00, 35, "Crescimento"],
            ["PLA003", "Business", 899.00, 80, "Crescimento"],
            ["PLA004", "Enterprise", 1499.00, 200, "Corporativo"],
            ["PLA005", "Corporativo Plus", 2499.00, 500, "Corporativo"],
        ],
        columns=["plano_id", "nome_plano", "valor_mensal", "limite_usuarios", "categoria_plano"],
    )


def gerar_assinaturas(
    rng: np.random.Generator,
    clientes: pd.DataFrame,
    planos: pd.DataFrame,
    quantidade: int = 650,
) -> pd.DataFrame:
    """Gera assinaturas vinculadas a clientes e planos existentes."""
    cliente_ids = clientes["cliente_id"].to_numpy()
    plano_ids = planos["plano_id"].to_numpy()
    datas_inicio = escolher_datas(rng, "2023-01-01", "2025-12-01", quantidade)
    status = rng.choice(
        ["ativa", "cancelada", "expirada"],
        size=quantidade,
        replace=True,
        p=[0.72, 0.20, 0.08],
    )

    assinaturas = pd.DataFrame(
        {
            "assinatura_id": [f"ASS{i:06d}" for i in range(1, quantidade + 1)],
            "cliente_id": rng.choice(cliente_ids, size=quantidade, replace=True),
            "plano_id": rng.choice(plano_ids, size=quantidade, replace=True, p=[0.28, 0.32, 0.22, 0.13, 0.05]),
            "data_inicio": datas_inicio,
            "data_fim": pd.NaT,
            "status_assinatura": status,
        }
    )

    # Datas de fim só existem para assinaturas que não continuam ativas.
    mascara_encerradas = assinaturas["status_assinatura"].isin(["cancelada", "expirada"])
    for indice in assinaturas[mascara_encerradas].index:
        inicio = assinaturas.loc[indice, "data_inicio"]
        dias_ativos = int(rng.integers(60, 900))
        data_fim = min(inicio + pd.Timedelta(days=dias_ativos), pd.Timestamp(f"{ANO_REFERENCIA}-12-31"))
        assinaturas.loc[indice, "data_fim"] = data_fim

    assinaturas["data_inicio"] = assinaturas["data_inicio"].dt.date.astype(str)
    assinaturas["data_fim"] = pd.to_datetime(assinaturas["data_fim"]).dt.date.astype("string").fillna("")
    return assinaturas


def atualizar_status_clientes(clientes: pd.DataFrame, assinaturas: pd.DataFrame) -> pd.DataFrame:
    """Atualiza o status do cliente com base na situação das assinaturas."""
    clientes = clientes.copy()
    clientes_com_assinatura_ativa = set(
        assinaturas.loc[assinaturas["status_assinatura"] == "ativa", "cliente_id"]
    )
    clientes_com_assinatura = set(assinaturas["cliente_id"])

    clientes["status_cliente"] = clientes["cliente_id"].apply(
        lambda cliente_id: "ativo"
        if cliente_id in clientes_com_assinatura_ativa
        else "cancelado"
        if cliente_id in clientes_com_assinatura
        else "prospect"
    )
    return clientes


def gerar_pagamentos(
    rng: np.random.Generator,
    assinaturas: pd.DataFrame,
    planos: pd.DataFrame,
) -> pd.DataFrame:
    """Gera pagamentos mensais de 12 meses para assinaturas elegíveis."""
    valores_planos = planos.set_index("plano_id")["valor_mensal"].to_dict()
    meses = pd.period_range(f"{ANO_REFERENCIA}-01", f"{ANO_REFERENCIA}-12", freq="M")
    registros = []

    for _, assinatura in assinaturas.iterrows():
        inicio = pd.Timestamp(assinatura["data_inicio"])
        fim = pd.Timestamp(assinatura["data_fim"]) if assinatura["data_fim"] else pd.Timestamp(f"{ANO_REFERENCIA}-12-31")

        for mes in meses:
            primeiro_dia = mes.to_timestamp()
            ultimo_dia = primeiro_dia + pd.offsets.MonthEnd(0)

            if inicio > ultimo_dia or fim < primeiro_dia:
                continue

            status_pagamento = rng.choice(["pago", "atrasado", "inadimplente"], p=[0.86, 0.08, 0.06])
            valor_base = float(valores_planos[assinatura["plano_id"]])
            ajuste = rng.normal(1.0, 0.015)
            valor_pago = round(valor_base * ajuste, 2) if status_pagamento != "inadimplente" else 0.00

            if status_pagamento == "inadimplente":
                data_pagamento = ""
            else:
                atraso_dias = int(rng.integers(1, 8)) if status_pagamento == "pago" else int(rng.integers(12, 35))
                data_pagamento = (ultimo_dia + pd.Timedelta(days=atraso_dias)).date().isoformat()

            registros.append(
                {
                    "pagamento_id": f"PAG{len(registros) + 1:07d}",
                    "assinatura_id": assinatura["assinatura_id"],
                    "cliente_id": assinatura["cliente_id"],
                    "data_pagamento": data_pagamento,
                    "mes_referencia": str(mes),
                    "valor_pago": valor_pago,
                    "status_pagamento": status_pagamento,
                    "metodo_pagamento": rng.choice(["boleto", "cartao_credito", "pix", "transferencia"]),
                }
            )

    return pd.DataFrame(registros)


def gerar_campanhas_marketing(rng: np.random.Generator, quantidade: int = 18) -> pd.DataFrame:
    """Gera campanhas de marketing para análise de aquisição."""
    canais = ["LinkedIn Ads", "Google Ads", "Eventos", "Webinar", "E-mail marketing", "Indicação"]
    temas = ["Aquisição B2B", "Retenção", "Expansão Enterprise", "Porto Digital", "Transformação Digital"]
    datas_inicio = escolher_datas(rng, "2025-01-01", "2025-10-31", quantidade)
    registros = []

    for i in range(quantidade):
        investimento = round(float(rng.uniform(8000, 65000)), 2)
        leads = int(rng.integers(120, 1800))
        taxa_conversao = float(rng.uniform(0.025, 0.14))

        registros.append(
            {
                "campanha_id": f"CAM{i + 1:03d}",
                "nome_campanha": f"{rng.choice(temas)} {i + 1:02d}",
                "canal": rng.choice(canais),
                "data_inicio": datas_inicio.iloc[i].date().isoformat(),
                "data_fim": (datas_inicio.iloc[i] + pd.Timedelta(days=int(rng.integers(20, 70)))).date().isoformat(),
                "investimento": investimento,
                "leads_gerados": leads,
                "clientes_convertidos": max(1, int(leads * taxa_conversao)),
            }
        )

    return pd.DataFrame(registros)


def gerar_tickets_suporte(
    rng: np.random.Generator,
    clientes: pd.DataFrame,
    quantidade: int = 1200,
) -> pd.DataFrame:
    """Gera tickets de suporte associados a clientes existentes."""
    categorias = ["acesso", "financeiro", "integracao", "performance", "duvida_funcional", "bug"]
    prioridades = ["baixa", "media", "alta", "critica"]
    clientes_ids = clientes["cliente_id"].to_numpy()
    datas_abertura = escolher_datas(rng, "2025-01-01", "2025-12-15", quantidade)
    registros = []

    for i in range(quantidade):
        prioridade = rng.choice(prioridades, p=[0.40, 0.36, 0.18, 0.06])
        status_ticket = rng.choice(["fechado", "em_atendimento", "aberto"], p=[0.82, 0.12, 0.06])
        horas_base = {"baixa": 72, "media": 36, "alta": 16, "critica": 6}[prioridade]
        abertura = datas_abertura.iloc[i]

        if status_ticket == "fechado":
            tempo_resolucao = round(float(max(1, rng.normal(horas_base, horas_base * 0.35))), 1)
            fechamento = (abertura + pd.Timedelta(hours=tempo_resolucao)).isoformat()
            satisfacao = int(rng.choice([1, 2, 3, 4, 5], p=[0.04, 0.08, 0.18, 0.38, 0.32]))
        else:
            tempo_resolucao = np.nan
            fechamento = ""
            satisfacao = np.nan

        registros.append(
            {
                "ticket_id": f"TIC{i + 1:06d}",
                "cliente_id": rng.choice(clientes_ids),
                "data_abertura": abertura.date().isoformat(),
                "data_fechamento": fechamento,
                "categoria": rng.choice(categorias),
                "prioridade": prioridade,
                "status_ticket": status_ticket,
                "tempo_resolucao_horas": tempo_resolucao,
                "satisfacao_cliente": satisfacao,
            }
        )

    return pd.DataFrame(registros)


def gerar_eventos_uso(
    rng: np.random.Generator,
    clientes: pd.DataFrame,
    quantidade: int = 6000,
) -> pd.DataFrame:
    """Gera eventos agregados de uso da plataforma por cliente e data."""
    tipos_evento = ["login", "relatorio_exportado", "dashboard_visualizado", "usuario_criado", "integracao_executada"]
    clientes_ids = clientes["cliente_id"].to_numpy()
    datas_evento = escolher_datas(rng, "2025-01-01", "2025-12-31", quantidade)
    pesos_eventos = {
        "login": (10, 80),
        "relatorio_exportado": (1, 18),
        "dashboard_visualizado": (3, 45),
        "usuario_criado": (1, 8),
        "integracao_executada": (2, 30),
    }
    registros = []

    for i in range(quantidade):
        tipo_evento = rng.choice(tipos_evento, p=[0.34, 0.18, 0.28, 0.08, 0.12])
        minimo, maximo = pesos_eventos[tipo_evento]
        registros.append(
            {
                "evento_id": f"EVT{i + 1:07d}",
                "cliente_id": rng.choice(clientes_ids),
                "data_evento": datas_evento.iloc[i].date().isoformat(),
                "tipo_evento": tipo_evento,
                "quantidade_eventos": int(rng.integers(minimo, maximo)),
            }
        )

    return pd.DataFrame(registros)


def salvar_tabelas(tabelas: dict[str, pd.DataFrame], tamanho_amostra: int = 30) -> list[dict[str, object]]:
    """Salva as tabelas completas e suas amostras em CSV."""
    resumo = []

    for nome_arquivo, tabela in tabelas.items():
        caminho_raw = RAW_DIR / nome_arquivo
        caminho_sample = SAMPLE_DIR / nome_arquivo

        tabela.to_csv(caminho_raw, index=False, encoding="utf-8")
        tabela.head(tamanho_amostra).to_csv(caminho_sample, index=False, encoding="utf-8")

        resumo.append({"arquivo": nome_arquivo, "linhas": len(tabela), "caminho": caminho_raw})
        resumo.append(
            {
                "arquivo": f"sample/{nome_arquivo}",
                "linhas": min(tamanho_amostra, len(tabela)),
                "caminho": caminho_sample,
            }
        )

    return resumo


def gerar_todas_as_tabelas() -> dict[str, pd.DataFrame]:
    """Executa a geração completa das tabelas sintéticas."""
    rng = np.random.default_rng(SEED)

    clientes = gerar_clientes(rng)
    planos = gerar_planos()
    assinaturas = gerar_assinaturas(rng, clientes, planos)
    clientes = atualizar_status_clientes(clientes, assinaturas)
    pagamentos = gerar_pagamentos(rng, assinaturas, planos)
    campanhas = gerar_campanhas_marketing(rng)
    tickets = gerar_tickets_suporte(rng, clientes)
    eventos = gerar_eventos_uso(rng, clientes)

    return {
        "clientes.csv": clientes,
        "planos.csv": planos,
        "assinaturas.csv": assinaturas,
        "pagamentos.csv": pagamentos,
        "campanhas_marketing.csv": campanhas,
        "tickets_suporte.csv": tickets,
        "eventos_uso.csv": eventos,
    }


def imprimir_resumo(resumo: list[dict[str, object]]) -> None:
    """Exibe no terminal os arquivos criados pelo script."""
    print("\nArquivos gerados:")
    for item in resumo:
        print(f"- {item['arquivo']}: {item['linhas']} linhas | {item['caminho']}")


def main() -> None:
    """Ponto de entrada para execução direta do script."""
    garantir_pastas()
    tabelas = gerar_todas_as_tabelas()
    resumo = salvar_tabelas(tabelas)
    imprimir_resumo(resumo)


if __name__ == "__main__":
    main()
