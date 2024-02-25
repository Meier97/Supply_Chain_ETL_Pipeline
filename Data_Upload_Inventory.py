import mysql.connector
import csv
import project_credentials as pc
import pandas as pd 

# Funktion zum Verbinden zur MySQL-Datenbank
def connect_to_mysql():
    
    connection = mysql.connector.connect(
        host=pc.my_sql_host,
        database="scm_data_staging",
        user=pc.my_sql_user,
        password=pc.my_sql_password
        )
    return connection

# Funktion zum CSV-Import in die MySQL-Datenbank
def import_csv_to_mysql(connection, csv_file_path, table_name):
    cursor = connection.cursor()
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Überspringe Header-Zeile
        for row in csv_reader:
            query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(row))})"
            cursor.execute(query, tuple(row))
    connection.commit()
    print("CSV-Daten erfolgreich in MySQL-Datenbank importiert")

# Kleine Änderung an der Tabelle  
df = pd.read_csv("inventory.csv")

# Eindeutigen Index hinzufügen
df['Index'] = range(1, len(df) + 1)
df['Product ID'] = df['Product ID'].astype(int)

# DataFrame in CSV exportieren
df.to_csv('output2.csv', index=False)



table_name = 'inventory'
csv_file_path = 'output2.csv'

# Verbindung herstellen
connection = connect_to_mysql()

# CSV-Datei in die MySQL-Datenbank importieren
import_csv_to_mysql(connection, csv_file_path, table_name)

# Verbindung schließen
connection.close()