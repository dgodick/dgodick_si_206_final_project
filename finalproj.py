import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import plotly.plotly as py
from plotly import tools
import plotly.graph_objs as go
import unittest

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Articles')
cur.execute('DROP TABLE IF EXISTS Sections')
cur.execute('Create table if not exists Articles(Id integer primary key, Author text, Date text, Headline text, Link text, SectionId integer)')
cur.execute('Create table if not exists Sections(Id integer primary key, SectionName text, SectionLink text, Description text, PopularityRank integer, HasPhotos boolean)')
cur.execute('INSERT INTO Sections VALUES(?, ?, ?, ?, ?, ?)', (None, 'Opinions', 'https://www.washingtonpost.com/opinions', 'Opinions Page of Washington Post', 1, True))
cur.execute('INSERT INTO Sections VALUES(?, ?, ?, ?, ?, ?)', (None, 'Politics', 'https://www.washingtonpost.com/politics/?nid=top_nav_politics', 'Politics Page of Washington Post', 2, True))
cur.execute('INSERT INTO Sections VALUES(?, ?, ?, ?, ?, ?)', (None, 'World', 'https://www.washingtonpost.com/world/', 'World Page of Washington Post', 3, True))
cur.execute('INSERT INTO Sections VALUES(?, ?, ?, ?, ?, ?)', (None, 'Home', 'https://www.washingtonpost.com', 'Home Page of Washington Post', 4, True))
conn.commit()

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def make_request_using_cache(url):
    unique_ident = url
    if unique_ident in CACHE_DICTION:
        #print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        #print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

class Section():
    def __init__(self, tuple):
        self.id = tuple[2]
        self.sectionname = tuple[0]
        self.sectionlink = tuple[1]

    def __str__(self):
        return '{} {} {}'.format(self.id, self.sectionname, self.sectionlink)

def get_sections():
    statement = 'SELECT SectionName, SectionLink, Id FROM Sections'
    cur.execute(statement)
    sections_lst = [Section(tup) for tup in cur.fetchall()]
    return sections_lst

def get_articles(sections_lst):
    all_articles = []
    for section_inst in sections_lst:
        if section_inst.sectionname == 'Home':
            html = make_request_using_cache(section_inst.sectionlink)
            soup = BeautifulSoup(html, 'html.parser')
            headlines = soup.find_all("a", {"data-pb-field" : "web_headline"})
            for x in headlines:
                article_link = x["href"]

                html = make_request_using_cache(article_link)
                soup_article = BeautifulSoup(html, 'html.parser')
                try:
                    article_author = soup_article.find("span", {'itemprop' : "name"}).text
                except:
                    continue
                headline = soup_article.find('h1', {'itemprop' : 'headline'}).text
                article_date = soup_article.find("span", {'itemprop' : "datePublished"})["content"]
                statement = 'INSERT INTO Articles VALUES(?, ?, ?, ?, ?, ?)'
                cur.execute(statement, (None, article_author, article_date, headline, article_link, section_inst.id))
                all_articles.append((None, article_author, article_date, headline, article_link, section_inst.id))
        else:
            html = make_request_using_cache(section_inst.sectionlink)
            soup = BeautifulSoup(html, 'html.parser')

            headlines = soup.find_all("a", {"data-pb-local-content-field" : "web_headline"})
            for x in headlines:
                article_link = x["href"]
                if article_link == '':
                    continue
                html = make_request_using_cache(article_link)
                soup_article = BeautifulSoup(html, 'html.parser')
                try:
                    article_author = soup_article.find("span", {'itemprop' : "name"}).text
                except:
                    continue
                headline = soup_article.find('h1', {'itemprop' : 'headline'}).text
                article_date = soup_article.find("span", {'itemprop' : "datePublished"})["content"]
                statement = 'INSERT INTO Articles VALUES(?, ?, ?, ?, ?, ?)'
                cur.execute(statement, (None, article_author, article_date, headline, article_link, section_inst.id))
                all_articles.append((None, article_author, article_date, headline, article_link, section_inst.id))
    conn.commit()
    return all_articles


def get_opinions():
    cur.execute("SELECT Headline, Link FROM Articles WHERE SectionId = 1")
    return cur.fetchall()

def get_politics():
    cur.execute("SELECT Headline, Link FROM Articles WHERE SectionId = 2")
    return cur.fetchall()

def get_world():
    cur.execute("SELECT Headline, Link FROM Articles WHERE SectionId = 3")
    return cur.fetchall()

def get_home():
    cur.execute("SELECT Headline, Link FROM Articles WHERE SectionId = 4")
    return cur.fetchall()

def get_most_pop_authors():
    cur.execute("SELECT Author FROM Articles")
    x = cur.fetchall()
    new_dict = {}
    for key in x:
        if key[0] not in new_dict:
            new_dict[key[0]] = 1
        else:
            new_dict[key[0]] += 1
    key_lst = list(new_dict.keys())
    popular = key_lst[0]
    for key in key_lst:
        if new_dict[key] > new_dict[popular]:
            popular = key
    return key

