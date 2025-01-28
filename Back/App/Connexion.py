import mysql.connector

class Connection:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Database connection established")
        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def get_connection(self):
        return self.connection
