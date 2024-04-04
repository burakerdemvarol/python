import pika
import uuid

# RabbitMQ bağlantı bilgileri
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

# Kuyruk oluşturma (varsa oluşturmaz)
channel.queue_declare(queue='hello')

def send_message():
    # Unique mesaj ID oluşturma
    message_id = str(uuid.uuid4())
    message = f"Mesaj {message_id}"
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f"Mesaj gönderildi: {message_id}")

def receive_message(ch, method, properties, body):
    message_id = body.decode()
    print(f"Mesaj alındı: {message_id}")

# Mesaj gönderme
send_message()

# Mesaj alma (callback fonksiyonu ile)
channel.basic_consume(queue='hello', on_message_callback=receive_message, auto_ack=True)
channel.start_consuming()

# Bağlantıyı kapatma
connection.close()