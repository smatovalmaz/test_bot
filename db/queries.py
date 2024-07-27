CREATE_TABLE_STORE = """
    CREATE TABLE IF NOT EXISTS online_stores 
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product VARCHAR(255),
    size VARCHAR(255),
    price VARCHAR(255),
    productid INTEGER,
    photo TEXT
   )
"""

INSERT_STORE = """
    INSERT INTO online_store(name_product, size, price, productid, photo)
    VALUES (?, ?, ?, ?, ?)
"""