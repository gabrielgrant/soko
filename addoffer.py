#from __future__ import print_function

import datetime

import urllib
import urllib2

#def say(x): print x

class myobj(object): pass
"""
currentCall = myobj()
currentCall.initialText = 'post 50kg coffee may 3'
currentCall.callerID = 9802242234
ask = print
say = print
log = print
"""


"""
register NAME @ LOCATION
post QTY PRODUCT DATE
sold QTY PRODUCT PRICE [date] (optional date is inferred automatically if missing)
sales
help [register|offer|sell]

Future expansion:
unpost - remove a previous posting
offer - send an offer to a farmer

"""

class ParseError(Exception):
    pass



#class Action(object):
#    def __init__(self, **kwargs):
#        for k,v in kwargs.iteritems():
#            setattr(self, k, v)
#
#class Ask(Action):
#    """options_dict comes from tropo definition"""
#    params = 'question', 'options_dict'
#class Send(Action):
#    params = 'text',
#class Submit(Action):
#    params = 'form_name', 'params'


def parse_cmd(text):
    if text.strip().lower() == 'help':
        return 'help', ''
    try:
        cmd, params = tuple(text.split(' ',1))
    except ValueError:
        raise ParseError
    return cmd, params

    cmd, params = params[0], params[1:]
    if cmd == 'help':
        return cmd, params
    params = tuple(text.split(None,2))
    try:
        params = tuple(text.split(' ',2))
    except:
        return None
    if len(params) == 3:
        return cmd, params

def parse_text(text):
    cmd, param_string = parse_cmd(text)
    parse_fn = globals().get('parse_%s' % cmd, parse_help)
    params = parse_fn(param_string)
    return cmd, params

def parse_register(param_string):
    try:
        name, location = param_string.split('@', 1)
    except ValueError:
        raise ParseError('"register" requires name and location')
    return name, location

def do_register(name, location):
    """ Register yourself in the system as a seller.

        Usage: "register NAME @ LOCATION"
    """
    def timeout():
        params = {
            'userid': currentCall.callerID,
            'name': name,
            'location': location,
        }
        send_to_form('register', params)
        #say("OK, you're registered")
    confirmation = 'Your name is %s. You are located at %s.' % (name, location)
    #
    timeout()
    say("OK, you're registered: " + confirmation)
    """
    result = ask(
        confirmation + 'Reply "no" if this is wrong.',
        {
            "choices" : "no,n,No,NO,nO",
            'onTimeout': timeout,
            "timeout": 10.0,
        })
    say("OK, your registration has been cancelled")
    """

def parse_post(param_string):
    params = param_string.split(None, 2)
    if len(params) != 3:
        raise ParseError('"post" requires quantity, product and date available')
    return params
def do_post(qty, product, date):
    """ Post a product for sale

        Usage: "post QTY PRODUCT DATE_AVAILABLE"
    """
    def timeout():
        params = {
            'userid': currentCall.callerID,
            'product': product,
            'quantity': qty,
            'date': date,
        }
        send_to_form('post', params)
        #say("OK, we've recorded your post")
    confirmation = 'You have %s of %s available %s.' % (qty, product, date)
    timeout()
    say("OK, we've recorded your post: " + confirmation)
    """
    result = ask(
        confirmation + 'Reply "no" if this is wrong.',
        {
            "choices" : "no,n,No,NO,nO",
            'onTimeout': timeout,
            "timeout": 10.0,
        })
    say("OK, your post has been cancelled")
    """

def parse_sold(param_string):
    params = param_string.split(None, 3)
    if len(params) < 3:
        raise ParseError('"sold" requires quantity, product and price')
    return params

def do_sold(qty, product, price, date=None):
    """ Report a sale.

        sold QTY PRODUCT PRICE [date]

        optional date is inferred automatically if missing
    """
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def timeout():
        params = {
            'userid': currentCall.callerID,
            'product': product,
            'quantity': qty,
            'price': price,
            'date': date,
        }
        send_to_form('sold-full', params)
        #say("OK, we've recorded your sale")
    confirmation = 'You sold %s of %s on %s.' % (qty, product, date)
    timeout()
    say("OK, we've recorded your sale: " + confirmation)
    """
    result = ask(
        confirmation + 'Reply "no" if this is wrong.',
        {
            "choices" : "no,n,No,NO,nO",
            'onTimeout': timeout,
            "timeout": 10.0,
        })
    if result.value.lower() == 'no':
        say("OK, your sale has been cancelled")
    """

def do_recordable(confirmation_message, affirmation_message, cancellation_message, form_name, params):
    pass

def parse_help(param_string):
    if param_string.strip() not in ('', 'register', 'post', 'sold', 'help',):
        raise ParseError('"help" doesn\' recognize the command given')
    return param_string.split()

def do_help(sub_cmd=None):
    """ Get help with the system's commands.

    Usage: "help [register|offer|sell]"
    """
    if sub_cmd is None:
        say("Available commands: register offer sell\n"
            '\nFor help with a specific command, send "help COMMAND_NAME"')
        return
    call_fn = get_call_fn(sub_cmd)
    say(sub_cmd + '\n\n' + call_fn.__doc__)


# mapping of human-readable field names to the names of the form fields
# automatically assigned by Google Docs (via view-source on HTML form)
name2fields = {
    'register': {
        'userid': 'entry.1659283833',
        'name': 'entry.1700624017',
        'location': 'entry.1622679819',
    },
    'sold-full': {
        'userid': 'entry.918800942',
        'product': 'entry.332541659',
        'quantity': 'entry.49792857',
        'price': 'entry.1148698341',
        'date': 'entry.39340761',
    },
    'post': {
        'userid': 'entry.1109230072',
        'product': 'entry.27283378',
        'quantity': 'entry.196741524',
        'date': 'entry.899181608',
    }
}

"""
registrations should be private
posts should be public
"""

#cmd, param_string = parse_text(currentCall.initialText)
#if not params:
#    say('I don\'t understand. Please send "[weight] [crop] [date]"')
#    raise RuntimeError

#say('You have %s of %s available %s. Reply "no" if this is wrong' % params)


def get_call_fn(cmd):
    return globals().get('do_%s' % cmd, do_help)

def call_cmd(cmd, params):
    call_fn = get_call_fn(cmd)
    return call_fn(*params)

def main(text):
    try:
        cmd, params = parse_text(text)
    except ParseError:
        msg = "Sorry, I didn't understand: %s\n\n" # % e.message
        say(msg + "Please try again or send \"help\" for more info")
        return
    call_cmd(cmd, params)


forms = {
    'register': 'https://docs.google.com/forms/d/1DqeQfBPtgIywxSxyhPBsJfLCEfb084-Wr84pkqvbDg0/formResponse',
    'post': 'https://docs.google.com/forms/d/1azMo-5q2Zso7GAptI_aehwNcomv0REjVwpjkeQTRTDE/formResponse',
    'sold-full': 'https://docs.google.com/forms/d/1TBzL_4ymf2rKnmy-xfiuy8WhDoQWibb9-K5G_kwgHns/formResponse',
    'sold-filtered': '',
}

def send_to_form(form_name, params):
    values = {}
    for k,v in params.iteritems():
        values[name2fields[form_name][k]] = v
    data = urllib.urlencode(values)
    url = forms[form_name]
    req = urllib2.Request(url, data)
    return urllib2.urlopen(req)


log(__name__)

if __name__ in ('__main__', '__builtin__'):
    log('calling main(%s)' % currentCall.initialText)
    main(currentCall.initialText)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
