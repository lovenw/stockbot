from slacker import Slacker


# 슬랙 토큰으로 객체 생성

tokenf = 'xoxb-891410806117-888411335875-'
tokenb = '2wHNq3Mjh1IBF5IUiiUWwZ7c'

#token = tokenf+tokenb

slack = Slacker(tokenf+tokenb)

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

slack_token = tokenf+tokenb
rtm_client = RTMClient(token=slack_token)
rtm_client.start()


# 메시지 전송 (#채널명, 내용)

slack.chat.post_message('#random', 'Slacker 테스트')

#
