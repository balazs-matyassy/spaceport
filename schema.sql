DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS product;

CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  unit_price INTEGER NOT NULL,
  discount INTEGER NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

INSERT INTO user (username, password, role)
    VALUES (
            'admin',
            'pbkdf2:sha256:260000$oq5tjm5l8QlugwnP$802307ecfc0b454a4fd5ba63930a03255170056fb5e3610690a56cd9bdb8b7c5',
            'ADMIN'
    );