import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from app.main import app, validate_temperature

@pytest.fixture
def client():
    """Create a test client with mocked database"""
    app.config['TESTING'] = True
    return app.test_client()

@pytest.fixture
def mock_db():
    """Mock the database operations"""
    with patch('app.main.db') as mock_db:
        mock_db.session = Mock()
        mock_db.session.add = Mock()
        mock_db.session.commit = Mock()
        yield mock_db

def test_health_check(client):
    """Test that health check endpoint works"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_temperature_validation_logic():
    """Test temperature validation function - WILL FAIL due to BUG 2"""
    # These should be valid but validation incorrectly rejects them
    assert validate_temperature(5.0) == True   # 5°C should be valid (winter)
    assert validate_temperature(0.0) == True   # 0°C should be valid (freezing)
    assert validate_temperature(-10.0) == True # -10°C should be valid (cold winter)
    
    # These should still be valid
    assert validate_temperature(25.0) == True  # 25°C room temperature
    assert validate_temperature(45.0) == True  # 45°C hot summer day
    
    # These should be invalid (extreme temperatures)
    assert validate_temperature(-60.0) == False  # Too cold
    assert validate_temperature(70.0) == False   # Too hot

@patch('app.main.WeatherData')
def test_add_weather_success(mock_weather_data, client, mock_db):
    """Test adding valid weather data with normal temperature"""
    # Mock the WeatherData instance
    mock_instance = Mock()
    mock_instance.id = 1
    mock_instance.to_dict.return_value = {
        'id': 1,
        'city': 'London',
        'temperature': 20.5,
        'humidity': 65,
        'timestamp': '2024-01-01T12:00:00'
    }
    mock_weather_data.return_value = mock_instance
    
    weather_data = {
        "city": "London",
        "temperature": 20.5,
        "humidity": 65
    }
    
    response = client.post('/weather', 
                          data=json.dumps(weather_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['status'] == 'created'
    assert response.json['data']['city'] == 'London'
    assert response.json['data']['temperature'] == 20.5
    
    # Verify database operations were called
    mock_db.session.add.assert_called_once()
    mock_db.session.commit.assert_called_once()

@patch('app.main.WeatherData')
def test_add_weather_winter_temperature(mock_weather_data, client, mock_db):
    # Mock the WeatherData instance
    mock_instance = Mock()
    mock_instance.id = 2
    mock_instance.to_dict.return_value = {
        'id': 2,
        'city': 'Oslo',
        'temperature': 2.0,
        'humidity': 80,
        'timestamp': '2024-01-01T12:00:00'
    }
    mock_weather_data.return_value = mock_instance
    
    weather_data = {
        "city": "Oslo",
        "temperature": 2.0,  # Valid winter temperature, but validation rejects it
        "humidity": 80
    }
    
    response = client.post('/weather', 
                          data=json.dumps(weather_data),
                          content_type='application/json')
    
    # This should succeed but will fail due to validation bug
    assert response.status_code == 201
    assert response.json['status'] == 'created'
    assert response.json['data']['temperature'] == 2.0

def test_add_weather_missing_fields(client):
    """Test error handling for missing required fields"""
    weather_data = {
        "city": "Paris"
        # Missing temperature field
    }
    
    response = client.post('/weather', 
                          data=json.dumps(weather_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    assert 'Missing required fields' in response.json['error']

@patch('app.main.WeatherData')
def test_get_weather_by_city(mock_weather_data, client):
    """Test retrieving weather data for a city"""
    # Mock the query result
    mock_weather_item = Mock()
    mock_weather_item.to_dict.return_value = {
        'id': 1,
        'city': 'Tokyo',
        'temperature': 28.0,
        'humidity': 70,
        'timestamp': '2024-01-01T12:00:00'
    }
    
    mock_query = Mock()
    mock_query.filter_by.return_value.limit.return_value.all.return_value = [mock_weather_item]
    mock_weather_data.query = mock_query
    
    response = client.get('/weather/Tokyo')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['city'] == 'Tokyo'
    assert response.json[0]['temperature'] == 28.0

def test_add_weather_extreme_invalid_temperature(client):
    """Test that truly invalid temperatures are rejected"""
    weather_data = {
        "city": "InvalidCity",
        "temperature": 100.0,  # This should be rejected (too hot)
        "humidity": 50
    }
    
    response = client.post('/weather', 
                          data=json.dumps(weather_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    assert 'Temperature out of valid range' in response.json['error']


