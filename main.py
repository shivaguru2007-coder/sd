import random
import time
import json
import telebot
import requests 

TOKEN = "Rupees "
AIRDROP = "Nothing"
BOT_TOKEN = "5049149165:AAEA95mYTUzazaewU4sp9ouk5GrIMUkjTxk"
PAYMENT_CHANNEL = "@sglooter"
OWNER_ID = 2044257366
CHANNELS = ["@sglooter"]
Mini_Withdraw = 1
Paytmkeys = "key"
mid = "key"
paytmtoken = "key"

Maxwith = telebot.types.ReplyKeyboardMarkup(True)
Maxwith.row('🚫 Cancel') 

botdata = json.load(open('panel.json', 'r'))
admins = botdata['admins'] 

msg_start = botdata['msgstart'] 

bot = telebot.TeleBot(BOT_TOKEN) 

bonus = {}
withdraw = {} 

setbonus_mess = "<b>🟣 Send new bonus amount to set Bonus in bot</b>"
ban_mess = "<b>⚫️ Send user Telegram ID to ban the user</b>"
unban_mess = "<b>🔵 Send user Telegram ID to unban the user</b>"
add_mess = "<b>🟢 Send user Telegram ID to add balance</b>"
cut_mess = "<b>🟡 Send user Telegram ID to cut balance</b>"
setref_mess = "<b>🟠 Send new refer bonus amount to set refer bonus in bot</b>"
setwith_mess = "<b>🔘 Send new minimum withdraw amount to set Minimum withdraw in bot</b>"
addadmin_mess = "<b>🔴 Send new Admin Telegram id to make Admin in bot</b>"


def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True


