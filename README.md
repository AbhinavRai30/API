# GreenCycles Dynamic CRUD API

A FastAPI-based RESTful API providing dynamic CRUD operations for PostgreSQL database tables. This API allows you to perform Create, Read, Update, and Delete operations on any table in the `greencycles` database without hardcoding table-specific logic.

## Features

- **Dynamic CRUD Operations**: Perform CRUD on any database table
- **Automatic Primary Key Detection**: Automatically identifies table primary keys
- **Safe Column Handling**: Filters out identity columns and columns with defaults for INSERT operations
- **Binary Data Support**: Handles binary/blob data with Base64 encoding
- **Table Discovery**: List all available tables in the database
- **PostgreSQL Integration**: Built with SQLAlchemy and psycopg2

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server

## Project Structure

```
API/
├── main.py           # FastAPI application and endpoints
├── db.py             # Database connection and session management
├── crud.py           # CRUD operation functions
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas for request/response validation
├── security.py       # Security configurations (if applicable)
├── ddl.py            # Database DDL utilities
├── requirements.txt  # Python dependencies
└── .venv/            # Virtual environment
```

## Prerequisites

- Python 3.10+
- PostgreSQL database
- `greencycles` database created

## Installation

1. **Clone the repository**
```bash
https://github.com/AbhinavRai30/API.git
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
```

4. **Configure database connection**

Edit `db.py` and update the database URL:
```python
DATABASE_URL = "postgresql://username:password@localhost:5432/greencycles"
```

## Running the API

**Start the server:**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Access the API:**
- API Base URL: `http://127.0.0.1:8000`
- Interactive API Docs: `http://127.0.0.1:8000/docs`
- Alternative Docs: `http://127.0.0.1:8000/redoc`

## API Endpoints

### 1. List All Tables
**GET** `/tables`

Returns a list of all tables in the database.

**Example Response:**
```json
["actor", "film", "customer", "rental"]
```

### 2. Get All Rows from a Table
**GET** `/table/{table}`

Retrieve all rows from the specified table (limited to 100 rows).

**Example Request:**
```
GET /table/film
```

**Example Response:**
```json
[
  {
    "film_id": 1,
    "title": "ACADEMY DINOSAUR",
    "rental_rate": 0.99,
    "language_id": 1
  }
]
```

### 3. Get Single Row by ID
**GET** `/table/{table}/{id}`

Retrieve a specific row by its primary key.

**Example Request:**
```
GET /table/film/1
```

### 4. Insert New Row
**POST** `/table/{table}`

Create a new record in the specified table.

**Example Request:**
```json
POST /table/film
Content-Type: application/json

{
  "title": "New Film",
  "rental_duration": 3,
  "rental_rate": 4.99,
  "replacement_cost": 19.99,
  "language_id": 1
}
```

**Example Response:**
```json
{
  "film_id": 1001,
  "title": "New Film",
  "rental_duration": 3,
  "rental_rate": 4.99,
  "replacement_cost": 19.99,
  "language_id": 1
}
```

### 5. Update Existing Row
**PUT** `/table/{table}/{id}`

Update an existing record by its primary key.

**Example Request:**
```json
PUT /table/film/1001
Content-Type: application/json

{
  "title": "Updated Film Title",
  "rental_rate": 5.99
}
```

### 6. Delete Row
**DELETE** `/table/{table}/{id}`

Delete a record by its primary key.

**Example Request:**
```
DELETE /table/film/1001
```

**Example Response:**
```json
{
  "status": "deleted"
}
```

## Database Configuration

The API connects to PostgreSQL database `greencycles` with the following default configuration:

- **Host:** localhost
- **Port:** 5432
- **Database:** greencycles
- **User:** postgres
- **Password:** pgadmin

Update these values in `db.py` as needed.

## Error Handling

The API includes error handling for:
- Invalid table names
- Missing primary keys
- Record not found (404)
- Invalid data format (400)
- Database connection errors

## Security Considerations

- Table name validation to prevent SQL injection
- Uses parameterized queries
- Transaction management with automatic rollback on errors

## Testing

This API is designed to work with the Robot Framework automation test suite located in the `api-framework` folder.

To run tests:
```bash
cd c:\driver\PythonProject\PythonProject\api-framework
robot tests/api_json_tests.robot
```

## Development

**Enable development mode:**
```bash
uvicorn main:app --reload
```

The `--reload` flag automatically restarts the server when code changes are detected.

## Contributing

1. Make changes in a feature branch
2. Test thoroughly using the Robot Framework test suite
3. Ensure all tests pass before merging

## License



## Support

For issues or questions, please contact the development team.

---

**Note:** This API provides direct access to database tables. Ensure proper authentication and authorization are implemented before deploying to production.
