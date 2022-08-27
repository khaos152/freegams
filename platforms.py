freegamefinders_url   = "https://steamcommunity.com/groups/freegamesfinders/announcements/listing"

redirecting_url       = "https://steamcommunity.com/linkfilter/?url="

thumbs                = "https://raw.githubusercontent.com/khaos152/freegams/main/thumbnails/"
profile_icon          = thumbs + "gift_"

footer_icon   = "https://avatars.githubusercontent.com/u/83596694?v=4"
footer_text   = "Freega • Free Game Notifier, Discord-Webhook"



def announcement(number):
    annc_element     = f'//div[@class="announcement"][{number}]'
    annc             = {}
    annc["date"]     = annc_element + '//div[@class="announcement_byline"]/text()'
    annc_head        = annc_element + '//a[@class="large_title"]'
    annc["title"]    = annc_head + "/text()"
    annc["url"]      = annc_head + "/@href"
    annc_body        = annc_element + '//div[@class="bodytext"]'
    annc["bodytext"] = annc_body + "/text()"
    annc["bodyurls"] = annc_body + '//a[@class="bb_link"]/@href'
    annc["likes"]    = annc_element + '//span[@class="rateUpCount"]//span/text()'
    return annc

platforms  = [
{
"scrape" : True,
"title"  : "Steam Store",
"icon"   : profile_icon + "steam.png",
"thumb"  : thumbs + "steam.png",
"link"   : "https://store.steampowered.com/app",
"color"  : 2302894,
"redir"  : ["https://store.steampowered.com/app/"],
"gtitle" : '//div[@class="apphub_AppName"]/text()',
"glink"  : '//img[@class="game_header_image_full"]/@src',
"gdesc"  : '//div[@class="game_description_snippet"]/text()',
},

{
"scrape" : True,
"title"  : "Good old Games / GOG.com",
"icon"   : profile_icon + "gog.png",
"thumb"  : thumbs + "gog.png",
"link"   : "https://www.gog.com/",
"color"  : 14139156,
"redir"  : ["https://www.gog.com/game/", "https://www.gog.com/en/game/"],
"gtitle" : '//h1[@class="productcard-basics__title"]/text()',
"glink"  : '//meta[@property="og:image"]/@content',
"gdesc"  : '//div[@class="description"]/text()',
},

{
"scrape" : False,
"title"  : "Epic Games",
"icon"   : profile_icon + "epic.png",
"thumb"  : thumbs + "epic.png",
"link"   : "https://www.store.epicgames.com/",
"color"  : 16777214,
"redir"  : ["https://store.epicgames.com/en-US/p/"],
}
]