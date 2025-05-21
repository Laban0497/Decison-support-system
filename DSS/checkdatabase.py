import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('registration.db')

# Query the users table and load it into a DataFrame
query = "SELECT * FROM users"
df = pd.read_sql_query(query, conn)

# Display the DataFrame
print(df)

# Close the connection
conn.close()