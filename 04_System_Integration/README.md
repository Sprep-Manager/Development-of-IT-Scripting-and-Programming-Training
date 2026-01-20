# Module 5: Climate System Integration (CliDE Simulation)

This directory covers **Lecture 22 & 23**, demonstrating how to programmatically connect to Climate Data Management Systems (CDMS) like **CliDE**.

## 📂 Contents

* **`db_connect_clide_simulation.py`**: A script that simulates a connection to a Climate DB using SQLite. It demonstrates creating tables, inserting data, and executing SQL queries via Python.

## 🛠️ Key Concepts

1.  **Database Connection (SQL)**:
    * In a real environment (CliDE), you would use libraries like `psycopg2` (PostgreSQL) or `mysql-connector`.
    * This training uses `sqlite3` to simulate the database structure locally without requiring server access.
2.  **SQL Querying**:
    * Writing `SELECT` statements with `JOIN` clauses to combine metadata (Station Info) and time-series data (Observations).
    * Filtering data using `WHERE` clauses for specific dates and elements (e.g., RAIN).
3.  **Pandas Integration**:
    * Using `pd.read_sql()` to directly load query results into a DataFrame for immediate analysis.

## 🚀 How to Run

```bash
# No extra installation needed (sqlite3 is built-in with Python)
# Just ensure pandas is installed
pip install pandas

# Run the simulation
python db_connect_clide_simulation.py
