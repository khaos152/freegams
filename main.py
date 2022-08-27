import requests
from lxml import html
from datetime import datetime
import platforms
import config
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from datefinder import find_dates

class scrape:
    def get_html(url):
        req = requests.get(url)
        htm = html.fromstring(req.text)
        return htm

class log:
    def write(msg):
        with open(config.logfile, "a+") as f:
            f.write(msg)
    def read():
        with open(config.logfile, "r") as f:
            return f.read()

class post:
    def get_content(number): # reads announcements from freegamefinders
        content  = scrape.get_html(platforms.freegamefinders_url)
        dictlist = []
        for i in range(1, number, 1):
            xpaths   = platforms.announcement(i)
            dict     = {}
            dict["date"]       = content.xpath(xpaths["date"])[0]
            dict["title"]      = content.xpath(xpaths["title"])[0]
            dict["url"]        = content.xpath(xpaths["url"])[0]
            dict["bodytext"]   = content.xpath(xpaths["bodytext"])
            dict["bodyurls"]   = content.xpath(xpaths["bodyurls"])[0]
            dict["likes"]      = content.xpath(xpaths["likes"])[0]
            dict["expires"]    = time.get_date(dict["bodytext"], True)  # string version
            dict["expires_d"]  = time.get_date(dict["bodytext"], False) # date version
            dictlist.append(dict)
        return dictlist

    def is_new(dict): # takes the newest announcement if it hasn't been seen yet
        title = dict[0]
        if title in log.read(): # if the first title is inside the logs
            return False
        else:
            return True

    def is_blacklisted(dict):
        title = dict[0]
        for word in config.blacklist:
            if word in title:
                return True
        return False

    def allows_scraping(dict):
        if dict["scrape"]:
            return True
        else:
            return False

    def is_outdated(date):
        if (date < datetime.now()):
            return True
        else:
            return False

    def cleanup(dictlist):
        for dict in dictlist:
            if not post.is_new(dict["title"]):
                dictlist.remove(dict)
                print(f'{dict["title"]} has already been posted!')
            elif post.is_blacklisted(dict["title"]):
                dictlist.remove(dict)
                print(f'{dict["title"]} is blacklisted!')
            elif post.is_outdated(dict["expires_d"]):
                dictlist.remove(dict)
                print(f'{dict["title"]} has expired!')
        return dictlist

class game:
    def get_platform(url):
        for platform in platforms.platforms:
            for redir_url in platform["redir"]:
                if redir_url in url:
                    platform["target_url"] = url.replace(platforms.redirecting_url, "")
                    return platform
        return False

    def get_details(url, platform):
        content     = scrape.get_html(url)
        dict        = {}
        dict["title"]       = content.xpath(platform["gtitle"])[0]
        dict["picture"]     = content.xpath(platform["glink"])[0]
        dict["description"] = content.xpath(platform["gdesc"])[0]
        return dict

class time:
    def cleanup(date):
        date_clear = date.replace("\r","").replace("\n","").replace("\t","").replace("-","")
        return date_clear

    def release_format(date):
        date_clear     = time.cleanup(date)
        date_out       = datetime.strptime(date_clear, '%d %b @ %I:%M%p ').replace(year=datetime.now().year)
        date_timestamp = date_out.timestamp()
        return date_timestamp

    def get_date(text_list, string):
        text = ""
        for t in text_list:
            text += t + "\n"
        for date in find_dates(text):
            first_find = date.replace(year=datetime.now().year)
            date_out   = first_find.replace(year=datetime.now().year) # fix date year
            if string:
                date_out = date_out.strftime("%B %d, %Y") # date becomes string
            return date_out


class discord:
    def urls():
        with open(config.urls, "r") as f:
            url_list = f.read().split("\n")
            return url_list

    def move(dict_game, dict_platform, timestamp):
        dict                = {}
        dict["title"]       = dict_game["title"]
        dict["color"]       = dict_platform["color"]
        dict["url"]         = dict_platform["target_url"]
        dict["author"]      = dict_platform["title"]
        dict["author_url"]  = dict_platform["link"]
        dict["author_icon"] = dict_platform["icon"]
        dict["field_name"]  = "test"
        dict["field_value"] = "test"
        if config.footer   == True:
            dict["footer_text"] = platforms.footer_text
            dict["footer_icon"] = platforms.footer_icon
        dict["thumbnail"]   = dict_platform["thumb"]
        dict["image"]       = dict_game["picture"]
        dict["timestamp"]   = timestamp
        return dict

    def translate(url, dict):
        webhook = DiscordWebhook(url=url)
        embed   = DiscordEmbed(title=dict["title"], color=dict["color"], url=dict["url"])
        embed.set_author(name=dict["author"], url=dict["author_url"], icon_url=dict["author_icon"])
        for name, value in zip(dict["field_name"], dict["field_value"]):
            embed.add_embed_field(name=name, value=value, inline=False)
        embed.set_footer(text=dict["footer_text"], icon_url=dict["footer_icon"])
        embed.set_thumbnail(url=dict["thumbnail"])
        embed.set_image(url=dict["image"])
        embed.set_timestamp(dict["timestamp"])
        webhook.add_embed(embed)
        return webhook

    def send(webhook):
        return webhook.execute()

    def sendstatus():
        return

### RUN ###

def run(url, debug):
    if url == "":
        url = discord.urls()[0]
    announcements     = post.get_content(6)
    if not debug:
        announcements = post.cleanup(announcements)
    for a in announcements:
        platform        = game.get_platform(a["bodyurls"])
        if post.allows_scraping(platform):
            print(a["title"])
            gamedata        = game.get_details(platform["target_url"], platform)
            timestamp       = time.release_format(a["date"])
            gamedata_sorted = discord.move(gamedata, platform, timestamp)
            refer = f''':octopus: [GitHub](https://github.com/khaos152/freegams)
            :information_source: [Source]({platforms.freegamefinders_url})
            :gift: [**Get '{gamedata["title"]}' for free**]({platform["target_url"]})'''
            gamedata_sorted["field_name"]  = ["expires", "description", "links", "rating"]
            gamedata_sorted["field_value"] = [":calendar: " + a["expires"], gamedata["description"], refer, ":thumbsup: " + a["likes"]]
            gamedata_json   = discord.translate(url, gamedata_sorted)
            discord.send(gamedata_json)
            if not debug:
                log.write(a["title"])
        else:
            print(f'{a["title"]} can not be posted as {platform["title"]} does not allow scraping!')
