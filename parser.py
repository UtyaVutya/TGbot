import re
import requests
import datetime
from bs4 import BeautifulSoup
from python_utils import converters
 
 
def get_parsed_page(url):
    headers = {
        "referer": "https://www.hltv.org/stats",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
 
    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")
 
 
def top5teams():
    page = get_parsed_page("http://www.hltv.org/ranking/teams/")
    teams = page.find("div", {"class": "ranking"})
    teams5 = []
    for team in teams.find_all("div", {"class": "ranked-team standard-box"}):
        newteam = {'name': team.find('div', {"class": "ranking-header"}).select('.name')[0].text.strip(),
                   'rank': converters.to_int(team.select('.position')[0].text.strip(), regexp=True),
                   'rank-points': converters.to_int(team.find('span', {'class': 'points'}).text, regexp=True),
                   'team-players': []
                   }
        for player_div in team.find_all("td", {"class": "player-holder"}):
            player = {}
            player['player_name'] = player_div.find('img', {'class': 'playerPicture'})['title']
            newteam['team-players'].append(player)
        if len(teams5)<5:
         teams5.append(newteam)
    return teams5
 
 
def get_matches():
    matches = get_parsed_page("http://www.hltv.org/matches/")
    matches_list = []
    upcomingmatches = matches.find("div", {"class": "upcoming-matches"})
 
    matchdays = upcomingmatches.find_all("div", {"class": "match-day"})
 
    for match in matchdays:
        matchDetails = match.find_all("table", {"class": "table"})
        count = 0
        for getMatch in matchDetails:
            matchObj = {}
 
            matchObj['date'] = match.find("span", {"class": "standard-headline"}).text.encode('utf8')
            matchObj['time'] = getMatch.find("td", {"class": "time"}).text.lstrip().rstrip()
            if int(matchObj['time'][:2])+2 < 10:
                matchObj['time'] = ('0' + str(int(matchObj['time'][:2])+2) + matchObj['time'][2:]).encode('utf-8')
            else:
                matchObj['time'] = (str(int(matchObj['time'][:2])+2) + matchObj['time'][2:]).encode('utf-8')
 
            if (getMatch.find("td", {"class": "placeholder-text-cell"})):
                matchObj['event'] = getMatch.find("td", {"class": "placeholder-text-cell"}).text.encode('utf8')
            elif (getMatch.find("td", {"class": "event"})):
                matchObj['event'] = getMatch.find("td", {"class": "event"}).text.encode('utf8')
            else:
                matchObj['event'] = None
 
            if (getMatch.find_all("td", {"class": "team-cell"})):
                matchObj['team1'] = getMatch.find_all("td", {"class": "team-cell"})[0].text.encode(
                    'utf8').lstrip().rstrip()
                matchObj['team2'] = getMatch.find_all("td", {"class": "team-cell"})[1].text.encode(
                    'utf8').lstrip().rstrip()
            else:
                matchObj['team1'] = 'Ещё не определённая'
                matchObj['team2'] = 'Ещё не определённая'

            url = match.find_all("a", {"class": "a-reset"})[count].get("href")
            matchObj['url'] = 'http://www.hltv.org' + url
            count += 1
            
            if len(matches_list) < 15:
                matches_list.append(matchObj)
 
    return matches_list
 
 
def get_results():
    results = get_parsed_page("http://www.hltv.org/results/")
 
    results_list = []
 
    pastresults = results.find_all("div", {"class": "results-holder"})
 
    for result in pastresults:
        resultDiv = result.find_all("div", {"class": "result-con"})
 
        for res in resultDiv:
            getRes = res.find("div", {"class": "result"}).find("table")
 
            resultObj = {}
 
            if (res.parent.find("span", {"class": "standard-headline"})):
                resultObj['date'] = res.parent.find("span", {"class": "standard-headline"}).text.encode('utf8')
            else:
                dt = datetime.date.today()
                resultObj['date'] = str(dt.day) + '/' + str(dt.month) + '/' + str(dt.year)
 
            if (res.find("td", {"class": "placeholder-text-cell"})):
                resultObj['event'] = res.find("td", {"class": "placeholder-text-cell"}).text.encode('utf8')
            elif (res.find("td", {"class": "event"})):
                resultObj['event'] = res.find("td", {"class": "event"}).text.encode('utf8')
            else:
                resultObj['event'] = None
 
            if (res.find_all("td", {"class": "team-cell"})):
                resultObj['team1'] = res.find_all("td", {"class": "team-cell"})[0].text.encode('utf8').lstrip().rstrip()
                resultObj['team1score'] = converters.to_int(
                    res.find("td", {"class": "result-score"}).find_all("span")[0].text.encode('utf8').lstrip().rstrip())
                resultObj['team2'] = res.find_all("td", {"class": "team-cell"})[1].text.encode('utf8').lstrip().rstrip()
                resultObj['team2score'] = converters.to_int(
                    res.find("td", {"class": "result-score"}).find_all("span")[1].text.encode('utf8').lstrip().rstrip())
            else:
                resultObj['team1'] = None
                resultObj['team2'] = None
 
            if len(results_list)<10:
             results_list.append(resultObj)
 
    return results_list
