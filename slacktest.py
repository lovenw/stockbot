from slacker import Slacker



# 슬랙 토큰으로 객체 생성

token = 'xoxb-891410806117-888411335875-48NSDtf0Flon6gIwLcQ1Lkos'

slack = Slacker(token)



# 메시지 전송 (#채널명, 내용)

slack.chat.post_message('#random', 'Slacker 테스트')


