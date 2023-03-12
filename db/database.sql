-- Criação da tabela de usuários
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL
);

-- Criação do usuário admin
INSERT INTO users (username, password) VALUES ('admin', 'admin');

-- Criação da tabela de plataformas
CREATE TABLE plataformas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL
);

-- Criação da tabela de categorias
CREATE TABLE categorias (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(50) NOT NULL
);

-- Criação da tabela de jogos
CREATE TABLE games (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  platform_id INT NOT NULL,
  category_id INT NOT NULL,
  description TEXT,
  image VARCHAR(255),
  FOREIGN KEY (platform_id) REFERENCES plataformas(id),
  FOREIGN KEY (category_id) REFERENCES categorias(id)
);