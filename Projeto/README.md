### **Agente Conversacional ARCOS**

Agente conversacional que possui acesso aos dados abertos do RJ e informações relevantes sobre os documentos lá armazenados.

Conta com funcionalidades 
- **listar_bases**: Através do endpoint que contém as bases de dados a serem consultadas, é capaz de listar o nome de todas elas.
- **buscar_infos_base**: O usuário passa o nome da base de dados que quer ter mais informações e obtem o retorno. Se o nome repassado pelo usuário não for suficiente para encontrar a base, usará a tool *listar_bases* para encontrar uma correspondência.
- 

### **Base 1 (Testes: Gratuidade)**

**1. Dados de Gratuidade (setram_sgr)**

*   **Organização:** SETRAM
*   **Descrição:** Contém dados de gratuidade.
*   **Recursos:** Possui 202 arquivos, a maioria são arquivos ZIP com dados de "Transações Gratuidade" em formato CSV, abrangendo diversas datas em 2025. Também inclui dicionários públicos detalhados e consolidados em formato XLSX.
*   **Periodicidade:** Diária
*   **Dicionário de Dados:** Sim
*   **Última atualização dos metadados:** 7 de dezembro de 2025

**2. Concessionária Barcas S.A. (concessionaria-ccr-barcas)**

*   **Organização:** AGETRANSP
*   **Descrição:** Dados sobre a concessionária Barcas S.A., incluindo a série histórica de passageiros, tarifas, receitas, custos e despesas da concessão.
*   **Recursos:** Dentro desta base, há recursos específicos sobre gratuidades, como a "Série histórica da quantidade de gratuidades" disponível em formato XLSX e PDF.
*   **Cobertura Temporal (Gratuidades):** De 01/01/2017 a 11/02/2025
*   **Periodicidade:** Sob demanda
