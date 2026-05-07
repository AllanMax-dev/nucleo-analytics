# Dicionário de dados

Este documento vai registrar as tabelas, campos, tipos de dados e descrições utilizadas no projeto.

Nesta versão inicial, o dicionário descreve as bases sintéticas geradas para simular uma operação SaaS corporativa.

## clientes.csv

| Campo | Descrição |
| --- | --- |
| cliente_id | Identificador único do cliente. |
| nome_empresa | Nome fictício da empresa cliente. |
| segmento | Segmento de atuação do cliente. |
| porte_empresa | Porte da empresa: pequena, média ou grande. |
| cidade | Cidade da empresa. |
| estado | Unidade federativa da empresa. |
| data_cadastro | Data em que o cliente entrou na base. |
| status_cliente | Situação do cliente na base. |

## planos.csv

| Campo | Descrição |
| --- | --- |
| plano_id | Identificador único do plano. |
| nome_plano | Nome comercial do plano. |
| valor_mensal | Valor mensal previsto para o plano. |
| limite_usuarios | Quantidade máxima de usuários permitida. |
| categoria_plano | Categoria comercial do plano. |

## assinaturas.csv

| Campo | Descrição |
| --- | --- |
| assinatura_id | Identificador único da assinatura. |
| cliente_id | Cliente associado à assinatura. |
| plano_id | Plano contratado na assinatura. |
| data_inicio | Data de início da assinatura. |
| data_fim | Data de encerramento, quando houver. |
| status_assinatura | Situação da assinatura. |

## pagamentos.csv

| Campo | Descrição |
| --- | --- |
| pagamento_id | Identificador único do pagamento. |
| assinatura_id | Assinatura relacionada ao pagamento. |
| cliente_id | Cliente relacionado ao pagamento. |
| data_pagamento | Data em que o pagamento foi realizado. |
| mes_referencia | Mês de competência do pagamento. |
| valor_pago | Valor recebido. |
| status_pagamento | Situação do pagamento. |
| metodo_pagamento | Meio usado para pagamento. |

## campanhas_marketing.csv

| Campo | Descrição |
| --- | --- |
| campanha_id | Identificador único da campanha. |
| nome_campanha | Nome fictício da campanha. |
| canal | Canal de aquisição utilizado. |
| data_inicio | Data de início da campanha. |
| data_fim | Data de encerramento da campanha. |
| investimento | Valor investido na campanha. |
| leads_gerados | Quantidade de leads gerados. |
| clientes_convertidos | Quantidade de clientes convertidos. |

## tickets_suporte.csv

| Campo | Descrição |
| --- | --- |
| ticket_id | Identificador único do ticket. |
| cliente_id | Cliente que abriu o ticket. |
| data_abertura | Data de abertura do ticket. |
| data_fechamento | Data de fechamento, quando houver. |
| categoria | Categoria do atendimento. |
| prioridade | Prioridade do ticket. |
| status_ticket | Situação atual do ticket. |
| tempo_resolucao_horas | Tempo de resolução em horas. |
| satisfacao_cliente | Nota de satisfação informada pelo cliente. |

## eventos_uso.csv

| Campo | Descrição |
| --- | --- |
| evento_id | Identificador único do evento agregado. |
| cliente_id | Cliente associado ao evento. |
| data_evento | Data em que o uso foi registrado. |
| tipo_evento | Tipo de interação com a plataforma. |
| quantidade_eventos | Quantidade de eventos agregados no registro. |
