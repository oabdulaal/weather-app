from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://pguser:password@db:5432/weather_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

def validate_temperature(temp):
    """Validate temperature is within reasonable range"""
    if temp < 30 or temp > 40:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/weather', methods=['POST'])
def add_weather():
    try:
        data = request.json
        
        if not data or 'city' not in data or 'temperature' not in data:
            return jsonify({"error": "Missing required fields: city, temperature"}), 400
            
        temp = float(data['temperature'])
        
        if not validate_temperature(temp):
            return jsonify({"error": "Temperature out of valid range"}), 400
        
        weather = WeatherData(
            city=data['city'],
            temperature=temp,
            humidity=data.get('humidity', 0)
        )
        
        db.session.add(weather)
        db.session.commit()
        
        return jsonify({
            "id": weather.id, 
            "status": "created",
            "data": weather.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        weather_data = WeatherData.query.filter_by(city=city).limit(10).all()
        return jsonify([w.city.to_dict() for w in weather_data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5004, debug=False)