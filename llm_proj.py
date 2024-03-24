import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import requests

class RAGPipeline:
    def __init__(self, trigger, actions, error_handler):
        self.trigger = trigger
        self.actions = actions
        self.error_handler = error_handler

    def execute(self):
        try:
            if self.trigger():
                for action in self.actions:
                    action()
        except Exception as e:
            self.error_handler(e)

def trigger_sql_query():
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="food_entity"
        )

        # Create cursor
        cursor = connection.cursor()

        # Execute dummy SQL query
        cursor.execute("SELECT * FROM food_items")

        # Fetch result
        result = cursor.fetchall()
        # print(result)
        # Close cursor and connection
        cursor.close()
        connection.close()

        return True

    except mysql.connector.Error as error:
        print("Error executing SQL query:", error)
        return None

def send_email():
    sender_email = "arjunviki44@gmail.com"
    receiver_email = "arjungovindarajan44@gmail.com"
    password = "kxeu tsca vhlc wzsn"
    
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Request for Data"

    text = "Please fill in the relevant data."
    html = """\
    <html>
      <body>
        <p>Please fill in the relevant data.</p>
      </body>
    </html>
    """

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def webhook():
    url = "your_webhook_url"
    payload = {"data": "Gmail response data"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

def parse_and_insert_data():

    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="food_entity"
        )

        # Create cursor
        cursor = connection.cursor()

        # Execute dummy SQL query
        cursor.execute('''CREATE TABLE if not exists mytable (Id INT, Employee_name VARCHAR(50))''')

        data_to_insert = [('1', 'Arjun'),
                          ('2', 'Vignesh'),
                          ('3', 'Vijay')]

        cursor.executemany('INSERT INTO mytable VALUES (?, ?)', data_to_insert)
        # Fetch result
        result = cursor.fetchall()
        # print(result)
        # Close cursor and connection
        cursor.close()
        connection.close()

        return result

    except mysql.connector.Error as error:
        print("Error executing SQL query:", error)
        return None

def handle_error(exception):
    print(f"An error occurred: {exception}")

pipeline = RAGPipeline(trigger_sql_query, [send_email, webhook, parse_and_insert_data], handle_error)
pipeline.execute()
