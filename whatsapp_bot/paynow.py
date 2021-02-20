from paynow import Paynow


def index():
    paynow = Paynow(
    '9437',
	'5f8250e8-1c59-4d2c-ba00-8bd74693e6c2',
    'http://example.com/gateways/paynow/update', 
    'http://example.com/return?gateway=paynow'
    )

    # Create new payment and pass in the reference and payer's email address
    payment = paynow.create_payment('Order #100', 'test@example.com')

    # Passing in the name of the item and the price of the item
    payment.add('Bananas', 2.50)
    payment.add('Apples', 3.40)

    # Save the response from paynow in a variable
    response = paynow.send(payment)
