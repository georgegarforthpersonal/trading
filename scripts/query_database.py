import psycopg2

# Connect to the existing database
conn = psycopg2.connect(
    dbname="postgres",
    user="georgegarforth",
    password="Touc@n16",
    host="127.0.0.1",
    port="5434"
)

cur = conn.cursor()

# Execute a SELECT query to retrieve data
select_query = '''
    SELECT * FROM users;
'''

cur.execute(select_query)

# Fetch all rows from the result set
rows = cur.fetchall()

# Display the fetched rows
for row in rows:
    print(row)  # You can format and process the data as needed

# Close communication with the database
cur.close()
conn.close()