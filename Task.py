class Task():
    isRunning = False
    sources = [
        ['results', 'результаты','резы', 'res'],
        ['today\'s matches', 'сегодняшние матчи', 'матчи', 'matches'],
        ['top-5 teams', 'топ-5 команд', 'топ5', 'top5']
    ]
    def __init__(self):
        returns