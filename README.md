# GitMiner CLI

**GitMiner** é uma ferramenta de linha de comando (CLI) para mineração de repositórios Git, projetada para extrair insights valiosos sobre a evolução do código, complexidade, manutenibilidade, hotspots e vulnerabilidades de segurança.

## Funcionalidades

-   **Análise de Commits**: Rastreia o histórico de commits para calcular métricas como churn (linhas adicionadas/removidas).
-   **Análise de Complexidade**: Mede a [complexidade ciclomática](https://en.wikipedia.org/wiki/Cyclomatic_complexity) de funções e métodos usando a ferramenta **Lizard**.
-   **Análise de Manutenibilidade (NOVO!)**: Calcula o **Índice de Manutenibilidade (MI)**, uma métrica avançada que combina a complexidade ciclomática, métricas de Halstead (volume do código) e linhas de código para gerar um score (0-100) que avalia a facilidade de manutenção de cada arquivo.
-   **Identificação de Hotspots**: Combina métricas de churn e complexidade para encontrar "hotspots" no código — arquivos que são complexos e mudam com frequência.
-   **Análise de Segurança**: Verifica potenciais vulnerabilidades de segurança em código Python usando **Bandit**.
-   **Relatórios e Visualização**: Gera relatórios resumidos no terminal, exporta dados para CSV/JSON e cria gráficos com `matplotlib`.

## Instalação

Para instalar o `gitminer-cli`, clone este repositório e instale-o em modo de desenvolvimento usando `pip`.

```bash
# 1. (Opcional, mas recomendado) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 2. Instale as dependências e a CLI a partir do diretório local
pip install -e .
```

Após a instalação, o comando `gitminer` estará disponível no seu terminal.

## Uso

A CLI possui quatro comandos principais.

### 1. `analyze`

Roda todas as análises (commits, complexidade, hotspots e manutenibilidade) e exibe um relatório resumido no terminal.

**Comando:**
```bash
gitminer analyze /caminho/para/seu/repo
```

**Exemplo de Saída (Atualizado):**
```
✅ Análise concluída.

📊 Resumo do Repositório
------------------------
Total de Arquivos com Churn: 152
Total de Arquivos com Complexidade Analisada: 98

🔥 Top 5 Hotspots (Complexidade vs. Churn)
--------------------------------------------
                             File  Complexity  Churn  Hotspot_Score
0     src/core/main.py            120       550         66000.0
1     src/utils/parser.py          85       300         25500.0
...

🧠 Top 5 Arquivos por Complexidade Ciclomática
-------------------------------------------------
                     File  Complexity
0  src/core/main.py            120
1  src/utils/parser.py          85
...

📈 Top 5 Arquivos por Churn (Linhas Alteradas)
------------------------------------------------
                         File  Churn
0    src/core/main.py        550
1    src/api/views.py        400
...

📉 Top 5 Arquivos com Menor Índice de Manutenibilidade (Pior para Manter)
----------------------------------------------------------------------
                                    file_path  maintainability_index  halstead_volume
0  src/legacy/old_module.py                   25.5                    8540.2
1          src/core/main.py                   32.8                    7600.5
2       src/utils/parser.py                   41.2                    5120.0
...
```

### 2. `security`

Roda a análise de segurança com o Bandit e exibe as vulnerabilidades encontradas.

**Comando:**
```bash
gitminer security /caminho/para/seu/repo
```

### 3. `export`

Exporta os dados brutos da análise para os formatos CSV ou JSON.

**Comandos:**
```bash
# Exportar para CSV
gitminer export /caminho/para/seu/repo --format csv --output-dir results/

# Exportar para JSON
gitminer export /caminho/para/seu/repo --format json --output-dir results/
```
Isso criará arquivos como `results/commits_analysis.csv`, `results/complexity_analysis.csv`, e o novo `results/maintainability_analysis.csv`.

### 4. `plot`

Gera e salva gráficos para as métricas especificadas (`complexity`, `churn`, `hotspots`, e a nova `maintainability`).

**Comandos:**
```bash
# Gráfico de hotspots (Complexidade vs. Churn)
gitminer plot /caminho/para/seu/repo --metric hotspots --output-dir plots/

# Gráfico de complexidade por arquivo
gitminer plot /caminho/para/seu/repo --metric complexity --output-dir plots/

# Gráfico de churn (linhas alteradas) por arquivo
gitminer plot /caminho/para/seu/repo --metric churn --output-dir plots/

# NOVO: Gráfico de manutenibilidade (mostra os piores arquivos)
gitminer plot /caminho/para/seu/repo --metric maintainability --output-dir plots/
```
Isso salvará imagens PNG, como `plots/maintainability_report.png`, no diretório especificado.

## Testes

Para rodar os testes automatizados, use `pytest`:

```bash
pytest
```