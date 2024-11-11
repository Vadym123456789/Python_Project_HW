PRAGMA foreign_keys=ON;
PRAGMA encoding='UTF-8';

CREATE TABLE IF NOT EXISTS User (
    login TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    ipn TEXT UNIQUE,
    full_name TEXT,
    contacts TEXT,
    photo BLOB
);

CREATE TABLE IF NOT EXISTS Item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo BLOB,
    name TEXT NOT NULL,
    description TEXT,
    price_hour REAL,
    price_day REAL,
    price_week REAL,
    price_month REAL
);

CREATE TABLE IF NOT EXISTS Contract (
    contract_num INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    start_date DATE,
    end_date DATE,
    leaser TEXT,
    taker TEXT,
    item_id INTEGER,
    FOREIGN KEY (leaser) REFERENCES User(login),
    FOREIGN KEY (taker) REFERENCES User(login),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);

CREATE TABLE IF NOT EXISTS Feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    user TEXT,
    text TEXT,
    grade INTEGER CHECK (grade BETWEEN 1 AND 5),
    contract_num INTEGER,
    FOREIGN KEY (author) REFERENCES User(login),
    FOREIGN KEY (user) REFERENCES User(login),
    FOREIGN KEY (contract_num) REFERENCES Contract(contract_num)
);

CREATE TABLE IF NOT EXISTS SearchHistory (
    search_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    search_text TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user) REFERENCES User(login)
);

CREATE TABLE IF NOT EXISTS Favorites (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    item_id INTEGER,
    FOREIGN KEY (user) REFERENCES User(login),
    FOREIGN KEY (item_id) REFERENCES Item(item_id)
);