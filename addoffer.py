params = tuple(currentCall.initialText.split(' ',2))
if len(params) == 3:
    say("You have %s of %s available %s!" % params)
else:
    say('I don\'t understand. Please send "[wieght] [crop] [date]"')
