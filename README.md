# Supply_Chain_ETL_Pipeline

EN below
 
ETL-Pipeline für Lagerbestands- und Verkaufsdaten

Überblick

Dieses Repository enthält eine ETL (Extract, Transform, Load)-Pipeline zur Verarbeitung von Lagerbestands- und Verkaufsdaten. Die Pipeline ermöglicht die Extraktion von Daten aus einer CSV-Datei, deren Transformation für eine Staging-Datenbank und schließlich deren Laden in ein finales Datenbankschema. Die Daten für dieses Projekt sind keine echten Daten, sondern zwecks Demonstration der ETL-Pipeline von Kaggle runtergelandene Daten. Quelle: https://www.kaggle.com/datasets/shreydevil/supply-chain

Funktionalitäten

Import von Lagerbestands- und Verkaufsdaten aus einer CSV-Datei
Transformation der Daten für die Staging-Datenbank
Laden der Daten in die Staging-Datenbank
Herunterladen und erneute Transformation der Daten für das finale Datenbankschema
Visualisierung der Daten mit Power BI
Durchführung einer explorativen Datenanalyse (EDA)
Vorhersage des künftigen Lagerbestands mithilfe eines XGBoost-Algorithmus
Verzeichnisstruktur
bash

Copy code
|- data/
|  |- inventory.csv              # Rohdaten
|  |- orders_and_shipments.csv   # Rohdaten
|- scripts/
|  |- Data_Upload_Inventory.py  # Geringfügige Transformation und Upload in Staging-Datenbank der Lagerbestandsdaten (sql_staging_inventory)
|  |- Data_Upload_Orders.py     # Geringfügige Transformation und Upload in Staging-Datenbank der Sales-Daten (sql_staging_orders)
|  |- Data_Transformation.py    # Download der Daten aus der Staging-Datenbank, Transformation in Zielformat und Upload in finales Datenbankschema (sql_scm_database.sql)
|  |- sql_scm_database.sql      # SQL-Skript für finales Datenbank-Schema
|  |- sql_staging_inventory.sql # SQL-Skript für Staging-Datenbank der Lagerbestandsdaten
|  |- sql_staging_orders.sql    # SQL-Skript für Staging-Datenbank der Sales-Daten
|  |- EDA_inventory.ipynb       # Jupyter Notebook für die explorative Datenanalyse
|  |- ML-Algorithmus.ipynb      # Skript zur Vorhersage des Lagerbestands
|- docs/
|  |- README.md                 # Dokumentation
|- power_bi/
|  |- scm_data_analysis.pbix    # Power BI Dashboard

Systemanforderungen
Python 3.x
Power BI Desktop

Verwendung
Um diese ETL-Pipeline für Lagerbestands- und Verkaufsdaten zu verwenden, folgen Sie diesen Schritten:

Datenimport: Beginnen Sie mit dem Import der Rohdaten. Platzieren Sie die CSV-Dateien inventory.csv (für den Lagerbestand) und orders_and_shipments.csv (für Verkaufsdaten) im Verzeichnis data/.

Datenverarbeitung und Upload in die Staging-Datenbank: Führen Sie die Skripte Data_Upload_Inventory.py und Data_Upload_Orders.py aus, um die Daten zu transformieren und in die Staging-Datenbank hochzuladen. Überprüfen Sie die SQL-Skripte sql_staging_inventory.sql und sql_staging_orders.sql für die Struktur der Staging-Datenbanktabellen.

Daten herunterladen und Transformation für das finale Datenbankschema: Führen Sie das Skript Data_Transformation.py aus, um die Daten aus der Staging-Datenbank herunterzuladen, zu transformieren und in das finale Datenbankschema hochzuladen. Überprüfen Sie das SQL-Skript sql_scm_database.sql für die Struktur des finalen Datenbankschemas.

Explorative Datenanalyse (EDA): Verwenden Sie das Jupyter Notebook EDA_inventory.ipynb, um eine explorative Datenanalyse der Lagerbestandsdaten durchzuführen.

Vorhersage des künftigen Lagerbestands: Führen Sie das Skript ML-Algorithmus.ipynb aus, um mithilfe des XGBoost-Algorithmus eine Vorhersage des künftigen Lagerbestands zu erstellen.

