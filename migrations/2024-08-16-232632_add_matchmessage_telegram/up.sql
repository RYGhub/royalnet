CREATE TABLE matchmessage_telegram (
    matchmaking_id INT NOT NULL,
    telegram_message_id BIGINT NOT NULL,

    PRIMARY KEY(matchmaking_id, telegram_message_id)
)