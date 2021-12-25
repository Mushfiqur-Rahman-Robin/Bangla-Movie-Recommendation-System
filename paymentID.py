import razorpay
import sqlite3 
from key import keyid, keysecret

client = razorpay.Client(auth=(keyid, keysecret))

resp = client.payment.fetch_all()
payment_id = resp['items'][0]['id']
print('Your payment ID:', payment_id)


order_id = resp['items'][0]['order_id']
print('Your order ID:', order_id)

user = resp['items'][0]['email']
print('Your name:', user)


connn = sqlite3.connect('order.db', check_same_thread=False)
cursor = connn.cursor()

def create_idtable():
	cursor.execute('CREATE TABLE IF NOT EXISTS idtable(order_id TEXT,payment_id TEXT)')

def add_id(order_id,payment_id):
	cursor.execute('INSERT INTO idtable(order_id,payment_id) VALUES (?,?)',(order_id,payment_id))
	connn.commit()

if (payment_id == resp['items'][0]['id']):
    create_idtable()
    add_id(order_id, payment_id)

