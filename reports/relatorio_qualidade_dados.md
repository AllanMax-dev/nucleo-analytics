# Relatório de qualidade dos dados

Data/hora da execução: 2026-05-07 14:29:23

## Resumo executivo

- Tabelas avaliadas: 7
- Total de validações executadas: 60
- Validações aprovadas: 57
- Alertas com ocorrência: 3
- Problemas críticos com ocorrência: 0

## Tabelas avaliadas

- `clientes` | volume_tabela | status=OK | problemas=0 | 500 linhas e 8 colunas.
- `planos` | volume_tabela | status=OK | problemas=0 | 5 linhas e 5 colunas.
- `assinaturas` | volume_tabela | status=OK | problemas=0 | 650 linhas e 6 colunas.
- `pagamentos` | volume_tabela | status=OK | problemas=0 | 5810 linhas e 8 colunas.
- `campanhas_marketing` | volume_tabela | status=OK | problemas=0 | 18 linhas e 8 colunas.
- `tickets_suporte` | volume_tabela | status=OK | problemas=0 | 1200 linhas e 9 colunas.
- `eventos_uso` | volume_tabela | status=OK | problemas=0 | 6000 linhas e 5 colunas.

## Principais problemas encontrados

- `assinaturas` | valores_nulos | status=ALERTA | problemas=468 | nulos={'data_fim': 468}; percentual={'data_fim': 72.0}
- `pagamentos` | valores_nulos | status=ALERTA | problemas=359 | nulos={'data_pagamento': 359}; percentual={'data_pagamento': 6.18}
- `tickets_suporte` | valores_nulos | status=ALERTA | problemas=600 | nulos={'data_fechamento': 200, 'tempo_resolucao_horas': 200, 'satisfacao_cliente': 200}; percentual={'data_fechamento': 16.67, 'tempo_resolucao_horas': 16.67, 'satisfacao_cliente': 16.67}

## Validações críticas

- Nenhuma ocorrência.

## Validações de alerta

- `assinaturas` | valores_nulos | status=ALERTA | problemas=468 | nulos={'data_fim': 468}; percentual={'data_fim': 72.0}
- `pagamentos` | valores_nulos | status=ALERTA | problemas=359 | nulos={'data_pagamento': 359}; percentual={'data_pagamento': 6.18}
- `tickets_suporte` | valores_nulos | status=ALERTA | problemas=600 | nulos={'data_fechamento': 200, 'tempo_resolucao_horas': 200, 'satisfacao_cliente': 200}; percentual={'data_fechamento': 16.67, 'tempo_resolucao_horas': 16.67, 'satisfacao_cliente': 16.67}

## Observações informativas

