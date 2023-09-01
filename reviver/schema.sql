BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    key_path TEXT
);

CREATE TABLE IF NOT EXISTS bots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    max_tokens INT NOT NULL,
    temperature FLOAT NOT NULL,
    top_p FLOAT NOT NULL,
    frequency_penalty FLOAT NOT NULL,
    presence_penalty FLOAT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    bot_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY(bot_id) REFERENCES bots(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    time TIMESTAMP NOT NULL,
    role TEXT NOT NULL,
    conversation_id INTEGER,
    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
);

COMMIT;