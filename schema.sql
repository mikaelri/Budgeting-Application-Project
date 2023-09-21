DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    password TEXT,
    role INTEGER
);

CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(id),
    name TEXT,
    income INTEGER,
    expense INTEGER,
    message TEXT
);

CREATE TABLE IF NOT EXISTS income (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER REFERENCES budgets,
    income INTEGER,
    category TEXT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS expense (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER REFERENCES budgets,
    expense INTEGER,
    category TEXT,
    message TEXT
);