- `clientes` | quantidade_linhas_colunas | status=OK | problemas=0 | 500 linhas e 8 colunas.
- `clientes` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `clientes` | valores_nulos | status=OK | problemas=0 | nulos={}; percentual={}
- `clientes` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `clientes` | tipos_identificados | status=OK | problemas=0 | {"cliente_id": "str", "nome_empresa": "str", "segmento": "str", "porte_empresa": "str", "cidade": "str", "estado": "str", "data_cadastro": "str", "status_cliente": "str"}
- `planos` | quantidade_linhas_colunas | status=OK | problemas=0 | 5 linhas e 5 colunas.
- `planos` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `planos` | valores_nulos | status=OK | problemas=0 | nulos={}; percentual={}
- `planos` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `planos` | tipos_identificados | status=OK | problemas=0 | {"plano_id": "str", "nome_plano": "str", "valor_mensal": "float64", "limite_usuarios": "int64", "categoria_plano": "str"}
- `assinaturas` | quantidade_linhas_colunas | status=OK | problemas=0 | 650 linhas e 6 colunas.
- `assinaturas` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `assinaturas` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `assinaturas` | tipos_identificados | status=OK | problemas=0 | {"assinatura_id": "str", "cliente_id": "str", "plano_id": "str", "data_inicio": "str", "data_fim": "str", "status_assinatura": "str"}
- `pagamentos` | quantidade_linhas_colunas | status=OK | problemas=0 | 5810 linhas e 8 colunas.
- `pagamentos` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `pagamentos` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `pagamentos` | tipos_identificados | status=OK | problemas=0 | {"pagamento_id": "str", "assinatura_id": "str", "cliente_id": "str", "data_pagamento": "str", "mes_referencia": "str", "valor_pago": "float64", "status_pagamento": "str", "metodo_pagamento": "str"}
- `campanhas_marketing` | quantidade_linhas_colunas | status=OK | problemas=0 | 18 linhas e 8 colunas.
- `campanhas_marketing` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `campanhas_marketing` | valores_nulos | status=OK | problemas=0 | nulos={}; percentual={}
- `campanhas_marketing` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `campanhas_marketing` | tipos_identificados | status=OK | problemas=0 | {"campanha_id": "str", "nome_campanha": "str", "canal": "str", "data_inicio": "str", "data_fim": "str", "investimento": "float64", "leads_gerados": "int64", "clientes_convertidos": "int64"}
- `tickets_suporte` | quantidade_linhas_colunas | status=OK | problemas=0 | 1200 linhas e 9 colunas.
- `tickets_suporte` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `tickets_suporte` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `tickets_suporte` | tipos_identificados | status=OK | problemas=0 | {"ticket_id": "str", "cliente_id": "str", "data_abertura": "str", "data_fechamento": "str", "categoria": "str", "prioridade": "str", "status_ticket": "str", "tempo_resolucao_horas": "float64", "satisfacao_cliente": "float64"}
- `eventos_uso` | quantidade_linhas_colunas | status=OK | problemas=0 | 6000 linhas e 5 colunas.
- `eventos_uso` | colunas_esperadas | status=OK | problemas=0 | faltantes=[]; extras=[]
- `eventos_uso` | valores_nulos | status=OK | problemas=0 | nulos={}; percentual={}
- `eventos_uso` | duplicidades_exatas | status=OK | problemas=0 | 0 linha(s) duplicada(s).
- `eventos_uso` | tipos_identificados | status=OK | problemas=0 | {"evento_id": "str", "cliente_id": "str", "data_evento": "str", "tipo_evento": "str", "quantidade_eventos": "int64"}
- `clientes` | chave_primaria_cliente_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `planos` | chave_primaria_plano_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `assinaturas` | chave_primaria_assinatura_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `pagamentos` | chave_primaria_pagamento_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `campanhas_marketing` | chave_primaria_campanha_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `tickets_suporte` | chave_primaria_ticket_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `eventos_uso` | chave_primaria_evento_id | status=OK | problemas=0 | nulos=0; duplicados=0
- `assinaturas` | integridade_cliente_id | status=OK | problemas=0 | assinaturas.cliente_id -> clientes.cliente_id
- `assinaturas` | integridade_plano_id | status=OK | problemas=0 | assinaturas.plano_id -> planos.plano_id
- `pagamentos` | integridade_assinatura_id | status=OK | problemas=0 | pagamentos.assinatura_id -> assinaturas.assinatura_id
- `pagamentos` | integridade_cliente_id | status=OK | problemas=0 | pagamentos.cliente_id -> clientes.cliente_id
- `tickets_suporte` | integridade_cliente_id | status=OK | problemas=0 | tickets_suporte.cliente_id -> clientes.cliente_id
- `eventos_uso` | integridade_cliente_id | status=OK | problemas=0 | eventos_uso.cliente_id -> clientes.cliente_id
- `planos` | valor_mensal_maior_que_zero | status=OK | problemas=0 | valor_mensal não pode ser menor ou igual a zero.
- `pagamentos` | valor_pago_nao_negativo | status=OK | problemas=0 | valor_pago não pode ser negativo.
- `campanhas_marketing` | investimento_nao_negativo | status=OK | problemas=0 | investimento não pode ser negativo.
- `campanhas_marketing` | leads_gerados_nao_negativo | status=OK | problemas=0 | leads_gerados não pode ser negativo.
- `campanhas_marketing` | clientes_convertidos_nao_negativo | status=OK | problemas=0 | clientes_convertidos não pode ser negativo.
- `campanhas_marketing` | clientes_convertidos_ate_leads | status=OK | problemas=0 | clientes_convertidos não pode ser maior que leads_gerados.
- `tickets_suporte` | tempo_resolucao_nao_negativo | status=OK | problemas=0 | tempo_resolucao_horas não pode ser negativo.
- `tickets_suporte` | satisfacao_cliente_entre_1_e_5 | status=OK | problemas=0 | satisfacao_cliente deve estar entre 1 e 5 quando existir.
- `eventos_uso` | quantidade_eventos_nao_negativa | status=OK | problemas=0 | quantidade_eventos não pode ser negativa.
- `assinaturas` | data_fim_assinatura_apos_inicio | status=OK | problemas=0 | data_fim não pode ser anterior à data_inicio.
- `tickets_suporte` | data_fechamento_apos_abertura | status=OK | problemas=0 | data_fechamento não pode ser anterior à data_abertura.
- `campanhas_marketing` | data_fim_campanha_apos_inicio | status=OK | problemas=0 | data_fim de campanha não pode ser anterior à data_inicio.

## Conclusão geral

Os dados estão aptos para a próxima etapa do projeto.
