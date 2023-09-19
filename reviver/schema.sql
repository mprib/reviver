BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS user (
    name TEXT PRIMARY KEY NOT NULL,
    dot_env_loc TEXT
);

CREATE TABLE IF NOT EXISTS bots (
    _id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    rank INTEGER NOT NULL,
    hidden BOOLEAN NOT NULL,
    model TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    max_tokens INT NOT NULL,
    temperature FLOAT NOT NULL,
    top_p FLOAT NOT NULL,
    frequency_penalty FLOAT NOT NULL,
    presence_penalty FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS conversations (
    _id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    bot_id INTEGER,
    FOREIGN KEY(bot_id) REFERENCES bots(id)
);

CREATE TABLE IF NOT EXISTS messages (
    conversation_id INTEGER,
    position INTEGER,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    PRIMARY KEY (conversation_id, position),
    FOREIGN KEY(conversation_id) REFERENCES conversations(_id)
    
);

COMMIT;