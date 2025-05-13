<!-- image -->

## 1. CADASTROS GERAIS

## 1.1. EMPRESAS

Os códigos das empresas seguem o seguinte padrão:

| Faixa numérica   | Descrição                                                                           |
|------------------|-------------------------------------------------------------------------------------|
| X00              | Empresa matriz.                                                                     |
| 110 - 199        | Empresas do grupo JC Thedin Transportes.                                            |
| 210 - 299        | Empresas do grupo TJ4 Transportes.                                                  |
| 310 - 399        | Empresas do grupo JJ Thedin Transportes.                                            |
| 901 - 999        | Transportadoras parceiras contratadas pela Frilog para redespacho / subcontratação. |

Os dois últimos dígitos dos códigos de empresas do grupo devem respeitar a tabela abaixo:

|   Dígito | Localização física da empresa   |
|----------|---------------------------------|
|       10 | Rio de Janeiro / RJ             |
|       11 | Nova Friburgo / RJ              |
|       12 | São Paulo / SP                  |
|       13 | Rio Claro / SP                  |
|       14 | Campinas / SP                   |
|       15 | Itaboraí / RJ                   |
|       16 | São Pedro da Aldeia / RJ        |
|       17 | Itaperuna / RJ                  |
|       18 | Americana / SP                  |
|       19 | Barra Mansa / RJ                |
|       20 | Teresópolis / RJ                |
|       21 | Campos dos Goytacazes / RJ      |

Para a área de RH, as empresas matriz (100, 200 e 300) servem apenas para sinalizar em qual matriz administrativa o colaborador trabalha (Empresa Sistema). Já os registros dos colaboradores devem ser vinculados as outras empresas não matrizes, de acordo com o registro na CTPS.

Atualmente temos registradas as seguintes empresas para emissão de conhecimentos:

| Nome SISLOG   |   Código SENIOR | Empresa               | Unidade        |   Código Prosoft |
|---------------|-----------------|-----------------------|----------------|------------------|
| FRILOG 01     |             211 | TJ4 Transportes       | Nova Friburgo  |               58 |
| FRILOG 02     |             111 | JC Thedin Transportes | Nova Friburgo  |              169 |
| FRILOG 03     |             112 | JC Thedin Transportes | São Paulo      |               29 |
| FRILOG 05     |             215 | TJ4 Transportes       | Itaboraí       |               57 |
| FRILOG 06     |             312 | JJ Thedin Transportes | São Paulo      |              232 |
| FRILOG 07     |             317 | JJ Thedin Transportes | Itaperuna      |              252 |
| FRILOG 09     |             310 | JJ Thedin Transportes | Rio de Janeiro |              253 |
| FRILOG 12     |             210 | TJ4 Transportes       | Rio de Janeiro |              223 |

## NORMAS PARA PADRONIZAÇÃO DE CADASTRO NO ERP SENIOR

ROBERT OLIVEIRA - GERÊNCIA ADMINSITRATIVA   30/08/2017   Versão 1.0 - -

<!-- image -->

## NORMAS PARA PADRONIZAÇÃO DE CADASTRO NO ERP SENIOR

ROBERT OLIVEIRA - GERÊNCIA ADMINSITRATIVA   30/08/2017   Versão 1.0 - -

| FRILOG 13   |   110 | JC Thedin Transportes   | Rio de Janeiro   |   233 |
|-------------|-------|-------------------------|------------------|-------|
| FRILOG 21   |   116 | JC Thedin Transportes   | S. P. da Aldeia  |   171 |
| FRILOG 23   |   113 | JC Thedin Transportes   | Rio Claro        |   313 |
| FRILOG 24   |   214 | TJ4 Transportes         | Campinas         |    56 |

No entanto, para vínculo cadastral de itens do TMS, como clientes, rotas, itinerários e regiões, utilizamos apenas uma empresa por unidade, conforme tabela abaixo.

| Empresa Padrão   | Filial   |
|------------------|----------|
| 211 (TJ4NOF)     | NOF      |
| 112 (JCSAO)      | SÃO      |
| 110 (JCRJO)      | RJO      |
| 317 (JJITA)      | ITA      |
| 215 (TJ4ITB)     | ITB      |
| 116 (JCSPA)      | SPA      |
| 113 (JCRCL)      | RCL      |
| 214 (TJ4CAS)     | CAS      |

