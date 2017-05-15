import os
import json
import random
import requests
import time

from flask import Flask, request, Response


application = Flask(__name__)

# FILL THESE IN WITH YOUR INFO
my_bot_name = 'merabot' #e.g. zac_bot
my_slack_username = 'zac.wentzell' #e.g. zac.wentzell


slack_inbound_url = 'https://hooks.slack.com/services/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'


# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    # Adding a delay so that all bots don't answer at once (could overload the API).
    # This will randomly choose a value between 0 and 10 using a uniform distribution.
    # delay = random.uniform(0, 10)
    # time.sleep(delay)

    print '========POST REQUEST @ /slack========='
    response = {'username': 'merabot', 'icon_emoji': ':thumbsup:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form


    channel = request.form.get('channel_name') #this is the channel name where the message was sent from
    username = request.form.get('user_name') #this is the username of the person who sent the message
    text = request.form.get('text') #this is the text of the message that was sent
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message

    query = text
    q1 = query.split(':')
    answer_link = []
    title = []
    answer_count = []
    date_of_creation = []
    if username in [my_slack_username, 'zac.wentzell']:
        if text == "&lt;BOTS_RESPOND&gt;":
            print 'Bot is responding to favorite color question'
            response['text'] = 'Hello my name is merabot. I belong to csachdev. I live at 52.41.49.226'
            print 'Response text set correctly'
            print response['text']
            r = requests.post(slack_inbound_url, json=response)

        elif q1[0] == '&lt;I_NEED_HELP_WITH_CODING&gt;':
            #print ('chalta hai betta')
            splitdata=text.split(':')
            question=splitdata[1]
            payload = {'order': 'desc', 'sort': 'activity','q': question, 'answers': '5','accepted': 'True'
                ,'views': 500, 'site': 'stackoverflow'}
            inp = requests.get('https://api.stackexchange.com/2.2/search/advanced', params=payload).json()
            for i in range(5):
                print (inp['items'][i]['title'])
                print inp['items'][i]['link']
                local_answer_link = answer_link.append(str(inp['items'][i]['link']))
                local_answer_count = answer_count.append(str(inp['items'][i]['answer_count']))
                local_title = title.append(str(inp['items'][i]['title']))
                # https://docs.python.org/2/library/time.html
                # python reference paper

                local_datetime = date_of_creation.append(str(time.strftime("%a %d %b %Y %H:%M:%S GMT",
                                                                           time.gmtime(
                                                                               inp['items'][i]['creation_date']))))
                response['text'] = answer_link[i] + '\t' + 'Number of responses:' + '\t' + answer_count[
                    i] + '\t' + 'Title:' + '\t' + title[i] + '\t' + 'Date Created:' + '\t' + date_of_creation[i]
                r = requests.post(slack_inbound_url, json=response)

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
