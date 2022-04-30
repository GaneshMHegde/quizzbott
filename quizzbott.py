import html
import  requests
import json

BOTAPI_UPDATE = "https://api.telegram.org/bot1975970237:AAGNghNOLjfSbRlZdOZzo2UjEHY0xpaKC70/getUpdates"
BOTAPI_POLL = "https://api.telegram.org/bot1975970237:AAGNghNOLjfSbRlZdOZzo2UjEHY0xpaKC70/sendPoll"
BOTAPI_MESSAGE = "https://api.telegram.org/bot1975970237:AAGNghNOLjfSbRlZdOZzo2UjEHY0xpaKC70/sendMessage"
QAPI = "https://opentdb.com/api.php?amount=1&type=boolean"


while True:
    responce = requests.get(BOTAPI_UPDATE)
    question_responce = requests.get(QAPI)
    question_responce.raise_for_status()
    responce.raise_for_status()
    procede=None
    try:
        from_name = responce.json()["result"][-1]["message"]['from']["first_name"]
        from_id = responce.json()["result"][-1]["message"]['from']['id']
        message_id = responce.json()["result"][-1]["message"]["message_id"]
        try:
            with open('.\messageid.txt','r') as file:
                p_message_id=int(file.readline())
                if message_id > p_message_id:
                    procede=True
                    with open('.\messageid.txt', 'w') as file:
                        file.write(f'{message_id}')

                else:
                    procede=False

        except FileNotFoundError:
            with open('.\messageid.txt','w') as file:
                file.write(f'{message_id}')


        text = responce.json()["result"][-1]["message"]['text']
        question = question_responce.json()["results"][0]["question"]
        answer = question_responce.json()["results"][0]["correct_answer"]
    except KeyError:
        pass
    else:
        if procede==True:
            option_list = ["True","False"]
            options = json.dumps(option_list)
            if answer == "True":
                currect_ans_id = 0

            else:
                currect_ans_id = 1


            if text == "/start":
                message = f'''Hii {from_name}....
                welcome to @Quiz_Mebot
                To start taking Quiz press /quiz
                '''
                message_params={
                    'chat_id':from_id,
                    'text':message
                }
                requests.get(BOTAPI_MESSAGE,params=message_params)
            elif text == "/quiz":
                message = html.unescape(question)
                pole_params={
                    'chat_id':from_id,
                    'question':message,
                    'options':options,
                    'type':'quiz',
                    'correct_option_id':currect_ans_id
                }
                result_of_pole=requests.get(BOTAPI_POLL,params=pole_params)
                result_of_pole.raise_for_status()

        else:
            pass
