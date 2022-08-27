import requests
from lxml import html
from datetime import datetime
import platforms
import config
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import strptime, datetime

class scrape:
    def get_html(url):
        req = requests.get(url)
        htm = html.fromstring(req.text)
        return htm

class log:
    def write(msg):
        with open(config.file, "a+") as f:
            f.write(msg)
    def read():
        with open(config.file, "r") as f:
            return f.read()

class post:
    def get_content(number): # reads announcements from freegamefinders
        content  = scrape.get_html(platforms.freegamefinders_url)
        dictlist = []
        for i in range(1, number, 1):
            xpaths   = platforms.announcement(i)
            dict["date"]     = content.xpath(xpaths[0])
            dict["title"]    = content.xpath(xpaths[1])
            dict["url"]      = content.xpath(xpaths[2])
            dict["bodytext"] = content.xpath(xpaths[3])
            dict["bodyurls"] = content.xpath(xpaths[4])
            dict["likes"]    = content.xpath(xpaths[5])
            dictlist.append(dict)
        return dictlist

    def is_new(content): # takes the newest announcement if it hasn't been seen yet
        title = content[0]
        if title in log.read(): # if the first title is inside the logs
            return False
        else:
            return True

    def is_blacklisted(content):
        title = content[0]
        for word in config.blacklist:
            if word in title:
                return True
        return False

    def cleanup(dictlist):
        for dict in dictlist:
            if not is_new(dict["title"]):
                dictlist.remove(dict)
            elif is_blacklisted(dict["title"])
                dictlist.remove(dict)
        return dictlist

class game:
    def get_platform(url_list):
        for url in url_list:
            for platform in platforms.platforms:
                for redir_url in platform["redir"]:
                    if redir_url in url:
                        platform["target_url"] = url.replace(platforms.redirecting_url, "")
                        return platform
        return False

    def get_details(url, platform):
        content     = scrape.get_html(url)
        dict["title"]       = content.xpath(platform["gtitle"])
        dict["picture"]     = content.xpath(platform["glink"])
        dict["description"] = content.xpath(platform["gdesc"])
        return dict

class time:
    def release_format(date):
        date_out       = datetime.strptime(date, '%d %b @ %I:%M').replace(year=datetime.now().year)
        date_timestamp = date_out.timestamp()
        return date_timestamp

    def expiration_format(date):
        return
        

class discord:
    def move(dict_game, dict_platform, timestamp):
        dict["title"]       = dict_game["title"]
        dict["color"]       = dict_platform["color"]
        dict["url"]         = dict_platform["target_url"]
        dict["author"]      = dict_platform["title"]
        dict["author_url"]  = dict_platform["link"]
        dict["author_icon"] = dict_platform["icon"]
        dict["field_name"]  = 
        dict["field_value"] = 
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
            embed.add_embed_field(name=name, value=value)
        embed.set_footer(text=dict["footer_text"], icon_url=["footer_icon"])
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

def run(url, log):
    announcements        = post.get_content(3)
    wanted_announcements = post.cleanup(announcements)
    for a in announcements:
        platform        = game.get_platform(a["bodyurls"])
        gamedata        = game.get_details(platform["target_url"], platform)
        gamedata_sorted = discord.move(gamedata)
        gamedata_json   = discord.translate(gamedata_sorted)
        discord.send(gamedata_json)



print(post.get_content(1))