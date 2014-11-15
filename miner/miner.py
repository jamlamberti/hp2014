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
    #from alchemyapi import AlchemyAPI
#class SentimentAnalysis(object):
#    def __init__(self):
#        pass
#    def parse(s):
#        pass
# 
#class AlchemyWrapper(object):
#    def __init__():
#        self.api = AlchemyAPI()
#    def sentiment_analysis(text):
#        resp = self.api.sentiment('text', text)
#        if resp['status'] == 'OK':
#            x = json.dump(resp, indent=4)
#            #print '################################'
#            #print 'type: ' + resp['docSentiment']['type']
#            #print "################################"
#            #if 'score' in resp['docSentiment']:
#            #    print 'score: ' + resp['docSentiment']['type']
#        else:
#            pass
#            #print 'Error in call: %s'%resp['statusInfo']

if __name__ == '__main__':
    #aw = AlchemyWrapper()
    #aw.sentiment_analysis("This is an awesome test!")
    alchemyapi = alchemyapi.AlchemyAPI()
    response = alchemyapi.sentiment('text', "This is my super awesome test!")
    if response['status'] == 'OK':
        print(json.dumps(response, indent=4))
    
        print('')
        print('type: ', response['docSentiment']['type'])
        if 'score' in response['docSentiment']:
            print('score: ', response['docSentiment']['score'])
    else:
        print('Error in sentiment call: ', response['statusInfo'])
