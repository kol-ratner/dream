CREATE TABLE transactions
(
    id             SERIAL PRIMARY KEY,
    transaction_id UUID           NOT NULL,
    store_code     VARCHAR(255)   NOT NULL,
    amount         DECIMAL(10, 2) NOT NULL,
    status         VARCHAR(50)    NOT NULL,
    processed_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