def countSectionArticles():
    cur.execute("SELECT Sections.SectionName, COUNT(*) FROM Sections JOIN Articles on Sections.Id = Articles.SectionId GROUP BY SectionName")
    results = cur.fetchall()

    labels = [tupl[0] for tupl in results]
    values = [tupl[1] for tupl in results]

    trace = go.Pie(labels=labels, values=values)

    layout = go.Layout(title='Article Distribution by Section')
    fig = go.Figure(data=[trace], layout=layout)
    py.plot(fig, filename='articles_by_section')

    return results


def plotHeadlineLengths():
    cur.execute("SELECT Sections.SectionName, Articles.Headline FROM Sections JOIN Articles on Sections.Id = Articles.SectionId")
    results = cur.fetchall()

    data = []
    count = {}
    for section, headline in results:
        if section in count:
            count[section].append(len(headline.split()))
        else:
            count[section] = [len(headline.split())]
    fig = tools.make_subplots(rows=len(count), cols=1)
    row = 1
    for key in count:
        fig.append_trace(go.Histogram(x=count[key], name=key), row, 1)
        row+=1
    fig['layout'].update(height=600, width=600, title='Words in Headline')
    #, xaxis=dict(title='Number of Words in Headline'), yaxis=dict(title='Number of Articles')
    py.plot(fig, filename='simple-subplot')

    return count

def uniqueAuthorsBySection():
    cur.execute("SELECT Sections.SectionName, Articles.Author FROM Sections JOIN Articles on Sections.Id = Articles.SectionId")
    results = cur.fetchall()

    sections = {}
    for section, author in results:
        if section in sections:
            sections[section].append(author)
        else:
            sections[section] = [author]
    for section in sections:
        sections[section] = len(set(sections[section]))

    data = [go.Bar(
            x=list(sections.keys()),
            y=list(sections.values())
    )]
    layout = go.Layout(title='Unique Authors by Section', xaxis=dict(title='Section'), yaxis=dict(title='Number of Authors'))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='unique authors by section')

    return sections

def timeOfDayBySection():
    cur.execute("SELECT Sections.SectionName, Articles.Date FROM Sections JOIN Articles on Sections.Id = Articles.SectionId")
    results = cur.fetchall()

    sections = {}
    for section, date in results:
        hours = int(date[date.find("T")+1 : date.find(":")])

        if section not in sections:
            sections[section] = {
            "earlyAM" : 0,
            "lateAM" : 0,
            "earlyPM" : 0,
            "latePM" : 0
            }

        if hours >= 18:
            sections[section]["latePM"] += 1
        elif hours >= 12:
            sections[section]["earlyPM"] += 1
        elif hours >= 6:
            sections[section]["lateAM"] += 1
        else:
            sections[section]["earlyAM"] += 1


    data = []
    for section in sections:
        data.append(go.Bar(
            x=list(sections[section].keys()),
            y=list(sections[section].values()),
            name=section
        ))

    layout = go.Layout(
        barmode='group'
    )

    layout = go.Layout(title='Article Timing by Section', xaxis=dict(title='Time'), yaxis=dict(title='Number of Articles'))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='article timing by section')
    return sections

conn.commit()

def interactive_prompt():
    #help_text = load_help_text()
    response = ''

    while response != 'exit':
        response = input('Enter a Section Id (1-4) or enter "charts": ')

        if response == "exit":
            print("bye")
            break

        elif response == 'help':
            print("Please enter a number 1-4 or enter 'charts' ")
            continue

        elif response == '1':
            print("Opinions Section")
            opinions = get_opinions()
            count = 0
            for title in opinions:
                count += 1
                number = str(count) + ')'
                print(number, title[0])
                print(title[1])
            continue

        elif response == '2':
            print("Politics Section")
            politics = get_politics()
            count = 0
            for title in politics:
                count += 1
                number = str(count) + ')'
                print(number, title[0])
                print(title[1])
            continue

        elif response == '3':
            print("World Section")
            world = get_world()
            count = 0
            for title in world:
                count += 1
                number = str(count) + ')'
                print(number, title[0])
                print(title[1])
            continue

        elif response == '4':
            print("Home Page")
            home = get_home()
            count = 0
            for title in home:
                count += 1
                number = str(count) + ')'
                print(number, title[0])
                print(title[1])
            continue

        elif response == 'charts':
            print("""
                1 Count Section Articles
                2 Headline Lengths
                3 Unique Authors
                4 Time of Day""")
            new_inp = ''
            while new_inp != "sections" or new_inp != "exit":
                new_inp = input('What type of chart would you like to see? OR type "sections" to enter a Section Id : ')
                if new_inp == "sections":
                    break
                if new_inp == "exit":
                    print('bye')
                    exit()
                if new_inp == '1':
                    countSectionArticles()
                elif new_inp == '2':
                    plotHeadlineLengths()
                elif new_inp == '3':
                    uniqueAuthorsBySection()
                elif new_inp == '4':
                    timeOfDayBySection()
                else:
                    print("Please enter a valid chart number or 'sections' to go back ")
        else:
            print("Please enter a valid Section Id")


if __name__ == "__main__":
    sections_insts = get_sections()
    get_articles(sections_insts)
    interactive_prompt()