## 1.2. REGRAS GERAIS

- 1. Não devem ser usados caracteres especiais. Exemplos: ponto, hífen, parênteses, asterisco, porcentagem, cifrão, etc.
- 2. Exceções para o uso de caracteres especiais:
- a. Barra. Exemplo: S/A, 3/4, etc.
- b. Aspas (quando indica polegadas). Exemplo: 3'
- 3. Acentos, inclusive cedilha, não devem ser utilizados.
- 4. Abreviaturas ou siglas não devem conter espaço. Exemplos: SENAI, TJ4, JC Thedim, 3CTI, PH Fit (note que o espaço está entre as palavras e não dentro da sigla).
- 5. Reforçando a regra 1, não utilize ponto em abreviaturas. Exemplos: XYZ IND E COM (ao invés de XYZ IND. E COM.).
- 6. Utilizar sempre caixa alta (letras maiúsculas).
- 7. A única exceção para o uso de letras maiúsculas é para cadastros de grupos hierárquicos. Os cadastros de nível 0 devem iniciar com primeira letra em maiúscula e o restante em minúsculas. Todos os outros níveis devem ser em caixa alta.
- 8. Placa de veículos deve obedecer à máscara XXX-9999. Exemplos: XYZ-1234, ABC-9876.
- 9. Números telefônicos deve obedecer à máscara 99 9999 9999 (fixo) ou 99 9 9999 9999 (celular). Por exemplo: 22 9 8117 0296, 22 2010 6500.
- 10. O RNTRC (ANTT) deve conter oito dígitos. Se necessário, devem ser preenchidos zeros à esquerda. Exemplos: 00123456, 98765432, 00003456.

## 2. CADASTROS OPERACIONAIS

## 2.1. CODIFICAÇÃO PARA CIDADES E REGIÕES

Todas as cidades atendidas pela Frilog devem ser codificadas em suas respectivas regiões de atendimento, conforme regras estabelecidas abaixo.

<!-- image -->

## Máscara: AA.BB.C.DDDD

## Legenda:

- · AA = UF (ver tabela de UFs na seção Códigos de UF)

## 3. BB = LOCALIZAÇÃO DA FILIAL (VER QUADRO DE LOCALIZAÇÃO FÍSICA DA EMPRESA NA SEÇÃO  CADASTROS GERAIS

- · Empresas).
- · C = Subdivisão de região
- o 1 = Pólo (cidade onde está localizada a filial).
- o 2 = Região (região atendida pelas rotas/prazo mais curtos).
- o 3 = Interior (região atendida pelas rotas/prazos mais longos).
- · DDDD = Código da cidade fornecido pelo sistema.
- · 01 = RJ
- · 11 = Filial Nova Friburgo
- · 3 = Região Interior
- · 4243 = Santa Maria Madalena

## Exemplo: 01.11.3.4243

## 3.1.1. CÓDIGOS DE UF

• 01 = RJ

• 02 = SP

• 03 = ES

• 04 = MG

• 05 = PR

• 06 = SC

• 07 = RS

• 08 = GO

• 09 = PE

• 10 = MT

• 11 = MS

• 12 = TO

• 13 = DF

• 16 = SE

• 17 = CE

• 18 = RN

• 19 = PB

• 20 = PI

• 21 = MA

• 22 = PA

• 23 = AM

• 24 = RR

• 25 = RO

• 26 = AP

• 27 = AC

- · 14 = BA
- · 15 = AL

## 4. CADASTROS COMERCIAIS

## 4.1. CODIFICAÇÃO PARA TRECHOS DAS TABELAS DE PREÇO

Cada trecho cadastrado na estrutura de tabelas de preço deve ser codificado, obedecendo-se as seguintes regras.

Máscara: A.BB.CC.D

## NORMAS PARA PADRONIZAÇÃO DE CADASTRO NO ERP SENIOR

ROBERT OLIVEIRA - GERÊNCIA ADMINSITRATIVA   30/08/2017   Versão 1.0 --

<!-- image -->

