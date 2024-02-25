import pandas as pd 
import numpy as np 
import mysql.connector
import project_credentials as pc
from sqlalchemy import create_engine


##################################################################
# Download der Daten aus der Staging-Datenbank:

# Verbindung zur Staging-Datenbank herstellen
def connect_to_mysql():
    connection = mysql.connector.connect(
        host=pc.my_sql_host,
        database='scm_data_staging',
        user=pc.my_sql_user,
        password=pc.my_sql_password
    )
    return connection

# Funktion zum Abrufen aller Daten aus der Tabelle 'orders'
def fetch_orders_data(connection):
    query = "SELECT * FROM orders"
    df = pd.read_sql(query, connection)
    return df

# Funktion zum Abrufen aller Daten aus der Tabelle 'inventory'
def fetch_inventory_data(connection):
    query = "SELECT * FROM inventory"
    df = pd.read_sql(query, connection)
    return df

# Verbindung zur Datenbank herstellen
connection = connect_to_mysql()

if connection:
    # Alle Daten aus der Tabelle 'orders' und 'inventory' abrufen
    orders_df = fetch_orders_data(connection)
    inventory_df_raw = fetch_inventory_data(connection)
    # Verbindung schließen
    connection.close()
    print("Alle gewünschten Daten erfolgreich heruntergeladen")
else:
    print("Fehler bei der Verbindung zur MySQL-Datenbank.")

# Download abgeschlossen
##################################################################
# Transformationen der Daten in das gewünschte Format

# Leerzeichen ersetzen durch Unterstrich in den Spaltenbezeichnungen
orders_df.columns = orders_df.columns.str.strip()
orders_df.columns = orders_df.columns.str.replace(' ', '_')

# Leerzeichen ersetzen durch Unterstrich in den Spaltenbezeichnungen
inventory_df_raw.columns = inventory_df_raw.columns.str.strip()
inventory_df_raw.columns = inventory_df_raw.columns.str.replace(' ', '_')

# Filterung der relevanten Spalten mit Erhalt der Ursprungstabelle
inventory_df_new = pd.DataFrame()
inventory_df_new[['Product_ID', 'Year_Month', 'Warehouse_Inventory', 'Inventory_Cost_Per_Unit', "Product_Name"]] = inventory_df_raw[["Product_ID", "Year_Month", "Warehouse_Inventory", "Inventory_Cost_Per_Unit", "Product_Name"]]
orders_df.drop_duplicates(inplace=True)

# Product-DataFrame für späteren Upload erzeugen aus ausgewählten Spalten aus beiden Quelltabellen. Notwendige Operation, da die orders-Tabelle nicht alle Product_IDs enthält, sondern nur die inventory-Tabelle.
product_transformation_df = pd.DataFrame()
product_transformation_df[["Product_ID", "Product_Name"]] = inventory_df_new[["Product_ID", "Product_Name"]]
select_columns_orders_df = pd.DataFrame()
select_columns_orders_df[["Product_ID", "Product_Category", "Product_Department"]] = orders_df[["Product_ID","Product_Category", "Product_Department"]]
#product_df[["Product_ID", "Product_Name", "Product_Category", "Product_Department"]] = orders_df[["Product_ID", "Product_Name", "Product_Category", "Product_Department"]]
product_df = pd.merge(product_transformation_df, select_columns_orders_df, on="Product_ID", how="left")

# Spaltennamen anpassen für Upload in mySQL
orders_df["Order_ID"] = orders_df["Order_Item_ID"]
orders_df = orders_df.rename(columns={'Shipment_Days_-_Scheduled': 'Shipment_Days_Scheduled'})
orders_df = orders_df.rename(columns={'Discount_%': 'Discount_Percentage'})
inventory_df_new = inventory_df_new.rename(columns={"Year_Month": "Inventory_Date"})

