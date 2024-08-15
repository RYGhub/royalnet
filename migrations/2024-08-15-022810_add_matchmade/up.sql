CREATE TYPE matchmaking_reply AS ENUM (
    'yes',
    'late',
    'maybe',
    'dontw',
    'cant',
    'wont'
);

CREATE TABLE matchmade (
    matchmaking_id INTEGER REFERENCES matchmaking(id),
    user_id INTEGER REFERENCES users(id),
    reply matchmaking_reply NOT NULL,
    late_mins INTEGER NOT NULL DEFAULT 0,

    PRIMARY KEY(matchmaking_id, user_id)
);
