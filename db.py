# import MySQLdb
# import MySQLdb.cursors as cors
# from dotenv import dotenv_values

# env = dotenv_values(".env")

# MYSQL_DIALECT = env['MYSQL_DIALECT']
# MYSQL_DRIVER = env['MYSQL_DRIVER']
# MYSQL_HOST = env['MYSQL_HOST']
# MYSQL_USER = env['MYSQL_USER']
# MYSQL_PASSWORD = env['MYSQL_PASSWORD']
# MYSQL_DB = env['MYSQL_DB']
# MYSQL_PORT = env['MYSQL_PORT']

# # Create connection to db
# db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, charset='utf8', cursorclass=cors.DictCursor)

# # Acruire cursor
# cursor = db.cursor()

# # Execute SQL
# cursor.execute("SELECT VERSION()")

# # Fetch a single row
# data = cursor.fetchone()
# print("Database version: %s" % data)

# # Close connection
# db.close()