# Datentypen anpassen
orders_df['Order_ID'] = orders_df['Order_ID'].astype(int)
orders_df['Order_Item_ID'] = orders_df['Order_Item_ID'].astype(int)
orders_df['Order_YearMonth'] = orders_df['Order_YearMonth'].astype(str)
orders_df['Order_Year'] = orders_df['Order_Year'].astype(int)
orders_df['Order_Month'] = orders_df['Order_Month'].astype(int)
orders_df['Order_Day'] = orders_df['Order_Day'].astype(int)
orders_df['Order_Time'] = pd.to_datetime('1970-01-01') + orders_df['Order_Time']
orders_df['Order_Quantity'] = orders_df['Order_Quantity'].astype(int)
product_df['Product_Department'] = product_df['Product_Department'].astype(str)
product_df['Product_Category'] = orders_df['Product_Category'].astype(str)
orders_df['Product_Name'] = orders_df['Product_Name'].astype(str)
orders_df['Customer_ID'] = orders_df['Customer_ID'].astype(int)
orders_df['Customer_Market'] = orders_df['Customer_Market'].astype(str)
orders_df['Customer_Region'] = orders_df['Customer_Region'].astype(str)
orders_df['Customer_Country'] = orders_df['Customer_Country'].astype(str)
orders_df['Warehouse_Country'] = orders_df['Warehouse_Country'].astype(str)
orders_df['Shipment_Date'] = pd.to_datetime(orders_df[['Shipment_Year', 'Shipment_Month', 'Shipment_Day']].astype(str).agg('-'.join, axis=1), errors='coerce')
orders_df['Shipment_Year'] = orders_df['Shipment_Year'].astype(int)
orders_df['Shipment_Month'] = orders_df['Shipment_Month'].astype(int)
orders_df['Shipment_Day'] = orders_df['Shipment_Day'].astype(int)
orders_df['Shipment_Mode'] = orders_df['Shipment_Mode'].astype(str)
orders_df['Shipment_Days_Scheduled'] = orders_df['Shipment_Days_Scheduled'].astype(int)
orders_df['Gross_Sales'] = orders_df['Gross_Sales'].astype(float)
# Zeilen mit fehlerhaftem Wert in der Spalte "Discount_Percentage" löschen, da Umwandlung nicht funktioniert hat (1 Zeile wird gelöscht)
try:
    orders_df['Discount_Percentage'] = orders_df['Discount_Percentage'].astype(float)
except ValueError:
    # Wenn die Umwandlung fehlschlägt, lösche die entsprechende Zeile
    df = orders_df.dropna(subset=['Discount_Percentage'])
orders_df['Profit'] = orders_df['Profit'].astype(float)
orders_df['Order_Date'] = pd.to_datetime(orders_df[['Order_Year', 'Order_Month', 'Order_Day']].astype(str).agg('-'.join, axis=1), errors='coerce')
inventory_df_new["Inventory_Date"] = pd.to_datetime(inventory_df_new["Inventory_Date"], format="%Y%m")



# Ende der Transformationen
##################################################################
# Upload in das endgültige Datenbankschema

# Verbindung zur MySQL-Datenbank herstellen

def connect_to_mysql2():

    mysql_url = f'mysql+mysqlconnector://{pc.my_sql_user}:{pc.my_sql_password}@{pc.my_sql_host}:3306/scm_data_database'
    engine = create_engine(mysql_url)
    connection = engine.connect()
    return connection

def upload_to_table(data, table_name, connection, unique_key=None):
    try:
        # Wenn eine eindeutige Spalte angegeben ist, entferne Duplikate basierend auf dieser Spalte
        if unique_key:
            data = data.drop_duplicates(subset=[unique_key])

        # Daten aus dem DataFrame in die MySQL-Datenbank hochladen
        data.to_sql(name=table_name, con=connection, if_exists='append', index=False, method='multi')

        print(f'Daten wurden erfolgreich in die Tabelle {table_name} hochgeladen.')
    except Exception as e:
        print(f"Fehler beim Hochladen in die Tabelle {table_name}: {str(e)}")

def main():
    try:
        connection = connect_to_mysql2()

        if connection:
            # Customer-Tabelle
            #upload_to_table(orders_df[['Customer_ID', 'Customer_Country']], 'customer', connection, unique_key='Customer_ID')

            # Product-Tabelle
            #upload_to_table(product_df[['Product_ID', 'Product_Name', 'Product_Category', "Product_Department"]], 'product', connection, unique_key='Product_ID')

            # Order-Tabelle
            #upload_to_table(orders_df[['Order_ID', 'Order_Date', 'Order_Time',
                                  #'Customer_ID', 'Shipment_Date',
                                  #'Shipment_Mode', 'Shipment_Days_Scheduled', 'Gross_Sales', 'Discount_Percentage', 'Profit']], 'orders', connection)

            # Order_Item-Tabelle
            #upload_to_table(orders_df[['Order_Item_ID', 'Order_ID', 'Order_Quantity', 'Product_ID']], 'order_item', connection)

            # Warehouse_Inventory-Tabelle
            upload_to_table(inventory_df_new[['Product_ID', 'Warehouse_Inventory', 'Inventory_Date', 'Inventory_Cost_Per_Unit']], 'warehouse_inventory', connection)

            print('Daten wurden erfolgreich in alle Tabellen hochgeladen.')
        else:
            print("Fehler bei der Verbindung zur MySQL-Datenbank.")
    except Exception as e:
        print(f"Fehler: {str(e)}")
    finally:
        if connection:
            connection.close()
# Aufruf der Funktion main(), nur wenn das Skript direkt ausgeführt wird und nicht aufgerufen wird
if __name__ == "__main__":
    main()

# Ausgabe der transforimierten Daten in csv-Dateien für EDA und ML-Algorithmus als Alternative zum Abruf aus Datenbank

# product_df.to_csv(f'{pc.directory}product_data.csv', index=False)

# inventory_df_new.to_csv(f'{pc.directory}inventory_data.csv', index=False)

# orders_df.to_csv(f'{pc.directory}orders_data.csv', index=False)