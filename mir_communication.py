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

data = "{\"mission_id\" : \"5e794de3-6dfe-11eb-b44a-0001299df20a\" }"

send_mission = requests.post(host + "mission_queue", headers = headers, data = data)

print(send_mission)