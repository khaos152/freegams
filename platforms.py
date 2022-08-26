freegamefinders_url   = "https://steamcommunity.com/groups/freegamesfinders/announcements/listing"

def announcement(number):
    announcement_element  = f'//div[@class="announcement"][{number}]'
    announcement_head     = '//a[@class="large_title"]'
    announcement_title    = announcement_head + "/text()"
    announcement_url      = announcement_head + "/@href"
    announcement_body     = '//div[@class="bodytext"]'
    announcement_bodytext = announcement_body + "/text()"
    announcement_bodyurls = announcement_body + '//a[@class="bb_link"]/@href'
    return announcement_title, announcement_url, announcement_bodytext, announcement_bodyurls 

platforms  = [
{
"title"  : "steam",
"alias"  : "Steam Store",
"link"   : "https://store.steampowered.com/app",
"color"  : 2302894,
"redir"  : ["https://store.steampowered.com/app/"],
"gtitle" : '//div[@class="apphub_AppName"]/text()',
"glink"  : '//img[@class="game_header_image_full"]/@src',
"gdesc"  : '//div[@class="game_description_snippet"]/text()',
"check"  : '', # checks if game is actually free
},

{
"title"  : "gog",
"alias"  : "Good old Games / GOG.com",
"link"   : "https://www.gog.com/",
"color"  : 14139156,
"redir"  : ["https://www.gog.com/game/", "https://www.gog.com/en/game/"],
"gtitle" : '//h1[@class="productcard-basics__title"]/text()',
"glink"  : '//meta[@property="og:image"]/@content',
"gdesc"  : '//div[@class="description"]/text()',
"check"  : '', # checks if game is actually free
}
]