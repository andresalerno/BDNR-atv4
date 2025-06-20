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
Criando tabela 'favoritos'...
Tabela 'favoritos' criada ou já existente!
Iniciando a inserção do usuário...
Dados do usuário: {'nome': 'João Silva', 'email': 'joao@email.com', 'telefone': '1234567890', 'tipo_usuario': 'pessoa_fisica', 'documento': '123.456.789-00', 'dados_pessoa_fisica': {'cpf': '123.456.789-00', 'data_nascimento': '1990-01-01', 'endereco': 'Rua X, 123'}, 'dados_empresa': None}     
Usuário João Silva inserido com sucesso.
Produto Celular inserido com sucesso.
Compra 1d592892-5c47-4a84-8d95-18279e2acd99 inserida com sucesso.
Favoritos de João Silva inseridos com sucesso.
```