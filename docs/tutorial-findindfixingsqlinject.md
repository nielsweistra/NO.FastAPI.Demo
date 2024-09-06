
# **Tutorial: Finding and Fixing SQL Injection Vulnerabilities in a FastAPI App**

In this tutorial, we'll cover how to test a FastAPI application for SQL injection vulnerabilities and how to secure it. We’ll use two testing methods and then implement strategies to fix any issues we find.

## **Overview**

1. **Set Up a Vulnerable FastAPI App**
2. **Fuzz Testing**
   - Custom Fuzz Testing
   - Hypothesis-Based Testing
3. **Mitigation Strategies**

## **Step 1: Set Up the Vulnerable FastAPI App**

**Create a file named `main.py` with the following code:**

```python
from fastapi import FastAPI, Query
from typing import List, Dict
import sqlite3
from fastapi.responses import JSONResponse

app = FastAPI()

def query_database(query: str) -> List[Dict]:
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{'name': row[0]} for row in results]  # Adjust based on your schema

@app.get('/search', response_model=List[Dict[str, str]])
async def search(q: str = Query('', description="Query parameter for search")):
    # This is the vulnerable part
    query = f"SELECT * FROM innocent WHERE name = '{q}'"
    results = query_database(query)
    return JSONResponse(content=results)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Create the SQLite database (`example.db`) with these tables:**

```sql
-- Create the innocent table
CREATE TABLE innocent (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- Add sample data
INSERT INTO innocent (name) VALUES ('Alice');
INSERT INTO innocent (name) VALUES ('Bob');

-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
);
```

## **Step 2: Fuzz Testing**

### **Custom Fuzz Testing**

**Create a file named `custom_fuzz.py` with this code:**

```python
import requests

# List of SQL injection payloads
payloads = [
    "' OR '1'='1",
    '" OR "1"="1',
    "'; DROP TABLE users--",
    "' OR '1'='1' --",
    "') OR ('1'='1",
    "'; INSERT INTO users (username, password) VALUES ('hacker', 'password')--",
    "'; UPDATE users SET password='newpassword' WHERE username='admin'--",
    "' UNION SELECT NULL, username, password FROM users--",
    "'; DELETE FROM innocent--",
    # Add more payloads as needed
]

def fuzz_test():
    url = "http://127.0.0.1:8000/search"
    
    for payload in payloads:
        try:
            response = requests.get(url, params={'q': payload})
            print(f"Payload: {payload}, Status Code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Payload: {payload}, Error: {str(e)}")

if __name__ == "__main__":
    fuzz_test()
```

**Explanation:**
- This script sends HTTP requests with various SQL injection payloads to your FastAPI app and prints out the responses.
- It's useful for finding if any of the payloads cause unexpected behavior or errors.

### **Hypothesis-Based Testing**

**Create a file named `fuzz_hypothesis.py` with this code:**

```python
from fastapi.testclient import TestClient
from main import app
from hypothesis import given, strategies as st

client = TestClient(app)

# Define how to generate test inputs
sql_injection_patterns = st.one_of(
    st.just("' OR '1'='1"),
    st.just('" OR "1"="1'),
    st.just("'; DROP TABLE users--"),
    st.just("'; INSERT INTO users (username, password) VALUES ('hacker', 'password')--"),
    st.text(min_size=1, max_size=100)  # Random normal inputs
)

@given(q=sql_injection_patterns)
def test_search(q):
    response = client.get("/search", params={"q": q})
    print(f"Payload: {q}, Status Code: {response.status_code}, Response: {response.text}")
    assert response.status_code == 200
    # Add checks here if needed

if __name__ == "__main__":
    test_search()
```

**Explanation:**
- This script uses Hypothesis to generate various inputs, including SQL injection payloads.
- It sends these inputs to your FastAPI app and prints the results to help identify vulnerabilities.

## **Step 3: Mitigation Strategies**

To fix SQL injection vulnerabilities, follow these steps:

### **1. Use Parameterized Queries**

Modify your code to use parameterized queries. This way, user input is treated as data, not executable code.

**Update `main.py` to use parameterized queries:**

```python
@app.get('/search', response_model=List[Dict[str, str]])
async def search(q: str = Query('', description="Query parameter for search")):
    query = "SELECT * FROM innocent WHERE name = ?"
    results = query_database(query, (q,))
    return JSONResponse(content=results)

def query_database(query: str, params: tuple) -> List[Dict]:
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [{'name': row[0]} for row in results]
```

**Explanation:**
- `?` is a placeholder for parameters in the query.
- Parameters are passed as a tuple to the `execute` method, ensuring user inputs are safely handled.

### **2. Use an ORM**

Consider using an Object-Relational Mapping (ORM) library like SQLAlchemy. ORMs provide an abstraction layer for database interactions, making it easier to avoid SQL injection.

**Example using SQLAlchemy:**

**Install SQLAlchemy:**

```bash
pip install sqlalchemy
```

**Update `main.py` to use SQLAlchemy:**

```python
from fastapi import FastAPI, Query
from typing import List, Dict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.responses import JSONResponse

app = FastAPI()

DATABASE_URL = "sqlite:///./example.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Innocent(Base):
    __tablename__ = "innocent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

def query_database(name: str) -> List[Dict]:
    db = SessionLocal()
    results = db.query(Innocent).filter(Innocent.name == name).all()
    db.close()
    return [{'name': result.name} for result in results]

@app.get('/search', response_model=List[Dict[str, str]])
async def search(q: str = Query('', description="Query parameter for search")):
    results = query_database(q)
    return JSONResponse(content=results)
```

**Explanation:**
- SQLAlchemy abstracts away direct SQL queries and helps prevent SQL injection by using ORM models.

### **3. Validate and Sanitize Inputs**

Always validate and sanitize user inputs to ensure they meet expected formats and values.

**Example of input validation:**

```python
from pydantic import BaseModel, constr

class SearchQuery(BaseModel):
    q: constr(min_length=1, max_length=100)

@app.get('/search', response_model=List[Dict[str, str]])
async def search(query: SearchQuery):
    q = query.q
    results = query_database(q)
    return JSONResponse(content=results)
```

**Explanation:**
- `constr` from Pydantic ensures the input adheres to the specified constraints.

### **4. Monitor and Log**

Implement logging to monitor and record all queries and their results. This helps in identifying and responding to unusual or suspicious activities.

**Example of logging:**

```python
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)

@app.get('/search', response_model=List[Dict[str, str]])
async def search(q: str = Query('', description="Query parameter for search")):
    logging.info(f"Received query: {q}")
    query = "SELECT * FROM innocent WHERE name = ?"
    results = query_database(query, (q,))
    logging.info(f"Query result: {results}")
    return JSONResponse(content=results)
```

**Explanation:**
- Logs incoming queries and their results to help detect any unusual activity.

## **Running the Tests**

1. **Start your FastAPI app:**

    ```bash
    uvicorn main:app --reload
    ```

2. **Run the custom fuzz test:**

    ```bash
    python custom_fuzz.py
    ```

3. **Run the Hypothesis tests:**

    ```bash
    python fuzz_hypothesis.py
    ```

By following this tutorial, you’ll be able to test for SQL injection vulnerabilities and apply effective fixes to secure your FastAPI application.