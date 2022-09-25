import psycopg2

def create_tables(con):
    with con.cursor() as cur:
        cur.execute("""
        DROP TABLE phonenumbers;
        DROP TABLE clients;
        """)
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(40),
            surname VARCHAR(40),
            email VARCHAR(40) UNIQUE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonenumbers(
            phonenumber_id SERIAL,
            phonenumber VARCHAR(40),
            client_id INTEGER REFERENCES clients(client_id)
        );
        """)
        conn.commit()
    return

def get_id(cursor, phonenumber):
    cursor.execute("""
    SELECT client_id FROM phonenumbers WHERE phonenumber=%s;
    """, (phonenumber,))
    return cursor.fetchone()

def add_phonenumber(cursor, phonenumber, client_id):
    cursor.execute("""
    INSERT INTO phonenumbers(phonenumber, client_id) VALUES(%s, %s);
    """, (phonenumber, client_id))
    return

def add_client_data(cursor, name, surname, email, phonenumber=None):
    cursor.execute("""
        INSERT INTO clients(name, surname, email) VALUES(%s, %s, %s)
        RETURNING client_id;""",
        (name, surname, email))
    client_id = cursor.fetchone()
    if phonenumber:    
        add_phonenumber(cursor, phonenumber, client_id)
    return

def change_name(cursor, new_name, client_id):
    cursor.execute("""
        UPDATE clients SET name=%s WHERE client_id%=;
        """, (new_name, client_id))
    return

def change_surname(cursor, new_surname, client_id):
    cursor.execute("""
        UPDATE clients SET surname=%s WHERE client_id=%s;
        """, (new_surname, client_id))
    return

def change_email(cursor, new_email, client_id):
    cursor.execute("""
        UPDATE clients SET email=%s WHERE client_id=%s;
        """, (new_email, client_id))
    return

def change_phonenumber(cursor, new_phonenumber, client_id):
    cursor.execute("""
        UPDATE phonenumbers SET phonenumber=%s WHERE client_id=%s;
        """, (new_phonenumber, client_id))
    return

def change_data(cursor, client_id, new_name=None, new_surname=None, new_email=None, new_phonenumber=None):
    if new_name:
        change_name(cursor, new_name, client_id)
    if new_surname:
        change_surname(cursor, new_surname, client_id)
    if new_email:
        change_email(cursor, new_email, client_id)
    if new_phonenumber:
        change_phonenumber(cursor, new_phonenumber, client_id)
    return

def delete_phone(cursor, phonenumber):
    
    cursor.execute("""
        DELETE FROM phonenumbers WHERE phonenumber=%s;
        """, (phonenumber,))
    return

def delete_client(cursor, client_id):
    cursor.execute("""
        DELETE FROM phonenumbers WHERE client_id=%s;
        """, (client_id,))

    cursor.execute("""
        DELETE FROM clients WHERE client_id=%s;
        """, (client_id,))
    return

def find_by_name(cursor, name):
    cursor.execute("""
    SELECT * FROM clients WHERE name=%s;
    """, (name,))
    print(cursor.fetchall())
    return

def find_by_surname(cursor, surname):
    cursor.execute("""
    SELECT * FROM clients WHERE surname=%s;
    """, (surname,))
    print(cursor.fetchall())
    return  

def find_by_email(cursor, email):
    cursor.execute("""
    SELECT * FROM clients WHERE email=%s;
    """, (email,))
    print(cursor.fetchall())
    return

def find_by_phonenumber(cursor, phonenumber):
    client_id = get_id(cursor, phonenumber)
    cursor.execute("""
    SELECT * FROM clients WHERE client_id=%s;
    """, (client_id,))
    print(cursor.fetchall())
    return

def find_client(cursor, name=None, surname=None, email=None, phonenumber=None):
    if name:
        find_by_name(cursor, name)
    if surname:
        find_by_surname(cursor, surname)
    if email:
        find_by_email(cursor, email)
    if phonenumber:
        find_by_phonenumber(cursor, phonenumber)
    return 



with psycopg2.connect(database="homework_5_db", user="postgres", password="пароль") as conn:
    create_tables(conn)
    with conn.cursor() as cur:
        add_client_data(cur, "Василий", "Пупкин", "vasily_p@gmail.com", phonenumber=None)
        add_client_data(cur, "Ирина", "Кузина", "irina_p@gmail.com", phonenumber=None) 
        add_client_data(cur, "Николай", "Козлов", "kolya_kozel@gmail.com", phonenumber="1234567")   
        add_phonenumber(cur, "3333333", 1)
        add_phonenumber(cur, "2222222", 2)
        add_phonenumber(cur, "1111111", 2)
        add_phonenumber(cur, "5555555", 2)
        change_data(cur, 2, new_name=None, new_surname="Пупкина", new_email=None, new_phonenumber=None)
        delete_phone(cur, "1111111")
        delete_client(cur, 2)
        find_client(cur, name="Николай", surname=None, email=None, phonenumber=None)
        find_client(cur, name=None, surname=None, email=None, phonenumber="3333333")

        conn.commit()
