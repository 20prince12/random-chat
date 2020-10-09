from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
from config import TELEGRAM_INIT_WEBHOOK_URL

app = Flask(__name__)
TelegramBot.init_webhook(TELEGRAM_INIT_WEBHOOK_URL)

#current searching people chat id's list
queue = []
#pairs of people chat id's who are chatting
pairs = {}

@app.route('/')
def home():
    return "<h1>hello2</h1>"

#webhook recieves forwarded json data from telegram server when someone sends a message to bot.
@app.route('/webhook', methods=['POST'])
def index():
    req = request.get_json() #storing the data recieved by telegram server
    bot = TelegramBot() #creating object of telegramBot class
    bot.parse_webhook_data(req) #parsing the json data recieved by telegram server
    success = bot.action() #basic reply actions

    #if message recieved from user who is in chat with stranger
    if pairs.get(bot.chat_id):

        #if chat mesasge is leave
        if bot.incoming_message_text=="/leave":

            #alerting users with chat ending message.
            bot.send_msg(pairs.get(bot.chat_id),"Stranger left the chat.")
            bot.send_msg(bot.chat_id, "You left the chat.")

            #removing both users from the paired chat_id's
            x=pairs.get(bot.chat_id)
            del pairs[x]
            del pairs[bot.chat_id]
        else:

            #if it was just normal message then forward to the stranger who is in chat with the user
            bot.forward_message(pairs.get(bot.chat_id))

    #else
    else:

        #if user requests to search
        if bot.incoming_message_text=='/search' and bot.chat_id not in queue:
            bot.send_msg(bot.chat_id, "Searching....")
            #add user to searching queue
            queue.append(bot.chat_id)
        print("queue=", queue)

        #if queue has 2 users then match their pair.
        if(len(queue)==2):
            pairs[queue[0]]=queue[1]
            pairs[queue[1]]=queue[0]
            bot.send_msg(queue[0],"Search found,you can now start chatting with stranger.\nSharing of files and images is not allowed.\nThis is just chat.\nuse /leave to leave chat.")
            bot.send_msg(queue[1],"Search found,you can now start chatting with stranger.\nSharing of files and images is not allowed.\nThis is just chat.\nuse /leave to leave chat.")
            queue.clear()
        print(pairs)
    return jsonify(success=success) # TODO: Success should reflect the success of the reply

if __name__ == '__main__':
    app.run(host ='0.0.0.0',port=80)


# https://telegram.me

# check bot initialization: https://api.telegram.org/bot<secret key>/getme
# check webhook url: https://api.telegram.org/secret key/getWebhookInfo
