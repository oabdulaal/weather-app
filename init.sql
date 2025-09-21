CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data for testing
INSERT INTO weather_data (city, temperature, humidity) VALUES 
('London', 15.5, 65),
('New York', 22.0, 70),
('Tokyo', 18.3, 80)
ON CONFLICT DO NOTHING;