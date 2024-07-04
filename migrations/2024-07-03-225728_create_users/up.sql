CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL
);

CREATE TABLE telegram (
    user_id INT NOT NULL REFERENCES users (id),
    telegram_id BIGINT PRIMARY KEY
);

CREATE TABLE discord (
    user_id INT NOT NULL REFERENCES users (id),
    discord_id BIGINT PRIMARY KEY
);

CREATE TABLE steam (
    user_id INT NOT NULL REFERENCES users (id),
    steam_id BIGINT PRIMARY KEY
);

