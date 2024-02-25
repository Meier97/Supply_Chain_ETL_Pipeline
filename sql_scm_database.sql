-- Erstellen der Customer-Tabelle
CREATE TABLE Customer (
    Customer_ID INT PRIMARY KEY,
    Customer_Country VARCHAR(255)
);

-- Erstellen der Product-Tabelle
CREATE TABLE Product (
    Product_ID INT PRIMARY KEY,
    Product_Name VARCHAR(255),
    Product_Category VARCHAR(255),
    Product_Department VARCHAR(255)
);

-- Erstellen der Order-Tabelle
CREATE TABLE Orders (
    Order_ID INT PRIMARY KEY,
    Order_Date DATETIME,
    Order_Time TIME,
    Customer_ID INT,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID),
    Shipment_Date DATETIME,
    Shipment_Mode VARCHAR(255),
    Shipment_Days_Scheduled INT,
    Gross_Sales DECIMAL(10, 2),
    Discount_Percentage VARCHAR(255),
    Profit DECIMAL(10, 2)
);

-- Erstellen der Order_Item-Tabelle
CREATE TABLE Order_Item (
    Order_Item_ID INT PRIMARY KEY,
    Order_ID INT,
    FOREIGN KEY (Order_ID) REFERENCES Orders(Order_ID),
    Order_Quantity INT,
    Product_ID INT,
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID)
);

-- Erstellen der Warehouse_Inventory-Tabelle
CREATE TABLE Warehouse_Inventory (
    Inventory_ID INT PRIMARY KEY,
    Product_ID INT,
    FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID),
    Warehouse_Inventory INT,
    Inventory_Date DATE,
    Inventory_Cost_Per_Unit DECIMAL(10, 2)
);

-- Änderungen an Tabellen
-- ALTER TABLE Orders
-- ADD COLUMN Product_ID INT,
-- ADD CONSTRAINT fk_order_product
-- FOREIGN KEY (Product_ID)
-- REFERENCES Product(Product_ID);

ALTER TABLE warehouse_inventory
DROP COLUMN Inventory_ID,
ADD PRIMARY KEY (Product_ID, Inventory_Date);