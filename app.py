from datetime import datetime
import os
from cassandra.cluster import Cluster
import json
import time
from uuid import uuid4, UUID

# Função para conectar ao Cassandra com retries
def connect_to_cassandra():
    cluster = Cluster(['127.0.0.1'])  # Endereço do Cassandra
    retries = 20  # Número de tentativas de conexão
    for attempt in range(retries):
        try:
            session = cluster.connect()  # Conectar ao Cassandra
            print("Conexão bem-sucedida!")
            return session
        except Exception as e:
            print(f"Tentativa {attempt + 1}/{retries} falhou: {e}")
            time.sleep(5)  # Espera 5 segundos antes de tentar novamente
    raise Exception("Não foi possível conectar ao Cassandra após várias tentativas.")

# Função de criação das tabelas
def create_tables(session):
    try:
        print("Criando tabela 'usuarios'...")
        session.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id UUID PRIMARY KEY,
                nome TEXT,
                email TEXT,
                telefone TEXT,
                tipo_usuario TEXT,
                documento TEXT,
                dados_pessoa_fisica TEXT,
                dados_empresa TEXT,
                favoritos TEXT  -- Adicionando o campo favoritos
            )
        """)
        print("Tabela 'usuarios' criada ou já existente!")
    except Exception as e:
        print(f"Erro ao criar a tabela 'usuarios': {e}")

    try:
        print("Criando tabela 'produtos'...")    
        session.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                produto_id UUID PRIMARY KEY,
                nome TEXT,
                descricao TEXT,
                id_vendedor TEXT,
                status TEXT,
                precos TEXT
            )
        """)
        print("Tabela 'produtos' criada ou já existente!")
    except Exception as e:
        print(f"Erro ao criar a tabela 'produtos': {e}")
        return False

    try:
        print("Criando tabela 'compras'...")
        session.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                compra_id UUID PRIMARY KEY,
                id_usuario TEXT,
                data TEXT,
                preco_total DOUBLE,
                status TEXT,
                itens TEXT
            )
        """)
        print("Tabela 'compras' criada ou já existente!")
    except Exception as e:
        print(f"Erro ao criar a tabela 'compras': {e}")
        return False

    return True

# Função principal para inicializar e executar as ações
def main():
    # Conectar ao Cassandra
    print("Iniciando a execução do main...")
    session = connect_to_cassandra()
    print("Conexão com o Cassandra estabelecida!")

    # Garantir que o keyspace 'mercadolivre' existe
    try:
        session.execute("""DROP KEYSPACE IF EXISTS mercado_livre""")
        print("Keyspace 'mercadolivre' removido.")
        session.execute("""
            CREATE KEYSPACE mercado_livre WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
        print("Keyspace 'mercadolivre' criado com sucesso.")
        session.set_keyspace('mercado_livre')
        print("Agora estamos usando o keyspace 'mercado_livre'!")
    except Exception as e:
        print(f"Erro ao criar ou remover keyspace: {e}")

    # Criar as tabelas
    if not create_tables(session):
        print("Erro ao criar as tabelas. Encerrando o programa.")
        return  # Sai do programa caso as tabelas não sejam criadas corretamente

    # Função para manipular os dados de usuário
    class Usuario:
        def __init__(self, session):
            self.session = session

        def check_product_exists(self, product_id):
            """Verifica se o produto existe na tabela 'produtos'"""
            try:
                # Garantir que product_id seja convertido para UUID
                product_uuid = UUID(product_id)
                query = "SELECT produto_id FROM produtos WHERE produto_id = %s"
                result = self.session.execute(query, (product_uuid,))
                # Se a consulta retornar algum resultado, o produto existe
                return len(result.current_rows) > 0
            except Exception as e:
                print(f"Erro ao verificar se o produto {product_id} existe: {e}")
                return False

        def insert_user(self, usuario_data):
            user_id = uuid4()
            try:
                print("Iniciando a inserção do usuário...")

                # Verificar se os produtos nos favoritos existem
                favoritos_validos = []
                for favorito in usuario_data["favoritos"]:
                    product_exists = self.check_product_exists(favorito["id_produto"])
                    if product_exists:
                        favoritos_validos.append(favorito)  # Apenas adiciona o favorito se o produto existir
                    else:
                        print(f"O produto com ID {favorito['id_produto']} não existe e será ignorado.")

                # Atualizando a lista de favoritos com os produtos válidos
                usuario_data["favoritos"] = favoritos_validos

                # Inserindo os dados do usuário, incluindo os favoritos válidos
                self.session.execute("""
                    INSERT INTO usuarios (user_id, nome, email, telefone, tipo_usuario, documento, dados_pessoa_fisica, dados_empresa, favoritos) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, usuario_data["nome"], usuario_data["email"], usuario_data["telefone"], usuario_data["tipo_usuario"], usuario_data["documento"], 
                    json.dumps(usuario_data["dados_pessoa_fisica"]), json.dumps(usuario_data["dados_empresa"]), json.dumps(usuario_data["favoritos"])))

                print(f"Usuário {usuario_data['nome']} inserido com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir usuário {usuario_data['nome']}: {e}")
                raise  # Levanta novamente o erro para que seja possível tratá-lo em um nível superior, caso necessário

        def update_user(self, user_id, usuario_data):
            try:
                # Atualizando o usuário, incluindo os favoritos válidos
                self.session.execute("""
                    UPDATE usuarios 
                    SET nome = %s, email = %s, telefone = %s, tipo_usuario = %s, documento = %s, dados_pessoa_fisica = %s, dados_empresa = %s, favoritos = %s
                    WHERE user_id = %s
                """, (usuario_data["nome"], usuario_data["email"], usuario_data["telefone"], usuario_data["tipo_usuario"], 
                      usuario_data["documento"], json.dumps(usuario_data["dados_pessoa_fisica"]), 
                      json.dumps(usuario_data["dados_empresa"]), json.dumps(usuario_data["favoritos"]), user_id))
                print(f"Usuário {usuario_data['nome']} atualizado com sucesso.")
            except Exception as e:
                print(f"Erro ao atualizar usuário {usuario_data['nome']}: {e}")

    class Produto:
        def __init__(self, session):
            self.session = session

        def insert_product(self, produto_data):
            produto_id = uuid4()
            try:
                self.session.execute("""
                    INSERT INTO produtos (produto_id, nome, descricao, id_vendedor, status, precos) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (produto_id, produto_data["nome"], produto_data["descricao"], produto_data["id_vendedor"], produto_data["status"], json.dumps(produto_data["precos"])))
                print(f"Produto {produto_data['nome']} inserido com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir produto {produto_data['nome']}: {e}")

    class Compra:
        def __init__(self, session):
            self.session = session

        def delete_purchase(self, compra_id):
            try:
                self.session.execute("""
                    DELETE FROM compras WHERE compra_id = %s
                """, (compra_id,))
                print(f"Compra {compra_id} deletada com sucesso.")
            except Exception as e:
                print(f"Erro ao deletar compra {compra_id}: {e}")

        def insert_purchase(self, compra_data):
            compra_id = uuid4()
            try:
                self.session.execute("""
                    INSERT INTO compras (compra_id, id_usuario, data, preco_total, status, itens) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (compra_id, compra_data["id_usuario"], compra_data["data"], compra_data["preco_total"], compra_data["status"], json.dumps(compra_data["itens"])))
                print(f"Compra {compra_id} inserida com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir compra {compra_id}: {e}")

    # Inserção de dados de exemplo
    usuario_colection = Usuario(session)
    produto_colection = Produto(session)
    compras_colection = Compra(session)

    # Exemplo de Inserção de Produtos (com UUIDs gerados)
    produto_data_1 = {
        "nome": "Celular",
        "descricao": "iPhone 14 Pro Max",
        "id_vendedor": "u1",
        "status": "ativo",
        "precos": [
            {"preco": 1000, "data_inicio": "2024-01-01", "data_fim": "2024-05-01"},
            {"preco": 900, "data_inicio": "2024-05-02", "data_fim": None}
        ]
    }
    produto_data_3 = {
        "nome": "Fone de Ouvido",
        "descricao": "AirPods Pro",
        "id_vendedor": "u1",
        "status": "ativo",
        "precos": [
            {"preco": 200, "data_inicio": "2024-01-01", "data_fim": "2024-05-01"},
            {"preco": 180, "data_inicio": "2024-05-02", "data_fim": None}
        ]
    }

    produto_colection.insert_product(produto_data_1)
    produto_colection.insert_product(produto_data_3)

    # Inserção de Usuário
    produto_id_1 = uuid4()  # Gerar UUID para o produto p1
    produto_id_3 = uuid4()  # Gerar UUID para o produto p3

    usuario_data = {
        "nome": "João Silva",
        "email": "joao@email.com",
        "telefone": "1234567890",
        "tipo_usuario": "pessoa_fisica",
        "documento": "123.456.789-00",
        "dados_pessoa_fisica": {"cpf": "123.456.789-00", "data_nascimento": "1990-01-01", "endereco": "Rua X, 123"},
        "dados_empresa": None,
        "favoritos": [  # Lista de favoritos com UUIDs dos produtos
            {"id_produto": str(produto_id_1), "status": "ativo"},
            {"id_produto": str(produto_id_3), "status": "removido"}
        ]
    }
    usuario_colection.insert_user(usuario_data)

# Rodar o main
if __name__ == "__main__":
    main()