Visualisierung mit Power BI: Öffnen Sie das Power BI-Dashboard scm_data_analysis.pbix, um die Daten visuell zu analysieren und Einblicke zu gewinnen.

Bitte beachten Sie, dass für die Ausführung der Pipeline Python, SQL und Jupyter Notebook (für die EDA) erforderlich sind. Stellen Sie sicher, dass Sie die erforderlichen Bibliotheken installiert haben, bevor Sie die Skripte ausführen.

Hinweis
Stellen Sie sicher, dass Sie Zugriff auf eine laufende Datenbank haben, um die Daten zu laden.

Beitrag
Fragen, Anregungen oder Verbesserungsvorschläge sind jederzeit willkommen! Zögern Sie nicht, ein Issue zu öffnen oder einen Pull-Request einzureichen.

Autor
Dieses Projekt wurde von Meier97 entwickelt.


ETL pipeline for inventory and sales data.

Overview
This repository contains an ETL (Extract, Transform, Load) pipeline for processing inventory and sales data. The pipeline facilitates data extraction from a CSV file, their transformation for a staging database, and finally loading into a final database schema. The data used for this project only serves demonstration purposes and does not represent real-life transacttions. Source: https://www.kaggle.com/datasets/shreydevil/supply-chain

Features
Import of inventory and sales data from a CSV file
Transformation of data for the staging database
Loading of data into the staging database
Download and re-transformation of data for the final database schema
Visualization of data with Power BI
Conducting exploratory data analysis (EDA)
Prediction of future inventory using an XGBoost algorithm
Directory Structure
bash
Copy code
|- data/
|  |- inventory.csv              # Raw data
|  |- orders_and_shipments.csv   # Raw data
|- scripts/
|  |- Data_Upload_Inventory.py  # Minor transformation and upload to staging database of inventory data (sql_staging_inventory)
|  |- Data_Upload_Orders.py     # Minor transformation and upload to staging database of sales data (sql_staging_orders)
|  |- Data_Transformation.py    # Download data from staging database, transform into target format, and upload to final database schema (sql_scm_database.sql)
|  |- sql_scm_database.sql      # SQL script for final database schema
|  |- sql_staging_inventory.sql # SQL script for staging database of inventory data
|  |- sql_staging_orders.sql    # SQL script for staging database of sales data
|  |- EDA_inventory.ipynb       # Jupyter Notebook for exploratory data analysis
|  |- ML-Algorithmus.ipynb      # Script for predicting inventory
|- docs/
|  |- README.md                 # Documentation
|- power_bi/
|  |- scm_data_analysis.pbix    # Power BI Dashboard

System Requirements
Python 3.x
Power BI Desktop

Usage
To use this ETL pipeline for inventory and sales data, follow these steps:

Data Import: Begin by importing the raw data. Place the CSV files inventory.csv (for inventory) and orders_and_shipments.csv (for sales data) in the data/ directory.

Data Processing and Upload to Staging Database: Execute the scripts Data_Upload_Inventory.py and Data_Upload_Orders.py to transform the data and upload it to the staging database. Check the SQL scripts sql_staging_inventory.sql and sql_staging_orders.sql for the structure of the staging database tables.

Data Download and Transformation for Final Database Schema: Run the script Data_Transformation.py to download the data from the staging database, transform it, and upload it to the final database schema. Check the SQL script sql_scm_database.sql for the structure of the final database schema.

Exploratory Data Analysis (EDA): Utilize the Jupyter Notebook EDA_inventory.ipynb to perform exploratory data analysis on the inventory data.

Prediction of Future Inventory: Execute the script ML-Algorithmus.ipynb to predict future inventory using the XGBoost algorithm.

Visualization with Power BI: Open the Power BI dashboard scm_data_analysis.pbix to visually analyze the data and gain insights.

Ensure that you have Python, SQL, and Jupyter Notebook (for EDA) installed before running the scripts.

Note
Ensure that you have access to a running database to load the data.

Contribution
Questions, suggestions, or improvements are always welcome! Feel free to open an issue or submit a pull request.

Author
This project was developed by Meier97.