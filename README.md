# Weather API Assignment - Instructions for Candidates

## Introduction
Welcome to the Weather Data App assignment! The Weather App is a basic application simulating the backend for a weather forecasting website, with simple functionalities of adding and querying weather updates. This is a practical coding challenge designed to evaluate your skills in API development, debugging, database integration, and ability to work with containarized environments.

## What You'll Be Working With

- **Backend:** Python Flask API with PostgreSQL database
- **Deployment:** Docker and Docker Compose
- **Data Processing:** Weather data ingestion and analytics
- **Integration:** REST API endpoints with database operations


## What you'll need
1. An IDE/Codespace with Python and Bash environment setup
2. A working docker environment with docker compose


## Instructions & Rules
- Go through this entire README before attempting the challenge
- Clone the provided repository first, and make sure you're familiar with the Database structure, Dockerfile, Docker-Compose and Tests to help you
- The challenge builds on each step, So solve the first step before moving on to the next
- You'll be asked to walk through your approach and decisions, and challenged on some of them, so avoid using AI tools like Claude Code or Cursor


## Assignment Phases

### Phase 1: Environment Setup & Debugging 

Here, you are asked to download this boilerplate code, read and understand the setup and APIs, and reach a working state for the application. 

#### Step 1: Initial Setup 
1. Clone the provided repository
2. Try to run `docker-compose up --build` 
3. Document what errors you encounter
4. Identify the scope of issues

#### Step 2: Identify and Fix the issues
There are multiple bugs within the code and deployment. Your task is to identify the configuration and logic issues and resolve them to fix the flawed code

```bash
# This should work without errors:
docker-compose up --build

# Health check should return 200:
curl http://localhost:5004/health

# Basic weather data insertion:
curl -X POST http://localhost:5004/weather \
  -H "Content-Type: application/json" \
  -d '{
    "city": "London",
    "temperature": 20.5,
    "humidity": 65,
    "timestamp": "2024-01-15 14:30:00"
  }'

# Data retrieval should work:
curl http://localhost:5004/weather/London
```

## Phase 2: Feature Implementation
This is where it gets progressively trickier. As a recently onboarded Software Engineer on the team, Your task is to start contributing by adding new features to our application. Our Product and Engineering teams have worked hard to identify the most impactful features needed by our customers: 

#### Step 1: Fix the Broken GET Endpoint
The `/weather/{city}` endpoint has several issues:
- **Error**: The current implementation seems to not work and return an error for our users
- **Case sensitivity problem**: Searching for "london" doesn't find data stored as "London"
- **No error handling**: Returns empty array instead of meaningful errors for non-existent cities

**Fix these issues to make the endpoint production-ready.**

#### Step 2: Add Analytics Endpoints
Implement three new endpoints:

**1. City Statistics**: `GET /weather/{city}/stats`
```json
{
  "city": "London",
  "statistics": {
    "total_records": 150,
    "temperature": {
      "min": 5.2,
      "max": 28.1,
      "average": 16.8
    },
    "humidity": {
      "average": 72.3
    }
  }
}
```

**2. Recent Weather**: `GET /weather/{city}/recent`
- Return weather data for the last 7 days
- Group by date with daily summaries (min/max/avg temperatures)

**3. Cities Summary**: `GET /cities/summary`
- Overview statistics for all cities in the system
- Include total records per city and temperature ranges

### Bonus Feature: Weather Alerts System

This is a bonus feature. You won't be penalized if you submit without it. Food for thought if you are in the mood.

Endpoints:

- `POST /alerts/configure` - Set up alert thresholds
- `GET /alerts` - Get active alerts
- `GET /alerts/history` - Alert history

Alert Configuration:
```json
{
  "city": "London",
  "temperature_min": 5.0,
  "temperature_max": 30.0,
  "humidity_max": 90.0,
  "enabled": true
}
```

Alert Response:
```json
{
  "alert_id": "alert_123",
  "city": "London",
  "alert_type": "temperature_high",
  "current_value": 32.5,
  "threshold": 30.0,
  "timestamp": "2024-01-15T16:30:00Z",
  "status": "active"
}
```


## Implementation Guidelines

