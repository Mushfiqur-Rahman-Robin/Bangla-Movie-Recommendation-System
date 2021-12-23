from key import keyid, keysecret

import razorpay

client = client = razorpay.Client(auth=(keyid, keysecret))

data = {

    'amount': 100*100,
    'currency': 'INR',
    'receipt': 'paymentdone',
    'notes': {
        'name': 'mushfiq',
        'payment_for': 'subscription'
    }

}

order = client.order.create(data=data)
print(order)


#datadict = {'razorpay_payment_id': 'pay_IabKrtBRPs6YhI', 
#'razorpay_order_id': 'order_IabJQNFH9j096P', 
#'razorpay_signature': '3c9807ba5d844ae76520cd0f2bb75d3a987204472d4406638d0a7c767c3ad3f0'}

#res = client.utility.verify_payment_signature(datadict)
#print(res)