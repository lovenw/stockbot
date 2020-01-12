import json
from slacker import Slacker
from flask import Flask, request, make_response, jsonify
import requests
from bs4 import BeautifulSoup
import re

tokenf = 'xoxb-891410806117-888411335875-'
tokenb = '2wHNq3Mjh1IBF5IUiiUWwZ7c'

slack_token = tokenf+tokenb


slack = Slacker(slack_token)

app = Flask(__name__)

std = ''

# print(std)


slack = Slacker(slack_token)

'''

import os
from slack import RTMClient

@RTMClient.run_on(event="message")
def say_hello(**payload):
  data = payload['data']
  web_client = payload['web_client']

  if 'Hello' in data['text']:
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']

    web_client.chat_postMessage(
      channel=channel_id,
      text=f"Hi <@{user}>!",
      thread_ts=thread_ts
    )

rtm_client = RTMClient(token=slack_token)
rtm_client.start()

'''



def stock_price(std) :
    currentPrice_URL="https://finance.yahoo.com/quote/"+std
#    print(currentPrice_URL)

    req = requests.get(currentPrice_URL)
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')#, from_encoding='utf-8')
    text = soup.find('span',{'class':'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'})

    text = str(text)

    text=re.sub('<.+?>','',text, 0).strip()
    print(std+' : '+ text)

    return text


print('hello')



def get_answer():

    return "안녕하세요."


# 이벤트 핸들하는 함수

def event_handler(event_type, slack_event):

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        receivedText = slack_event["event"]["text"]
        answer = receivedText.replace("@","")+get_answer()
        slack.chat.post_message(channel, answer)
        return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )
    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})



@app.route("/slack", methods=["GET", "POST"])

def hears():

    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})




@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    # print(f'got name {name}')


    price = stock_price(name)

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"{name} price : {price}"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=8080)