DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS budgets CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS results CASCADE;
DROP TABLE IF EXISTS comments CASCADE;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT, 
    password TEXT,
    role INTEGER
);

CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users(id),
    name TEXT
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    budget_id INTEGER REFERENCES budgets(id),
    income INTEGER,
    expense INTEGER,
    income_category TEXT,
    expense_category TEXT,
    message TEXT
);

CREATE TABLE IF NOT EXISTS results (
    budget_id INTEGER PRIMARY KEY REFERENCES budgets(id),
    total_income BIGINT,
    total_expense BIGINT,
    net_result BIGINT
);

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    comment_id INTEGER REFERENCES budgets(id),
    comment TEXT
);