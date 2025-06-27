## Atividade #4 Professor Diogo Branquinho

### Objetivo

Crie uma conta gratuita no Cassandra https://auth.cloud.datastax.com/

1. Implemente em Python as funções de manipulação da Base de Dados Não Relacional do Mercado Livre (EX1) no Cassandra

a. Insert em todas as coleções (Usuário, Vendedor, Produto, Compra) 
b. Update em Usuário 
c. Search em Produto 
d. Delete em Compra 
 
 


Para que o projeto rode, devemos criar um container cassandra baseado no arquivo docker-compose.yml.

```powershell
docker-compose up --build
```
Veja se o container está rodando no docker desktop.

<img src="../atv4/cassandra/img/docker.png" alt="docker-desktop" width="700"/>

```powesrhell
py -3 -m venv venv
```

```powershell
# dentro do diretorio chamado cassandra
\venv\Scripts\activate
```

```powershell
# instalar dependências
pip install -r .\requirements.txt
```

```powershell
# rodar projeto
python .\app.py
```

```powershell
Iniciando a execução do main...
Conexão bem-sucedida!
Conexão com o Cassandra estabelecida!
Keyspace 'mercadolivre' removido.
Keyspace 'mercadolivre' criado com sucesso.
Agora estamos usando o keyspace 'mercado_livre'!
Criando tabela 'usuarios'...
Tabela 'usuarios' criada ou já existente!
Criando tabela 'produtos'...
Tabela 'produtos' criada ou já existente!
Criando tabela 'compras'...
Tabela 'compras' criada ou já existente!
Produto Celular inserido com sucesso.
Produto Fone de Ouvido inserido com sucesso.
Iniciando a inserção do usuário...
O produto com ID e7baf533-9448-49d5-88c5-902f5686d52a não existe e será ignorado.
O produto com ID e25d469c-f14c-4701-886e-047528f812c5 não existe e será ignorado.
Usuário João Silva inserido com sucesso.
```