### Code Structure
Ideally, This is how code is structured.
```
app/
├── __init__.py
├── main.py              # Main Flask app
├── models.py            # Database models
├── routes/              # API route handlers
│   ├── __init__.py
│   ├── weather.py       # Weather CRUD operations
│   ├── analytics.py     # Analytics endpoints
│   └── alerts.py        # Alert system
├── services/            # Business logic
│   ├── weather_processor.py
│   ├── analytics_service.py
│   └── alert_service.py
├── utils/
│   └── validators.py
└── config.py
```

These are some of the industry best practices and guidelines. You are welcome to use them. However for simplicity they're not part of the assessment :smiley:

### Database Design Best Practices
- Use appropriate indexes for query performance
- Implement proper foreign key relationships
- Add constraints for data integrity
- Consider partitioning for time-series data

### API Design Standards
- Use proper HTTP status codes
- Implement consistent error response format
- Add request/response validation
- Include pagination for list endpoints
- Document all endpoints clearly

### Error Handling
```python
# Standard error response format
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Temperature must be between -50 and 60 degrees Celsius",
        "details": {
            "field": "temperature",
            "provided_value": 150.5
        }
    }
}
```



## Testing Your Implementation

### Manual Testing Checklist
- [ ] Docker environment starts successfully
- [ ] Health check endpoint responds
- [ ] Weather data CRUD operations work
- [ ] Analytics endpoint returns accurate calculations
- [ ] Alert system correctly identifies thresholds
- [ ] All endpoints handle errors gracefully
- [ ] Database persists data between restarts

### Sample Test Data
```bash
# Add weather data for testing analytics
curl -X POST http://localhost:5000/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "London", "temperature": 15.5, "humidity": 70}'

curl -X POST http://localhost:5000/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "London", "temperature": 18.2, "humidity": 65}'

curl -X POST http://localhost:5000/weather \
  -H "Content-Type: application/json" \
  -d '{"city": "New York", "temperature": 22.1, "humidity": 80}'

# Test analytics
curl "http://localhost:5000/analytics/London?period=7d"
```

## Success Milestone

### Test the fixed and new endpoints
```bash
curl "http://localhost:5000/weather/london"  # Case insensitive
curl "http://localhost:5000/weather/London/stats"
curl "http://localhost:5000/weather/London/recent"
curl "http://localhost:5000/cities/summary"
```

## Submission Requirements

### 1. Updated Codebase
- All Part 1 bugs fixed and working
- Part 2 features fully functional (fixed GET endpoint + 3 analytics endpoints)
- Clean, well-structured code with proper error handling

### 2. Updated README.md
Update the README with:
- Summary of Part 1 issues found and fixed
- Description of Part 2 features implemented
- API endpoint documentation for new analytics endpoints
- Instructions for testing all implemented features

### 3. SOLUTION.md File
Document your complete approach:
- **Part 1**: Debugging process and fixes implemented
- **Part 2**: Architecture decisions for the new endpoints
- **Testing**: How you verified your implementations work

### 4. Working Docker Environment
Ensure the final submission runs with:
```bash
docker-compose down
docker-compose up --build
```

## What We're Evaluating

### Technical Competencies
1. **Debugging Skills**: Ability to identify and resolve various types of issues
2. **API Development**: RESTful design, error handling, and documentation
3. **Database Integration**: Schema design, queries, and data modeling
4. **Data Processing**: Validation, transformation, and aggregation
5. **Docker & DevOps**: Containerization and deployment configuration
6. **Code Quality**: Structure, readability, and maintainability

## Tips for Success

### Debugging Strategy
1. **Start with the foundation**: Fix Docker and database issues first
2. **Work systematically**: Don't try to fix everything at once
3. **Test incrementally**: Verify each fix before moving to the next
4. **Read error messages carefully**: They often contain the exact problem

### Time Management
1. **Part 1 first**: Don't start Part 2 until existing code works and tests pass
2. **Fix then build**: Get the broken GET endpoint working before adding new analytics
4. **Leave time for documentation**: Your written explanations are as important as the code

### Common Pitfalls to Avoid
- Don't skip Part 1 debugging to jump to new features
- Don't ignore database performance when implementing analytics
- Don't over-engineer simple solutions - working code is better than complex broken code  
- Don't forget error handling and edge cases

## Questions?
If you encounter issues that seem outside the scope of the intended challenge (e.g., fundamental environment problems), please reach out. We want to evaluate your engineering skills, not frustrate you with setup issues.

Good luck! We're excited to see your approach to solving this challenge.
