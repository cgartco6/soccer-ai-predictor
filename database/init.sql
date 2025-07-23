CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(50) UNIQUE NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    league VARCHAR(50) NOT NULL,
    match_time TIMESTAMPTZ NOT NULL
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id),
    prediction_time TIMESTAMPTZ DEFAULT NOW(),
    outcome VARCHAR(20) NOT NULL,
    confidence FLOAT NOT NULL,
    btts_prob FLOAT NOT NULL,
    value_edge FLOAT NOT NULL,
    sent_to_telegram BOOLEAN DEFAULT FALSE
);

CREATE TABLE bookmaker_odds (
    id SERIAL PRIMARY KEY,
    match_id INTEGER REFERENCES matches(id),
    scraped_time TIMESTAMPTZ DEFAULT NOW(),
    bookmaker VARCHAR(50) NOT NULL,
    home_win FLOAT,
    draw FLOAT,
    away_win FLOAT,
    btts_yes FLOAT,
    btts_no FLOAT
);

CREATE INDEX idx_match_time ON matches(match_time);
CREATE INDEX idx_prediction_time ON predictions(prediction_time);
