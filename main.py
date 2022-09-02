import requests
from lxml import html
from datetime import datetime
import platforms
import config
from discord_webhook import DiscordWebhook, DiscordEmbed
from datetime import datetime
from datefinder import find_dates
from os.path import isfile

class scrape:
    def get_html(url):
        req = requests.get(url)
        htm = html.fromstring(req.text)
        return htm

class condition:
    def is_missing(file):
        if isfile(file):
            return False
        else:
            return True
    
class log:
    def write(msg):
        with open(config.logfile, "a+") as f:
            f.write(msg + "\n")
    def read():
        if condition.is_missing(config.logfile):
            log.write("")
        with open(config.logfile, "r") as f:
            return f.read()

class post:
    def get_content(number): # reads announcements from freegamefinders
        content  = scrape.get_html(platforms.freegamefinders_url)
        dictlist = []
        for i in range(1, number, 1):
            dict         = platforms.announcement_xpaths(i)
            dict_out     = {}
            for element in dict[0]:
                dict_out[element] = content.xpath(dict[0][element])[0]
            for element in dict[1]:
                dict_out[element] = content.xpath(dict[1][element])
            dictlist.append(dict_out)
        return dictlist

    def fix_dates(dict_list):
        dict_list_out = []
        for dict in dict_list:
            dict_out = dict
            annc_date               = time.release_format(dict["annc_date"])
            dict_out["annc_date_d"] = annc_date[0]
            dict_out["annc_date_t"] = annc_date[1]
            dict_out["expires_d"]   = time.get_date(dict_out["annc_text"], annc_date[0])  # string version
            dict_out["expires"]     = dict_out["expires_d"].strftime("%B %d, %Y") # date version
            dict_list_out.append(dict_out)
        return dict_list_out

    def is_new(string):
        if string in log.read():
            return False
        else:
            return True

    def is_blacklisted(dict):
        title = dict[0]
        for word in config.blacklist:
            if word in title:
                return True
        return False

    def is_outdated(date):
        if (date < datetime.now()):
            return True
        else:
            return False

    def cleanup(dictlist):
        dictlist_out = []
        for dict in dictlist:
            target = dict["annc_title"]
            if not post.is_new(target):
                print(f'{target} has already been posted!')
            elif post.is_blacklisted(target):
                print(f'{target} is blacklisted!')
            elif post.is_outdated(dict["expires_d"]):
                print(f'{target} has expired on {dict["expires"]}!')
            else:
                dictlist_out.append(dict)
        return dictlist_out

class game:
    def get_platform(dict):
        dict_out = dict
        url_list = dict["annc_listed_urls"]
        for url in url_list:
            for platform in platforms.platforms:
                for redir_url in platform["id_url"]:
                    if redir_url in url:
                        dict_out.update(platform)
                        dict_out["game_url"] = url.replace(platforms.redirecting_url, "")
                        return dict_out
        return False

    def get_details(dict):
        content     = scrape.get_html(dict["game_url"])
        dict_out        = dict
        for element in dict:
            if str(dict[element])[:2] == "//": # if element is xpath
                dict_out[element] = content.xpath(dict[element])[0] 
        return dict_out

    def fix_missing(dict):
        
        if "game_title" not in dict.keys():
            dict["game_title"] = dict["annc_title"]
        if "game_image" not in dict.keys():
            dict["game_image"] = platforms.missing
        if "game_desc" not in dict.keys():
            dict["game_desc"]  = "*no description*"
        if ("verify" not in dict.keys()) and ("verify_exp" not in dict.keys()):
            dict["verify"]     = "❌"
        elif dict["verify_exp"] in dict["verify"]:
            dict["verify"]     = "✅"
        else:
            dict["verify"]     = "❌"
        return dict

class time:
    def cleanup(date):
        date_clear = date.replace("\r","").replace("\n","").replace("\t","").replace("-","")
        return date_clear

    def release_format(date):
        date_clear     = time.cleanup(date)
        date_out       = datetime.strptime(date_clear, '%d %b @ %I:%M%p ').replace(year=datetime.now().year)
        date_timestamp = date_out.timestamp()
        return date_out, date_timestamp

    def get_date(text_list, old_date):
        text = ""
        for t in text_list:
            text += t + "\n"
        outputs = [text]
        for i in range(1000, 2400, 100): # removes numbers that irritate datefinder
            outputs.append(outputs[-1].replace(str(i), ""))
            outputs.remove(outputs[-2])
        for date in find_dates(outputs[-1]):
            first_find = date
            date_out   = first_find.replace(year=datetime.now().year) # fix date year
            if date_out > old_date: # if the expiration date is newer than the announcement date
                return date_out
        return False

class discord:
    def urls():
        with open(config.urls, "r") as f:
            url_list = f.read().split("\n")
            url_list = list(filter(None, url_list))
            return url_list

    def move(dict):
        dict_out                = {}
        if dict["game_title"]:
            hook_title          = dict["game_title"]
        else:
            hook_title          = dict["annc_title"]
        dict_out["title"]       = hook_title
        dict_out["color"]       = dict["hook_color"]
        dict_out["url"]         = dict["game_url"]
        dict_out["author"]      = dict["store"]
        dict_out["author_url"]  = dict["store_url"]
        dict_out["author_icon"] = dict["store_icon"]
        refer = platforms.linktree(dict["game_title"], dict["game_url"])
        dict_out["field_name"]  = ["expires", "description", "links", "rating", "verified"]
        dict_out["field_value"] = [":calendar: " + dict["expires"], dict["game_desc"], refer, ":thumbsup: " + dict["annc_rating"], dict["verify"]]
        if config.footer   == True:
            dict_out["footer_text"] = platforms.footer_text
            dict_out["footer_icon"] = platforms.footer_icon
        dict_out["thumbnail"]   = dict["thumbnail"]
        dict_out["image"]       = dict["game_image"]
        dict_out["timestamp"]   = dict["annc_date_t"]
        return dict_out

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

    def send_success(execute):
        execute_status = execute.status_code
        if execute_status == 200:
            return True
        else:
            return False

### RUN ###

def run(url_list, debug):
    if url_list == []:
        if condition.is_missing(config.urls):
            exit(f"Your webhook-url file '{config.urls}' is missing!")
        url_list = discord.urls()
    announcements    = post.get_content(config.scan_amount)
    announcements_wd = post.fix_dates(announcements)
    if not debug:
        announcements_wd = post.cleanup(announcements_wd)
    for a in announcements_wd:
        platform        = game.get_platform(a)
        gamedata        = game.get_details(platform)
        gamedata        = game.fix_missing(gamedata) # fixes for stores that prohibit web scraping
        gamedata_sorted = discord.move(gamedata)
        for url in url_list:
            gamedata_json = discord.translate(url, gamedata_sorted)
            sent          = discord.send(gamedata_json)
            success       = discord.send_success(sent)
            if success:
                print(f'\'{gamedata["annc_title"]}\' has successfully been posted!')
                if not debug:
                    if post.is_new(gamedata["annc_title"]):
                        log.write(gamedata["annc_title"])
            else:
                print(f'\'{gamedata["annc_title"]}\' could not be posted!')
