import telebot
import bs4
from Task import Task
import parser
import markups as m

#main variables
TOKEN = '1050010216:AAFccV-uwzSDJUMKVdCC21REJeXF2uwmswM'
bot = telebot.TeleBot(TOKEN)
task = Task()

#handlers
@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Что вас интересует?', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
        task.isRunning = True

def askSource(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Вот что вы запрашивали')
    text = message.text.lower() 
    if text in task.sources[0]:
        msg = bot.send_message(chat_id, 'Результаты последних 10 матчей')
        bot.register_next_step_handler(msg, answerResults)
    elif text in task.sources[1]:
        msg = bot.send_message(chat_id, 'Ближайшие 15 матчей')
        bot.register_next_step_handler(msg, answerMatches)
    elif text in task.sources[2]:
        msg = bot.send_message(chat_id, 'Топ-5 команд')
        bot.register_next_step_handler(msg, answerTop)
    else:
        msg = bot.send_message(chat_id, 'Такого раздела нет. Введите раздел корректно.')
        bot.register_next_step_handler(msg, askSource)
        return

def answerTop(message):
    chat_id = message.chat.id
    text = message.text.lower()
    task.isRunning = False
    output = ''
    top = parser.top5teams()
    count = 0
    for i in top:
        if 'name' in i:
            output += (f"Команда {i['name']} занимает {i['rank']} место в рейтинге,имея {i['rank-points']} очков\n  Состав\n")
            team = top[count]
            players = sostav['team-players']
            for j in range(5):
                player = players[j]
                nick = player['player_name']
                output += ('   — '+nick+';\n')
            count+=1

    msg = bot.send_message(chat_id, output, reply_markup=m.start_markup)

def answerResults(message):
    chat_id = message.chat.id
    text = message.text.lower()
    task.isRunning = False
    output = ''
    res = parser.get_results()
    for i in res:
        if 'date' in i:
            output += (f" Матч между  {i['team1']} и {i['team2']} на турнире {i['event']} завершился со счётом {i['team1score']}-{i['team2score']}.\n")
    msg = bot.send_message(chat_id, output, reply_markup=m.start_markup)

def answerMatches(message):
    chat_id = message.chat.id
    text = message.text.lower()
    task.isRunning = False
    output = ''
    matches = parser.get_matches()
    for i in matches:
        if 'date' in i:
            output += (f"{i['date']} на турнире {i['event']} в {i['time']} встретятся  {i['team1']} и {i['team2']}.\n")
    msg = bot.send_message(chat_id, output, reply_markup=m.start_markup)

bot.polling(none_stop=True)