- · Legenda:
- · A = Tipo de percurso
- o 1 = Da região atendida pela filial origem para a cidade polo da filial destino.
- 5. 2 = DA REGIÃO ATENDIDA PELA FILIAL ORIGEM PARA AS SUB-REGIÕES ATENDIDAS PELA FILIAL DESTINO (VER A LEGENDA DE SUBDIVISÃO DE REGIÕES NA SEÇÃO CADASTROS OPERACIONAIS
- o Codificação para cidades e regiões)
- o 3 = Da região atendida pela filial origem para um Estado inteiro.
- o 9 = Para regiões destino diferenciadas para clientes específicos.
- 6. BB = LOCALIZAÇÃO DA FILIAL ORIGEM (VER QUADRO DE LOCALIZAÇÃO FÍSICA DA EMPRESA NA SEÇÃO  CADASTROS GERAIS
- · Empresas).
- 7. CC = LOCALIZAÇÃO DA FILIAL DESTINO (VER QUADRO DE LOCALIZAÇÃO FÍSICA DA EMPRESA NA SEÇÃO  CADASTROS GERAIS
- · Empresas). Se o percurso for do tipo 3, este código representa a UF destino.
- 8. DD = SUB-REGIÕES ATENDIDAS PELA FILIAL DESTINO (VER A LEGENDA DE SUBDIVISÃO DE REGIÕES NA SEÇÃO CADASTROS OPERACIONAIS
- · Codificação para cidades e regiões). Não é aplicável ao tipo de percurso 1.

## Exemplos:

- · 1.14.10 = Trecho que compreende cargas com origem na filial CAS para a cidade do Rio de Janeiro (cidade polo da Frilog RJO).
- · 2.14.10.2 = Trecho que compreende cargas com origem na filial CAS para a região Interior da Frilog RJO.
- · 3.14.01.1 = Trecho que compreende cargas com origem na filial CAS para a região atendida pela filial que está na capital do Estado do Rio de Janeiro.
- · 3.14.01.2 = Trecho que compreende cargas com origem na filial CAS para a todo Estado do Rio de Janeiro, exceto a região atendida pela filial que está na capital.
- · 9.15.01.9 = Trecho que compreende cargas do cliente Tigre para a região diferenciada do padrão da Frilog, negociada com o cliente.

## 9. CADASTROS FINANCEIROS

- 9.1. CODIFICAÇÃO PARA NUMERAÇÃO DE TÍTULOS MANUAL

Todas as cidades atendidas pela Frilog devem ser codificadas em suas respectivas regiões de atendimento, conforme regras estabelecidas abaixo.

Máscara: AABBBC

## NORMAS PARA PADRONIZAÇÃO DE CADASTRO NO ERP SENIOR

ROBERT OLIVEIRA - GERÊNCIA ADMINSITRATIVA   30/08/2017   Versão 1.0 - -

<!-- image -->

## NORMAS PARA PADRONIZAÇÃO DE CADASTRO NO ERP SENIOR

ROBERT OLIVEIRA - GERÊNCIA ADMINSITRATIVA   30/08/2017   Versão 1.0 - -

## Legenda:

- · AA = Ano atual com dois dígitos.
- · BBB = Código da empresa.
- · C = Espécie de documento.
- · 17 = Ano atual (2017) com dois dígitos.
- · 110 = Filial da JC Thedim Transportes na cidade do Rio de Janeiro.
- · 6 = Documento do tipo ICMS.

Exemplo: 171106

## 10. CADASTROS DE RH

## 10.1.VÍNCULO DE COLABORADORES E EMPRESAS

Os colaboradores devem ser vinculados a dois tipos de empresa.

- · EMPRESA FOLHA: em qual empresa o colaborador está registrado.
- · EMPRESA SISTEMA: em que filial o colaborador efetivamente trabalha. Para este caso, deve-se utilizar somente as empresas do grupo 100 (J C THEDIM).

## 10.2.CADASTRO DE SINDICATOS

Todas os sindicatos vinculados a Frilog devem ser codificados, conforme regras estabelecidas abaixo.

Máscara: AAB

Legenda:

## 11. AA = LOCALIZAÇÃO FÍSICA DA FILIAL (LOCALIZAÇÃO DA FILIAL (VER QUADRO DE LOCALIZAÇÃO FÍSICA DA EMPRESA NA SEÇÃO CADASTROS GERAIS

- · Empresas).
- · B = Tipo de sindicato
- o 0 = Empregado de transportes
- o 1 = Empregado administrativo
- o 2 = Empregador
- · 16  = Filial SPA.
- · 1 = Sindicato do empregado administrativo.

## Exemplo: 161