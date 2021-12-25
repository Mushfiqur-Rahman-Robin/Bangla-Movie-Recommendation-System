from key import keyid, keysecret

import razorpay

client = razorpay.Client(auth=(keyid, keysecret))

data = {

    'amount': 100*100,
    'currency': 'INR',
    'receipt': 'Order_taken',
    'notes': {
        'name': 'mushfiq',
        'payment_for': 'subscription'
    }

}

order = client.order.create(data=data)
#print(order)



