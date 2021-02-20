from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from products.models import Product
from django.db.models import Q
from django.conf import settings
from cart.cart import Cart
from paynow import Paynow
from .models import PaynowPayment
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime
import emoji
import random
import json
import time
import os

# Create your views here.
def generate_transaction_id():
    """
    Generates a unique id which will be used by paynow to refer to the payment
    initiated
    """
    return str(int(time.time() * 1000))


@csrf_exempt
def index(request):
    paynow = Paynow(
    '9437',
	'5f8250e8-1c59-4d2c-ba00-8bd74693e6c2',
    'http://example.com/gateways/paynow/update', 
    'http://example.com/return?gateway=paynow'
    )
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()
        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        responded = False

        if incoming_msg == 'hello':
            response = emoji.emojize("""
*Hi! Welcome to Mushambadzi Store* :wave:
Let me assist you :wink:
You can give me the following commands:
:black_small_square: *'products':* Get a list of products on our store! :rocket:
:black_small_square: *'product <name>':* Get a detail of product on our store! *e.g product bread*
:black_small_square: *'add cart <product id> <quantity> '*: Add product to cart *e.g add cart 1 5 * 
:black_small_square: *'remove cart <product id>*: Remove item from cart e.g remove cart 1 ! *e.g remove cart 1 * 
:black_small_square: *'view cart'*: View Cart items. 
:black_small_square: *'pay cart'*: Pay cart. 
""", use_aliases=True)
            msg.body(response)
            responded = True

        elif incoming_msg == 'quote':
            # returns a quote
            r = requests.get('https://api.quotable.io/random')

            if r.status_code == 200:
                data = r.json()
                quote = f'{data["content"]} ({data["author"]})'

            else:
                quote = 'I could not retrieve a quote at this time, sorry.'

            msg.body(quote)
            responded = True

        elif incoming_msg == 'cat':
            # return a cat pic
            msg.media('https://cataas.com/cat')
            responded = True

        elif incoming_msg == 'dog':
            # return a dog pic
            r = requests.get('https://dog.ceo/api/breeds/image/random')
            data = r.json()
            msg.media(data['message'])
            responded = True


        elif incoming_msg == 'products':
            s = Product.objects.all()
            if s:
                        result = ''

                        for prod in s:
                            name = prod.name
                            price = prod.unit_price
                            prod_id = prod.id
                            vendor = prod.vendor_id.username
                            # price_count = recipe_data['pricecount']
                            # prep = recipe_data['prep']
                            # cook = recipe_data['cook']
                            # ready_in = recipe_data['ready in']
                            # calories = recipe_data['calories']

                            result += """
*{}*
Price:  ($ {} )
Product ID: *{}*
Manufacturer: {}
""".format(name, price, prod_id, vendor)

                    # else:
                    #     result = 'Sorry, I could not find any results for {}'.format(search_text)


            msg.body(result)
            responded = True

        elif incoming_msg.startswith('product'):

            # search for recipe based on user input (if empty, return featured recipes)
            search_text = incoming_msg.replace('product', '')
            search_text = search_text.strip()
            
            # data = json.dumps({'searchText': search_text})

            query = search_text
            s = Product.objects.filter(
                    Q(name__icontains=query) | Q(description__icontains=query))
            if s:
                        result = ''

                        for prod in s:
                            name = prod.name
                            price = prod.unit_price
                            prod_id = prod.id
                            vendor = prod.vendor_id.username
                            image = prod.image
                            # price_count = recipe_data['pricecount']
                            # prep = recipe_data['prep']
                            # cook = recipe_data['cook']
                            # ready_in = recipe_data['ready in']
                            # calories = recipe_data['calories']

                            result += """

*{}*
Price:  ($ {} )
Product ID: *{}*
Manufacturer: {}
""".format(name, price, prod_id, vendor)

            else:
                result = 'Sorry, I could not find any results for product {}'.format(search_text)
            # image = str(image)
            # image = image.replace('/', "\\")
            # image = image.strip()
            # base = os.path.dirname(os.path.dirname(os.path.abspath(str(image))))
            site_url = '127.0.0.1'
            image = os.path.join(site_url + '/malincol', image.url)
            msg.media(image)
            msg.body(result)
            responded = True

        elif incoming_msg.startswith('add cart'):

            # search for recipe based on user input (if empty, return featured recipes)
            search_text = incoming_msg.replace('add cart', '')
            search_text = search_text.strip()
            text = str(search_text )
            product_id, quantity, *_ = l = text.split()
            product_id = int(product_id)
            quantity = int(quantity)

            add_to_cart(request,product_id, quantity)
            cart = Cart(request)
            if(cart):

                for item in cart:
                    result = ''
                    name = item.product.name
                    quantity = item.quantity
                    total_price = item.total_price
                    
                    result += """
*{}*
Cart Qty: {}
Price:  ($ {} )
""".format(name, quantity, total_price)
                result = 'Great, We added *{}* units of *{}* to cart. Total Amount: *$* *{}*'.format(quantity, name,  total_price )

            else:
                result = 'Sorry, I could not add product: {} of quantity: {} to cart. Total Amount: *$* *{}*'.format(quantity, name,  total_price )
            # image = str(image)
            # image = image.replace('/', "\\")
            # image = image.strip()
            # base = os.path.dirname(os.path.dirname(os.path.abspath(str(image))))
            # site_url = '127.0.0.1'
            # image = os.path.join(site_url + '/mush_store', image.url)
            # msg.media(image)
            msg.body(result)
            responded = True


        elif incoming_msg.startswith('view cart'):
            separator = '  '
            s = Cart(request)
            if s:
                        result = ''

                        for item in s:
                            name = item.product.name
                            quantity = item.quantity
                            total_price = item.total_price

                            result += """
{}
*{}*
Product Quantity: {}
Total Price:  ($ {} )
""".format( separator, name, quantity, total_price)

            else:
                result = 'Sorry, I could not find any cart'

            title = '*Your Current Shopping Cart*'
            message = title + '\n'+ result
            msg.body(message)
            responded = True

        elif incoming_msg.startswith('remove cart'):
            search_text = incoming_msg.replace('remove cart', '')
            search_text = search_text.strip()
            text = str(search_text )
            product_id, *_ = l = text.split()
            product_id = int(product_id)
            remove_from_cart(request, product_id)
            s = Cart(request)
            if s:
                        result = ''
                        result = '*Your Current Shopping Cart*'

                        for item in s:
                            name = item.product.name
                            quantity = item.quantity
                            total_price = item.total_price

                            result += """

*{}*
Product Quantity: {}
Total Price:  ($ {} )
""".format(name, quantity, total_price)

            else:
                result = 'Sorry, I could not find any cart'
            # image = str(image)
            # image = image.replace('/', "\\")
            # image = image.strip()
            # base = os.path.dirname(os.path.dirname(os.path.abspath(str(image))))
            # site_url = '127.0.0.1'
            # image = os.path.join(site_url + '/mush_store', image.url)
            # msg.media(image)
            msg.body(result)
            responded = True

        elif incoming_msg.startswith('pay cart'):
            transaction_id = generate_transaction_id()

            # Generate Urls to pass to Paynow. These are generated dynamicaly
            # and should be absolute
            # result url is used by paynow system to update yo website on the status of a payment
            r = reverse('chatbot:paynow_update', args=(transaction_id, ))
            result_url = request.build_absolute_uri(r)
            # return url is the url paynow will return the payee to your site
            r = reverse('chatbot:paynow_return', args=(transaction_id,))
            return_url = request.build_absolute_uri(r)
            email = 'mpasiinnocent@gmail.com'

            print(result_url)
            print(return_url)
            # Create an instance of the Paynow class optionally setting the result and return url(s)
            paynow = Paynow(settings.PAYNOW_INTEGRATION_ID,
                            settings.PAYNOW_INTEGRATION_KEY,
                            result_url,
                            return_url,
                            )

            # Create a new payment passing in the reference for that payment(e.g invoice id, or anything that you can
            # use to identify the transaction and the user's email address.
            payment = paynow.create_payment(transaction_id, email)


            # You can then start adding items to the payment python passing in the name of the item and the price of the
            # item. This is useful when the site has a shopping cart
            s = Cart(request)
            if s:
                        for item in s:
                            payment.add(item.product.name, item.total_price)

            # When you are finally ready to send your payment to Paynow, you can use the `send` method
            # in the `paynow` object and save the response from paynow in a variable
            # response = paynow.send_mobile(payment, '0777757603', 'ecocash')
            response = paynow.send(payment)
            if response.success:
                # Get the link to redirect the user to, then use it as you see fit
                # redirect_url = response.redirect_url

                # Get the poll url (used to check the status of a transaction). You might want to save this in your DB
                poll_url = response.poll_url
                msg.body(poll_url)
                # Get instructions to display
                # instructions = response.instructions
                # msg.body(instructions)
                # msg.body(redirect_url)

            responded = True
            
        elif incoming_msg.startswith('recipe'):

            # search for recipe based on user input (if empty, return featured recipes)
            search_text = incoming_msg.replace('recipe', '')
            search_text = search_text.strip()
            
            data = json.dumps({'searchText': search_text})
            
            result = ''
            # updates the Apify task input with user's search query
            r = requests.put('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/input?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1', data = data, headers={"content-type": "application/json"})
            if r.status_code != 200:
                result = 'Sorry, I cannot search for recipes at this time.'

            # runs task to scrape Allrecipes for the top 5 search results
            r = requests.post('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            if r.status_code != 201:
                result = 'Sorry, I cannot search Allrecipes.com at this time.'

            if not result:
                result = emoji.emojize("I am searching Allrecipes.com for the best {} recipes. :fork_and_knife:".format(search_text),
                                        use_aliases = True)
                result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"
            msg.body(result)
            responded = True

        elif incoming_msg == 'get recipe':
            # get the last run details
            r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                # check if last run has succeeded or is still running
                if data['data']['status'] == "RUNNING":
                    result = 'Sorry, your previous query is still running.'
                    result += "\nPlease wait for a few moments before typing 'get recipe' to get your recipes!"

                elif data['data']['status'] == "SUCCEEDED":

                    # get the last run dataset items
                    r = requests.get('https://api.apify.com/v2/actor-tasks/o7PTf4BDcHhQbG7a2/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
                    data = r.json()

                    if data:
                        result = ''

                        for recipe_data in data:
                            url = recipe_data['url']
                            name = recipe_data['name']
                            rating = recipe_data['rating']
                            rating_count = recipe_data['ratingcount']
                            prep = recipe_data['prep']
                            cook = recipe_data['cook']
                            ready_in = recipe_data['ready in']
                            calories = recipe_data['calories']

                            result += """
*{}*
_{} calories_
Rating: {:.2f} ({} ratings)
Prep: {}
Cook: {}
Ready in: {}
Recipe: {}
""".format(name, calories, float(rating), rating_count, prep, cook, ready_in, url)

                    else:
                        result = 'Sorry, I could not find any results for {}'.format(search_text)

                else:
                    result = 'Sorry, your previous search query has failed. Please try searching again.'

            else:
                result = 'I cannot retrieve recipes at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg == 'news':
            r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-news,the-washington-post,the-wall-street-journal,cnn,fox-news,cnbc,abc-news,business-insider-uk,google-news-uk,independent&apiKey=3ff5909978da49b68997fd2a1e21fae8')
            
            if r.status_code == 200:
                data = r.json()
                articles = data['articles'][:5]
                result = ''
                
                for article in articles:
                    title = article['title']
                    url = article['url']
                    if 'Z' in article['publishedAt']:
                        published_at = datetime.datetime.strptime(article['publishedAt'][:19], "%Y-%m-%dT%H:%M:%S")
                    else:
                        published_at = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%S%z")
                    result += """
*{}*
Read more: {}
_Published at {:02}/{:02}/{:02} {:02}:{:02}:{:02} UTC_
""".format(
    title,
    url, 
    published_at.day, 
    published_at.month, 
    published_at.year, 
    published_at.hour, 
    published_at.minute, 
    published_at.second
    )

            else:
                result = 'I cannot fetch news at this time. Sorry!'

            msg.body(result)
            responded = True

        elif incoming_msg.startswith('statistics'):
            # runs task to aggregate data from Apify Covid-19 public actors
            requests.post('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/run-sync?token=qTt3H59g5qoWzesLWXeBKhsXu&ui=1')
            
            # get the last run dataset items
            r = requests.get('https://api.apify.com/v2/actor-tasks/5MjRnMQJNMQ8TybLD/runs/last/dataset/items?token=qTt3H59g5qoWzesLWXeBKhsXu')
            
            if r.status_code == 200:
                data = r.json()

                country = incoming_msg.replace('statistics', '')
                country = country.strip()
                country_data = list(filter(lambda x: x['country'].lower().startswith(country), data))

                if country_data:
                    result = ''

                    for i in range(len(country_data)):
                        data_dict = country_data[i]
                        last_updated = datetime.datetime.strptime(data_dict.get('lastUpdatedApify', None), "%Y-%m-%dT%H:%M:%S.%fZ")

                        result += """
*Statistics for country {}*
Infected: {}
Tested: {}
Recovered: {}
Deceased: {}
Last updated: {:02}/{:02}/{:02} {:02}:{:02}:{:03} UTC
""".format(
    data_dict['country'], 
    data_dict.get('infected', 'NA'), 
    data_dict.get('tested', 'NA'), 
    data_dict.get('recovered', 'NA'), 
    data_dict.get('deceased', 'NA'),
    last_updated.day,
    last_updated.month,
    last_updated.year,
    last_updated.hour,
    last_updated.minute,
    last_updated.second
    )
                else:
                    result = "Country not found. Sorry!"
            
            else:
                result = "I cannot retrieve statistics at this time. Sorry!"

            msg.body(result)
            responded = True

        elif incoming_msg.startswith('meme'):
            r = requests.get('https://www.reddit.com/r/memes/top.json?limit=20?t=day', headers = {'User-agent': 'your bot 0.1'})
            
            if r.status_code == 200:
                data = r.json()
                memes = data['data']['children']
                random_meme = random.choice(memes)
                meme_data = random_meme['data']
                title = meme_data['title']
                image = meme_data['url']

                msg.body(title)
                msg.media(image)
            
            else:
                msg.body('Sorry, I cannot retrieve memes at this time.')

            responded = True

        if not responded:
             msg.body("Sorry, I don't understand. Send 'hello' for a list of commands.")

        return HttpResponse(str(resp))


def add_to_cart(request, product_id, quantity ):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.add(product, product.unit_price, quantity)
    result = Cart(request)
    return result

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)

def get_cart(request):
    return render(request, 'cart.html', {'cart': Cart(request)})


def payment_success():
    result = 'payment successful'
    return result


def paynow_return(request, payment_id):
    """This the point where Paynow returns user to our site"""
    # Get payment object
    payment = get_object_or_404(PaynowPayment, reference=payment_id)
    # Init Paynow oject. The urls can now be blank
    paynow = Paynow(settings.PAYNOW_INTEGRATION_ID, settings.PAYNOW_INTEGRATION_KEY, '', '')

    # Check the status of the payment with the paynow server
    payment_result = paynow.check_transaction_status(payment.poll_url)

    save_changes = False

    # check if status has changed
    if payment.status != payment_result.status:
        payment.status = payment_result.status
        save_changes = True

    # Check if paynow reference has changed
    if payment.paynow_reference != payment_result.paynow_reference:
        payment.paynow_reference = payment_result.paynow_reference
        save_changes = True

    # Check if payment is now paid
    print(payment_result.paid)
    if payment_result.paid:
        if not payment.paid:
            payment.paid = True
            payment.confirmed_at = timezone.now()

    if save_changes:
        payment.save()

    msg = "Payment for Transaction " + payment.reference + ' confirmed'
    msg += " Paynow Reference: " + payment.paynow_reference
    messages.success(request, msg)
    msg = "Paynow Payment status => " + payment.status
    messages.success(request, msg)




    return redirect(reverse('index'))


def paynow_update(request, payment_reference):
    """This the point which Paynow polls our site with a payment status. I find it best to check with the Paynow Server.
     I also do the check when a payer is returned to the site when user is returned to site"""

    # Get saved paymend details
    payment = get_object_or_404(PaynowPayment, reference=payment_reference)
    # Init paynow object. The URLS can be blank
    paynow = Paynow(settings.PAYNOW_INTEGRATION_ID, settings.PAYNOW_INTEGRATION_KEY, '', '')
    # Check the status of the payment with paynow server
    payment_result = paynow.check_transaction_status(payment.poll_url)

    save_changes = False

    # check if status has changed
    if payment.status != payment_result.status:
        payment.status = payment_result.status
        save_changes = True

    # Check if paynow reference has changed
    if payment.paynow_reference != payment_result.paynow_reference:
        payment.paynow_reference = payment_result.paynow_reference
        save_changes = True

    # Check if payment is now paid
    if payment_result.paid:
        if not payment.paid:
            payment.paid = True
            payment.confirmed_at = timezone.now()

    if save_changes:
        payment.save()

    return HttpResponse('ok')
