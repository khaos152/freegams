import requests
from lxml import html
from datetime import datetime
import platforms
import config

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
    def get_content(): # reads announcements from freegamefinders
        content = scrape.get_html(platforms.freegamefinders_url)
        title   = content.xpath(platforms.announcement_title)
        url     = content.xpath(platforms.announcement_url)
        bodytext = content.xpath(platforms.announcement_bodytext)
        bodyurls = content.xpath(platforms.announcement_bodyurls)
        return content, title, url, bodytext, bodyurls

    def get_body(htmls):
        content  = get_new()

        return bodytext, bodyurls

    def get_new(): # takes the newest announcement if it hasn't been seen yet
        data = post.get_content()
        if data[1][0] != log.read(): # if the first title is not inside the logs
            return data
        else:
            return False

post.get_new()