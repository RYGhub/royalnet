CREATE TABLE diario (
    id INT PRIMARY KEY,

    saver_id INT REFERENCES users (id),
    saved_on TIMESTAMP,

    quoted_id INT REFERENCES users (id),
    quoted_name VARCHAR,

    warning TEXT,
    quote TEXT NOT NULL,
    context TEXT NOT NULL
);