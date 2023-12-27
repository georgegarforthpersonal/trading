import psycopg2


# Establish connection to your PostgreSQL database
conn = psycopg2.connect(
    dbname="postgres",
    user="georgegarforth",
    password="Touc@n16",
    host="127.0.0.1",
    port="5434"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS forex (
        id SERIAL PRIMARY KEY,
        base_currency VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
'''

cur.execute(create_table_query)
print("Table created successfully!")

# Insert data into the table
insert_query = '''
    INSERT INTO users (username, email)
    VALUES (%s, %s);
'''

# Sample data to insert
user_data = [
    ("john_doe", "john@example.com"),
    ("jane_smith", "jane@example.com"),
    ("mike_jones", "mike@example.com")
]

cur.executemany(insert_query, user_data)
conn.commit()
print("Data inserted successfully!")

# Close communication with the database
cur.close()
conn.close()

