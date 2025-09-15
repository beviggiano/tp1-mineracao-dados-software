# TP: Mineração de Repositórios de Software

## 1. Membros do Grupo
- Bernardo Viggiano 
- Eduardo Correia 
- Juan Coelho  
- Rafael Chimicatti  

## 2. Explicação do Sistema
O sistema consiste em uma ferramenta de linha de comando (CLI) que realiza a mineração de repositórios Git para identificar problemas de manutenção de software.  
Ele analisa dados históricos de commits, diffs e metadados do repositório, extraindo métricas como complexidade do código, hotspots de alterações e churn.  
O objetivo é fornecer relatórios e visualizações que auxiliem no processo de compreensão, manutenção e evolução do software, permitindo a detecção de padrões de degradação, possíveis pontos de falha e oportunidades de refatoração.

As saídas incluem:
- Relatórios em terminal (tabelas e estatísticas).  
- Exportação de resultados em CSV ou JSON.  
- Gráficos ilustrando a evolução das métricas ao longo do tempo.  

## 3. Tecnologias Utilizadas
- **PyDriller**: framework em Python para análise de commits e diffs em repositórios Git.  
- **GitPython**: biblioteca para manipulação e inspeção de repositórios Git locais.  
- **Typer**: criação de interface de linha de comando amigável e de fácil manutenção.  
- **Lizard**: cálculo da complexidade ciclomática e métricas de qualidade de código.  
- **Bandit**: identificação de vulnerabilidades comuns em código Python.  
- **Matplotlib** + **Pandas**: manipulação de dados e geração de gráficos.  
- **Pytest**: criação de testes automatizados para garantir a qualidade do sistema.  
