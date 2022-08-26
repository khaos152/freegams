import requests
from lxml import html
from datetime import datetime
import platforms
import config
from discord_webhook import DiscordWebhook, DiscordEmbed

class scrape:
    def get_html(url):
        req = requests.get(url)
        htm = html.fromstring(req.text)
        return htm

class log:
    def write(msg):
        with open(config.file, "w") as f:
            f.write(msg)
    def read():
        with open(config.file, "r") as f:
            return f.read()

class post:
    def get_content(number): # reads announcements from freegamefinders
        xpaths   = platforms.announcement(number)
        content  = scrape.get_html(platforms.freegamefinders_url)
        title    = content.xpath(xpaths[0])
        url      = content.xpath(xpaths[1])
        bodytext = content.xpath(xpaths[2])
        bodyurls = content.xpath(xpaths[3])
        return title, url, bodytext, bodyurls

    def is_new(content): # takes the newest announcement if it hasn't been seen yet
        if content[0] != log.read(): # if the first title is not inside the logs
            return True
        else:
            return False

class game:
    def get_platform(url):
        for platform in platforms.platforms:
            for redir_url in platform["redir"]
                if redir_url in url:
                    return platform
        return False

    def get_details(url, platform):
        content     = scrape.get_html(url)
        title       = content.xpath(platform["gtitle"])
        picture     = content.xpath(platform["glink"])
        description = content.xpath(platform["gdesc"])
        if len(content.xpath(platform["check"])) > 0:
            free = True
        else:
            free = False
        return title, picture, description, free

class discord:
    def translate(url, content):
        webhook = DiscordWebhook(url=url)
        embed   = DiscordEmbed(title=content["title"], color=content["color"], url=content["url"])
        embed.set_author(name=content["author"], url=content["author_url"], icon_url=content["author_icon"])
        for name, value in zip(content["field_name"], content["field_value"]):
		    embed.add_embed_field(name=name, value=value)
		embed.set_footer(text=content["footer_text"], icon_url=["footer_icon"])
		embed.set_thumbnail(url=content["thumbnail"])
		embed.set_image(url=content["image"])
	    embed.set_timestamp(content["timestamp"])
        webhook.add_embed(embed)
        return webhook

    def send(webhook):
        return webhook.execute()

class main:
    def run(url, log):
        post = 