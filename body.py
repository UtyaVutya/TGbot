import telebot
import bs4
from Task import Task
import parser
import markups as m

#main variables
TOKEN = '<TOKEN>'
bot = telebot.TeleBot(TOKEN)
task = Task()

#handlers
@bot.message_handler(commands=['start', 'Назад'])
def start_handler(message):
    if not task.isRunning:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Что вас интересует?', reply_markup=m.source_markup)
        bot.register_next_step_handler(msg, askSource)
        task.isRunning = True

def askSource(message):
    chat_id = message.chat.id
    text = message.text.lower()
    output = '' 
    if text in task.sources[0]:
        msg = bot.send_message(chat_id, 'Результаты последних 10 матчей')
        output = answerResults()
        msg = bot.send_message(chat_id, output, reply_markup=m.back_markup)
    elif text in task.sources[1]:
        msg = bot.send_message(chat_id, 'Ближайшие 15 матчей')
        output = answerMatches()
        msg = bot.send_message(chat_id, output, reply_markup=m.back_markup)
    elif text in task.sources[2]:
        msg = bot.send_message(chat_id, 'Топ-5 команд')
        output = answerTop()
        msg = bot.send_message(chat_id, output, reply_markup=m.back_markup)
    else:
        msg = bot.send_message(chat_id, 'Такого раздела нет. Введите раздел корректно.')
        bot.register_next_step_handler(msg, askSource)
        return

def answerTop():
    task.isRunning = False
    output = ''
    top = parser.top5teams()
    count = 0
    for i in top:
        if 'name' in i:
            output += (f"Команда {i['name']} занимает {i['rank']} место в рейтинге, имея {i['rank-points']} очков\n  Состав:\n")
            team = top[count]
            players = team['team-players']
            for j in range(5):
                player = players[j]
                nick = player['player_name']
                output += ('   — '+nick+';\n')
            count+=1
    return output

def answerResults():
    task.isRunning = False
    output = ''
    res = parser.get_results()
    for i in res:
        if 'date' in i:
            output += (f"— Матч между {i['team1']} и {i['team2']} на турнире {i['event']} завершился со счётом {i['team1score']}-{i['team2score']}.\n")
    output = output.replace("b\'", "\'")    
    return output

def answerMatches():
    task.isRunning = False
    output = ''
    matches = parser.get_matches()
    for i in matches:
        if 'date' in i:
            output += (f"({i['date']}) на турнире {i['event']} в {i['time']} (UTC+03:00) встретятся {i['team1']} и {i['team2']}.\nСсылка на матч: {i['url']}\n")
    output = output.replace("b\'", "\'")
    return output

bot.polling(none_stop=True)