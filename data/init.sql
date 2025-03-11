CREATE TABLE IF NOT EXISTS coordenadas (
    id SERIAL PRIMARY KEY,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL
);
COPY coordenadas(x, y) FROM '/docker-entrypoint-initdb.d/puntos.csv' DELIMITER ',' CSV HEADER;
