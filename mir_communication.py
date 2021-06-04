import requests


# !!!!!!!!!!!!!!!!!!!!! start the robot before running this program

# instead of using this python script, you can use the following terminal command:

# curl -X POST "http://192.168.12.20/api/v2.0.0/mission_queue" -H "accept: application/json" -H "Authorization: Basic RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA==" -H "Accept-Language: en_US" -H "Content-Type: application/json" -d "{\"mission_id\" : \"5e794de3-6dfe-11eb-b44a-0001299df20a\"}"

host = "http://192.168.12.20/api/v2.0.0/"
# computer vision pc 192.168.12.253
# mir 192.168.12.20
# router 192.168.12.1
# ur5 192.168.12.100

# Headers:

headers = {"Content-Type": "application/json",
           "Authorization": "Basic RGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA==",
           "Host" : "192.168.12.20",
           "Accept-Language" : "en_US"
            }

# Retrive mission list from the mir

recieve_mission = requests.get(host + "missions", headers = headers )

print(recieve_mission.text)

# Sending command to the mir

# {
#         "guid": "79579d2e-c52c-11eb-be53-0001299df20a",
#         "name": "coke",
#         "url": "/v2.0.0/missions/79579d2e-c52c-11eb-be53-0001299df20a"
#     },
#     {
#         "guid": "954fc36a-c52c-11eb-be53-0001299df20a",
#         "name": "lp",
#         "url": "/v2.0.0/missions/954fc36a-c52c-11eb-be53-0001299df20a"
#     },
#     {
#     "guid": "446d8109-ba3b-11eb-bf22-0001299df20a",
#     "name": "710_demo",
#     "url": "/v2.0.0/missions/446d8109-ba3b-11eb-bf22-0001299df20a"
#      },

# # run 710 demo
# data = "{\"mission_id\" : \"446d8109-ba3b-11eb-bf22-0001299df20a\" }"
#
# send_mission = requests.post(host + "mission_queue", headers = headers, data = data)
#
# print(send_mission)

# # run coke
# data = "{\"mission_id\" : \"79579d2e-c52c-11eb-be53-0001299df20a\" }"
#
# send_mission = requests.post(host + "mission_queue", headers = headers, data = data)
#
# print(send_mission)

# # run lp
# data = "{\"mission_id\" : \"954fc36a-c52c-11eb-be53-0001299df20a\" }"
#
# send_mission = requests.post(host + "mission_queue", headers = headers, data = data)
#
# print(send_mission)
