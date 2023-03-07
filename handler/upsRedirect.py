from twilio.rest import Client

def ups():
    

client = Client()
call = client.calls.create(
    from_='<your-twilio-phone-number>',
    to='<your-phone-number>',
    url='<your-twiml-bin-url>'
)