def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('💰 Balance')
    keyboard.row('🙌🏻 Invite', '🎁 Bonus ', '🗂 Wallet')
    keyboard.row('💳 Withdraw', '📊 Statistics')
    bot.send_message(id, "<b>🏡 Menu </b>", parse_mode="html",
                     reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('paytmusers.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['user']:
                data['user'][user] = 0
                data['contact'][user] = False
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.5)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='☑️ Joined ', callback_data='check'))
            bot.send_message(user, msg_start,
                             parse_mode="html", reply_markup=markup)
        else:
            data = json.load(open('paytmusers.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['total'] = data['total'] + 1
                data['referred'][user] = 0
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['user']:
                data['user'][user] = 0
                data['contact'][user] = True
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.5)
            ap = json.load(open('panel.json', 'r'))
            msg_tart = str(ap['msgstart'])
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
            bot.send_message(user, msg_tart,
                             parse_mode="html", reply_markup=markups)
    except:
        bot.send_message(message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


@bot.message_handler(content_types=['contact'])
def contact(contact):
    con = contact.contact.phone_number
    number = con[0]+con[1]+con[2]
    numberphone = con[0]+con[1]
    user_id = contact.from_user.id
    user = str(user_id)
    print(contact)
    if contact.forward_from or contact.forward_from_chat:
      bot.send_message(user, "Don't Forward The Number", parse_mode="html")
      return

    if contact.contact.vcard:
      bot.send_message(user, "Don't Send From Contact!", parse_mode="html")
      return

    if contact.contact.user_id:
      pass
    else:
      bot.send_message(user, "Don't Send From Contact!", parse_mode="html")
      return

    if user_id == contact.contact.user_id:
      pass
    else:
      bot.send_message(user, "Don't Send Number of others", parse_mode="html")
      return

    if contact.from_user.first_name == contact.contact.first_name:
      pass
    else:
      bot.send_message(user, "Don't Send Number of others", parse_mode="html")
      return
    if number == '+91' or numberphone == "91":
        data = json.load(open('paytmusers.json', 'r'))
        user_id = contact.from_user.id
        user = str(user_id)
        bot.delete_message(contact.from_user.id, contact.message_id)
        data['contact'][user] = True
        if user not in data['refer']:
            data['refer'][user] = True

            if user not in data['referby']:
                data['referby'][user] = user
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
            if int(data['referby'][user]) != user_id:
                ref_id = int(data['referby'][user])
                ref = str(ref_id)
                if ref not in data['balance']:
                    data['balance'][ref] = 0
                if ref not in data['referred']:
                    data['referred'][ref] = 0
                time.sleep(0.5)
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                botdata = json.load(open('panel.json', 'r'))
                Per_Refer = float(round( random.uniform(0.5 , 0.75),2))
                data['balance'][ref] += float(Per_Refer)
                data['referred'][ref] += 1
                markups = telebot.types.InlineKeyboardMarkup()
                markups.add(telebot.types.InlineKeyboardButton(text='✅ Check', callback_data='checkd'))
                bot.send_message(user, "<b>💹 To Check Who Invited You , Click On ✅ Check</b>",
                                parse_mode="html", reply_markup=markups)
                bot.send_message(
                    ref_id, '🚧 <b>New User On Your Invite Link :  <a href="tg://user?id='+str(user)+'">'+str(user)+'</a>\n💰 +'+str(Per_Refer)+' '+str(TOKEN)+' Added To Your Balance</b>', parse_mode="html")
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                return menu(contact.from_user.id)

            else:
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                return menu(contact.from_user.id)

        else:
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            return menu(contact.from_user.id)

    else:
        bot.send_message(
            contact.from_user.id, "<b>Sorry Only Indian users are allowed for bot</b>", parse_mode="html")


@bot.message_handler(commands=['panel'])
def panel(message):
    user = str(message.chat.id)
    data = json.load(open('panel.json', 'r'))
    if message.chat.id == OWNER_ID:
        keyboard = [[telebot.types.InlineKeyboardButton('⭕️ Ban user', callback_data='banuser'),
                     telebot.types.InlineKeyboardButton('❕Unban user', callback_data='unbanuser')],
                    [telebot.types.InlineKeyboardButton('➗ Add balance', callback_data='addbalance'),
                     telebot.types.InlineKeyboardButton('🚫 Cut balance', callback_data='cutbalance')],
                    [telebot.types.InlineKeyboardButton(
                        '💲 Add admins', callback_data='addadmins')],
                    [telebot.types.InlineKeyboardButton(
                        '🟡 Set Refer Bonus', callback_data='setrefer')],
                    [telebot.types.InlineKeyboardButton('🟢 Set bonus amount', callback_data='setbonus')]]
        markup8 = telebot.types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, "<b>🔆 Welcome to admin panel</b>",
                         parse_mode="html", reply_markup=markup8)
    elif user not in data['admins']:
        bot.send_message(
            message.chat.id, "<b>You need to become a admin first to open admin panel</b>", parse_mode="html")
    else:
        keyboard = [[telebot.types.InlineKeyboardButton('⭕️ Ban user', callback_data='banuser'),
                     telebot.types.InlineKeyboardButton('❕Unban user', callback_data='unbanuser')],
                    [telebot.types.InlineKeyboardButton('➗ Add balance', callback_data='addbalance'),
                     telebot.types.InlineKeyboardButton('🚫 Cut balance', callback_data='cutbalance')],
                    [telebot.types.InlineKeyboardButton(
                        '💲 Add admins', callback_data='addadmins')],
                    [telebot.types.InlineKeyboardButton(
                        '🟡 Set Refer Bonus', callback_data='setrefer')],
                    [telebot.types.InlineKeyboardButton('🟢 Set bonus amount', callback_data='setbonus')]]
        markup8 = telebot.types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, "<b>🔆 Welcome to admin panel</b>",
                         parse_mode="html", reply_markup=markup8)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   try:
        ch = check(call.message.chat.id)
        if call.data == 'checkd':
          bot.send_message(
              call.message.chat.id, "♻️ <b>Share Your Contact For Verification</b> \n\n<b><u>⚠️ We Never Share Your Contact To Anyone</u></b>", parse_mode="html")
        if call.data == 'check':
            if ch == True:
                data = json.load(open('paytmusers.json', 'r'))
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='✅ You joined.')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                keyboard = telebot.types.ReplyKeyboardMarkup(True)
                keyboard.row(telebot.types.KeyboardButton(
                    "Send Your number", request_contact=True))
                bot.send_message(
                    call.message.chat.id, "♻️ <b>Share Your Contact For Verification</b> \n\n<b><u>⚠️ We Never Share Your Contact To Anyone</u></b>", reply_markup=keyboard, parse_mode="html")
            else:
                user_id = call.message.chat.id
                user = str(user_id)
                bot.answer_callback_query(
                    callback_query_id=call.id, text='❌ You not Joined')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(
                    text='☑️ Joined', callback_data='check'))
                bot.send_message(user, msg_start,
                                parse_mode="html", reply_markup=markup)
                        
        if call.data.split("_")[0] == 'confirmwith':
            message = call.message
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            amount = float(call.data.split("_")[1])
            wallet = str(data['wallet'][user])
            response = requests.get("https://job2all.xyz/api/index.php?mid=&mkey=&guid=&mob="+str(wallet)+"&amount="+str(amount)+"")
    #            asd = response['status']
    #            if asd == "fail":
            data['balance'][user] -= float(amount)
            data['totalwith'] += float(amount)
            json.dump(data, open('paytmusers.json', 'w'))
            time.sleep(0.8)
    #            cur_time2 = int((time.time()))
    #            withdraw[user_id] = cur_time2
            bot.edit_message_text(chat_id=user, message_id=call.message.message_id, text="✅ Withdrawl initiated successfully!")
            bot.send_message(PAYMENT_CHANNEL, "❣️ <b>New withdraw successfully!!\n\n🍕 Amount</b> : "+str(amount)+" <b>Paytm Cash \n🥪 User</b> : "+str(message.chat.username)+"\n\n🍔 <b>Bot</b> : @"+bot.get_me().username, parse_mode="html")
            return menu(message.chat.id)
    #            else:
    #                bot.send_message(
    #                    user_id, "WE HAVE PAID YOUR WITHDRAW PLEASE WAIT 1-2 MINUTES.")
    #                return menu(message.chat.id)
        if call.data == 'setwallet':
            message = call.message
            user_id = message.chat.id
            user = str(user_id)
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "<b>Enter A Valid Paytm Number</b>",
                                    parse_mode="html", reply_markup=keyboard)
            bot.register_next_step_handler(message, trx_address)
        if call.data == "banuser":
            message = call.message
            bot.send_message(call.message.chat.id, ban_mess, parse_mode="html")
            bot.register_next_step_handler(message, ban)
        if call.data == "unbanuser":
            message = call.message
            bot.send_message(call.message.chat.id, unban_mess,
                            parse_mode="html")
            bot.register_next_step_handler(message, unban)
        if call.data == "addbalance":
            message = call.message
            bot.send_message(call.message.chat.id, add_mess, parse_mode="html")
            bot.register_next_step_handler(message, add_balance)
        if call.data == "cutbalance":
            message = call.message
            bot.send_message(call.message.chat.id, cut_mess, parse_mode="html")
            bot.register_next_step_handler(message, cut_balance)
        if call.data == "setrefer":
            message = call.message
            bot.send_message(call.message.chat.id, setref_mess,
                            parse_mode="html")
            bot.register_next_step_handler(message, set_refer)
        if call.data == "setbonus":
            message = call.message
            bot.send_message(call.message.chat.id, setbonus_mess,
                            parse_mode="html")
            bot.register_next_step_handler(message, set_bonus)
        if call.data == "addadmins":
            message = call.message
            bot.send_message(call.message.chat.id, addadmin_mess,
                            parse_mode="html")
            bot.register_next_step_handler(message, add_admins)
   except:
        bot.send_message(call.message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return

        
def ban(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "User successfully banned")
        data['banned'].append(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def unban(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "User successfully Unbanned")
        data['banned'].remove(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "This user is may not banned if you not sure you can contact our dev @SGking27_xd")
        return


def add_balance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data1 = json.load(open('paytmusers.json', 'r'))
        if message.text not in data1['user']:
            bot.send_message(message.chat.id, "This user is not found")
        else:
            data = json.load(open('panel.json', 'r'))
            data['addto'] = message.text
            json.dump(data, open('panel.json', 'w'), indent=4)
            time.sleep(0.8)
            bot.send_message(message.chat.id, "Send amount to add balance")
            bot.register_next_step_handler(message, addbalance)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return 

def cut_balance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data1 = json.load(open('paytmusers.json', 'r'))
        if message.text not in data1['user']:
            bot.send_message(message.chat.id, "This user is not found")
        else:
            data = json.load(open('panel.json', 'r'))
            data['addto'] = message.text
            json.dump(data, open('panel.json', 'w'), indent=4)
            time.sleep(0.8)
            bot.send_message(message.chat.id, "Send amount to cut balance")
            bot.register_next_step_handler(message, cutbalance)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return
def addbalance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data2 = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "Added successfully")
        data = json.load(open('paytmusers.json', 'r'))
        data['balance'][data2['addto']] += float(message.text)
        json.dump(data, open('paytmusers.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def cutbalance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data2 = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "Added successfully")
        data = json.load(open('paytmusers.json', 'r'))
        data['balance'][data2['addto']] -= float(message.text)
        json.dump(data, open('paytmusers.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def set_bonus(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "New bonus amount is set successfully")
        data['bonus'] = float(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def set_refer(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "New refer bonus amount is set successfully")
        data['refbonus'] = float(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def add_admins(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "Admin successfully added You can remove it by editing panel.json file in your server")
        data['admins'].append(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return
@bot.message_handler(content_types=['text'])
def send_text(message):
   try:
    bdata = json.load(open('paytmusers.json','r'))
    if str(message.chat.id) not in bdata['contact']:
      bdata['contact'][str(message.chat.id)] = False
      json.dump(bdata, open('paytmusers.json', 'w'), indent=4)
    if bdata['contact'][str(message.chat.id)] == True:
      ch = check(message.chat.id)
      if ch is True:
        if message.chat.id == OWNER_ID:
            if message.text == '/addu':
                bot.send_message(OWNER_ID, "Send User ID to add balance")
                bot.register_next_step_handler(message, add_balance)
        if message.text == '💰 Balance':
            data = json.load(open('paytmusers.json', 'r'))
            accmsg = '<b>👮 User : {}\n\n🗂 Wallet : </b><code>{}</code><b>\n\n💸 Balance : </b><code>{}</code><b> {}</b>'
            user_id = message.chat.id
            user = str(user_id) 

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none" 

            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name,
                                wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="html") 

        if message.text == '🙌🏻 Invite':
            data = json.load(open('paytmusers.json', 'r'))
            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)
            botdata = json.load(open('panel.json', 'r'))
            Per_Refer = "Random refer bonus 0.5 to 0.75"
            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            ref_count = data['referred'][user]
            ref_link = 'https://t.me/'+str(bot_name)+'?start='+str(message.chat.id)
            ref_msg = "<b>🙌🏻 Total Invites : "+str(ref_count)+" Users\n\n👥 Refferrals System\n\n🙇 Per Refer :-  "+str(Per_Refer)+" "+str(TOKEN)+"\n\n🔗 Referral Link ⬇️\n"+str(ref_link)+"</b>"
            bot.send_message(message.chat.id, ref_msg, parse_mode="html")
        if message.text == "🗂 Wallet":
            user_id = message.chat.id
            user = str(user_id) 

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "<b>✏️ Now Send Your Paytm number It will use For Future Withdrawals</b>",
                                    parse_mode="html", reply_markup=keyboard)
            bot.register_next_step_handler(message, trx_address)
        if message.text == "🎁 Bonus":
            botdata = json.load(open('panel.json', 'r'))
            Daily_bonus =  round(random.uniform(0.1, 0.5),2)
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('paytmusers.json', 'r'))
            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 24*60*60):
                data['balance'][(user)] += float(Daily_bonus)
                bot.send_message(
                    user_id, "<b>Congrats you just received "+str(Daily_bonus)+" Paytm CASH</b>", parse_mode="html")
                bonus[user_id] = cur_time
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                time.sleep(0.8)
            else:
                bot.send_message(
                    message.chat.id, "<b>❌You can only take bonus once every 24 hours!</b>", parse_mode="html")
            return
        if message.text == "st": 
            print(data)  
        if message.text == "📊 Statistics":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            msg = "<b>📊 Total members : {} Users\nThis Bot is Made By @SGking27_xd Dm me To buy\n💎 Total successful Withdraw : {} {}</b>"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="html")
            return
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text == "💳 Withdraw":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            cur_time = int((time.time()))  
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            bal = data['balance'][user]
            wall = data['wallet'][user]
            if wall == "none":
                markup = telebot.types.InlineKeyboardMarkup()
                markup.add(telebot.types.InlineKeyboardButton(
                    text='✅ Set wallet', callback_data='setwallet'))
                bot.send_message(user_id, "<b>⚠️ Your Wallet is</b> <code>Not set</code>\n‼️ <b>Please set your wallet first For withdraw</b>",
                                    parse_mode="html", reply_markup=markup)
                return

            if bal >= Mini_Withdraw:
                bot.send_message(user_id, "<b>Enter amount to withdraw Your paytm cash\n\nCurrent wallet: "+wall+"</b>",
                                    parse_mode="html", reply_markup=Maxwith)
                bot.register_next_step_handler(message, amo_with)
            if bal < 1:
                bot.send_message(user_id, "<b>your Balance is Low to Withdraw Mnimum Withdraw 1 rs</b>",parse_mode="html")
                return menu(message.chatid)    
 
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
   except:
      bot.send_message(
          message.chat.id, "An error has been occupied to our server pls wait sometime and try again \n\n Possible Reasons: \n\n 1. You have too low balance Withdraw \n Minimum Withdraw Is 1 Rs \n\n 2. If U have enough balanceContact Dev : @sgking27_xd")
      return

def trx_address(message):
   try:
      ch = check(message.chat.id)
      if ch is True:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if len(message.text) == 10:
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            data['wallet'][user] = message.text
            bot.send_message(message.chat.id, "<b>💹 Your paytm wallet set to " +
                             data['wallet'][user]+"</b>", parse_mode="html")
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            return menu(message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "<b>⚠️ It's Not a Valid Paytm Number!</b>", parse_mode="html")
            return menu(message.chat.id)
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
   except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def amo_with(message):
   try:
      ch = check(message.chat.id)
      if ch is True:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        if message.chat.id not in data['banned']:
            user_id = message.chat.id
            amo = message.text
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            cmsg = str(message.text.replace('.',''))
            if cmsg.isdigit() == True:
                pass
            else:
                bot.send_message(user_id, "⚠️ Invalid Amount")
                bot.register_next_step_handler(message, amo_with)
                return
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            bal = data['balance'][user]
            wall = data['wallet'][user]
            msg = message.text
            if float(message.text) > float(bal):
                bot.send_message(
                    user_id, "<i>❌ You Can't withdraw More than Your Balance</i>", parse_mode="html")
                return menu(message.chat.id)
            bot.send_message(
                message.chat.id, "Initiating Transaction\n<b>Please wait.</b>", parse_mode="html")
            amount = float(amo)
            mess = "<i>For, A success withdrawal You need to confirm the Withdrawal</i>\n\n⚠️ <b>You are Withdrawing</b> "+str(format(float(amo), '.8f'))+" <b>Paytm Cash</b> to the \n<code>"+str(wall)+"</code> <b>Paytm wallet\n\n✅ Please Check the Withdraw details Before <u>Confirm the withdraw</u></b>"
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(text='✅ Confirm Withdraw', callback_data='confirmwith_'+str(amo)))
            bot.send_message(user,mess,parse_mode='html',reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Sorry you are banned")
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
   except:
        bot.send_message(message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


bot.polling(none_stop=True)
