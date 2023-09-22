-- Cria a tabela 'ingredientes' com IDs como PK e NOT NULL

CREATE TABLE
    IF NOT EXISTS ingredientes (
        id SERIAL PRIMARY KEY,
        -- Identificador único do ingrediente
        name VARCHAR(50) NOT NULL -- Nome do ingrediente (não pode ser nulo)
    );

-- Define o proprietário da tabela 'ingredientes' como 'postgres' (você pode alterar para o proprietário desejado)

ALTER TABLE ingredientes OWNER TO postgres;

-- Insere os ingredientes na tabela 'ingredientes'

INSERT INTO ingredientes (name)
VALUES ('atum'), ('cenoura'), ('ricota'), ('azeitona'), ('cebola'), ('alface'), ('tomate'), ('frango desfiado'), ('milho'), ('catupiry'), ('batata palha'), ('molho especial'), ('peito de peru'), ('queijo minas'), ('abacaxi'), ('presunto'), ('muçarela'), ('maionese'), ('passas'), (
        'hamburguer bovino artesanal'
    ), (
        'hamburguer de frango artesanal'
    ), ('bacon'), ('ovo'), ('pão de batata');

-- Cria a tabela 'produto'

CREATE TABLE
    IF NOT EXISTS produto (
        id SERIAL PRIMARY KEY,
        -- Identificador único do produto
        codigo INTEGER NOT NULL,
        -- Código do produto (não pode ser nulo)
        produto VARCHAR(255) NOT NULL,
        -- Nome do produto (não pode ser nulo)
        valor DOUBLE PRECISION NOT NULL -- Valor do produto (não pode ser nulo)
    );

-- Define o proprietário da tabela 'produto' como 'postgres' (você pode alterar para o proprietário desejado)

ALTER TABLE produto OWNER TO postgres;

-- Cria a tabela de junção 'produto_ingrediente'

CREATE TABLE
    IF NOT EXISTS produto_ingrediente (
        produto_id INTEGER NOT NULL,
        -- ID do produto
        ingrediente_id INTEGER NOT NULL,
        -- ID do ingrediente
        PRIMARY KEY (produto_id, ingrediente_id),
        FOREIGN KEY (produto_id) REFERENCES produto (id),
        FOREIGN KEY (ingrediente_id) REFERENCES ingredientes (id)
    );

-- Insere os produtos sem a lista de IDs de ingredientes

INSERT INTO
    produto (codigo, produto, valor)
VALUES (1, 'Sanduíche de Atum', 24.00), (
        2,
        'Sanduíche de Frango',
        24.00
    ), (
        3,
        'Sanduíche de Peito de Peru',
        24.00
    ), (
        4,
        'Sanduíche de Presunto',
        20.00
    ), (
        5,
        'Sanduíche de Salpicão',
        24.00
    ), (6, 'Maxburguer', 24.00), (7, 'Havaiano', 28.00), (8, 'Framburguer', 32.00), (9, 'Sukão', 32.00);

-- Atualiza os valores da nova coluna 'ingredientes_do_produto' usando a tabela de junção

INSERT INTO
    produto_ingrediente (produto_id, ingrediente_id)
VALUES (1, 24), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 24), (2, 8), (2, 9), (2, 10), (2, 11), (2, 12), (2, 6), (2, 7), (3, 24), (3, 13), (3, 14), (3, 15), (3, 12), (3, 6), (3, 7), (4, 24), (4, 16), (4, 17), (4, 12), (4, 6), (4, 7), (5, 24), (5, 8), (5, 18), (5, 9), (5, 4), (5, 2), (5, 19), (5, 11), (5, 6), (5, 7), (6, 24), (6, 20), (6, 17), (6, 12), (6, 6), (6, 7), (7, 24), (7, 20), (7, 17), (7, 16), (7, 15), (7, 12), (7, 6), (7, 7), (8, 24), (8, 21), (8, 17), (8, 22), (8, 12), (8, 6), (8, 7), (9, 24), (9, 20), (9, 17), (9, 16), (9, 11), (9, 23), (9, 22), (9, 12), (9, 6), (9, 7);