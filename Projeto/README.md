### **Agente Conversacional ARCOS**

Agente conversacional que possui acesso aos dados abertos do RJ e informações relevantes sobre os documentos lá armazenados.

Conta com funcionalidades 
- **listar_bases**: Através do endpoint que contém as bases de dados a serem consultadas, é capaz de listar o nome de todas elas.
- **buscar_infos_base**: O usuário passa o nome da base de dados que quer ter mais informações e obtem o retorno. Se o nome repassado pelo usuário não for suficiente para encontrar a base, usará a tool *listar_bases* para encontrar uma correspondência.
- 
