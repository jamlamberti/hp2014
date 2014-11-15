#from __future__ import print_function
import json
testing = False
try:
    import alchemyapi
    import db_manager
except:
    import os, inspect, sys
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import alchemyapi
    import db_manager
def get_to_parse(conn):
    sql = "SELECT * from preparse"
    args = ()
    r = conn.execute_all(sql, )
    return r
def get_comments(conn, pid):
    sql = "SELECT * from comments where uid=%s"
    args = (pid)
    r = conn.execute_all(sql, args)
    return r
def insert_row(conn, table, args):
    sql = "INSERT into " + table + " VALUES(%s, '%s', '%s', %s, %s, %s, %s, %s)"
    print(sql)
    print(args)
    print(sql%args)
    conn.execute_all(sql%args)
    return True
def delete_row(conn, table, args):
    sql = "DELETE from " + table + " where id=%s"
    conn.execute_all(sql, args)
def sentiment_analysis(text):
    #aw = AlchemyWrapper()
    #aw.sentiment_analysis("This is an awesome test!")
    api = alchemyapi.AlchemyAPI()
    response = api.sentiment('text', text)
    if response['status'] == 'OK':
        #print(json.dumps(response, indent=4))
        #print('')
        print('type: ', response['docSentiment']['type'])
        if 'score' in response['docSentiment']:
            #print('score: ', response['docSentiment']['score'])
            return response['docSentiment']['score']
    else:
        print('Error in sentiment call: ', response['statusInfo'])
    return 0

def run():
    db = db_manager.DatabaseAccess('localhost', 'root', 'root', 'grades')
    db.connect()
    r = get_to_parse(db)
    for row in r:
        pid, prof, school, helpful, clarity, easiness  = row
        pid = int(pid)
        helpful = int(helpful)
        clarity = int(clarity)
        easiness = int(easiness)
        comments = get_comments(db, pid)
        sentiment = 0
        for iid, uid, comment in comments:
            sentiment += float(sentiment_analysis(comment))*100
            delete_row(db, 'comments', iid)
        if len(comments) > 0:
            sentiment /= len(comments)

        #sentiment = float(sentiment_analysis(comment))*100
        #sentiment = float(0.78)*100
        print(sentiment)
        overall = int(100*(helpful + clarity + easiness + sentiment)/(50+50+50+100))
        args = (pid, prof, school, helpful, clarity, easiness, sentiment, overall)
        if insert_row(db, 'postparse', (pid, prof, school, helpful, clarity, easiness, sentiment, overall)):
            delete_row(db, 'preparse', (pid))
    db.close()
if __name__ == "__main__":
    if (testing):
        sentiment_analysis('This is an awful line of code')
        sentiment_analysis('This is an amazing line of code!!')
    else:
        import time
        while True:
            time.sleep(30)
            run()
