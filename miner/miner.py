from __future__ import print_function
import json
try:
    import alchemyapi
except:
    import os, inspect, sys
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import alchemyapi
def sentiment_analysis(text):
    #aw = AlchemyWrapper()
    #aw.sentiment_analysis("This is an awesome test!")
    api = alchemyapi.AlchemyAPI()
    response = api.sentiment('text', text)
    if response['status'] == 'OK':
        print(json.dumps(response, indent=4))
    
        print('')
        print('type: ', response['docSentiment']['type'])
        if 'score' in response['docSentiment']:
            print('score: ', response['docSentiment']['score'])
    else:
        print('Error in sentiment call: ', response['statusInfo'])
if __name__ == "__main__":
    sentiment_analysis('This is an awful line of code')
    sentiment_analysis('This is an amazing line of code!!')
