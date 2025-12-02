import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',  # Cambia por tu host de MySQL
        user='root',  # Cambia por tu usuario de MySQL
        password='root',  # Cambia por tu contraseña de MySQL
        database='unida',  # Cambia por tu base de datos
        auth_plugin_map={"caching_sha2_password": "pymysql.auth.caching_sha2_password"}
    )
    return conn
    
    if __name__ == "__main__":
        try:
            conn = get_db_connection()
            print("Conexión exitosa a la base de datos.")
            conn.close()
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")
            