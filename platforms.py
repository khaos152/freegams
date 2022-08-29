freegamefinders_url   = "https://steamcommunity.com/groups/freegamesfinders/announcements/listing"

redirecting_url       = "https://steamcommunity.com/linkfilter/?url="

repository            = "https://raw.githubusercontent.com/khaos152/freegams/"
thumbs                = repository + "main/thumbnails/"
profile_icon          = thumbs + "gift_"
missing               = thumbs + "no_image.png"

footer_icon   = "https://avatars.githubusercontent.com/u/83596694?v=4"
footer_text   = "Freega • Free Game Notifier, Discord-Webhook"

def linktree(game_title, game_url):
    value = f''':octopus: [GitHub]({repository})
:information_source: [Source]({freegamefinders_url})
:gift: [**Get '{game_title}' for free**]({game_url})'''
    return value

def announcement_xpaths(number):
    annc_element     = f'//div[@class="announcement"][{number}]'
    annc_head        = annc_element + '//a[@class="large_title"]'
    annc_body        = annc_element + '//div[@class="bodytext"]'
    elements = [
    { # xpath for single elements
        "annc_date"        : annc_element + '//div[@class="announcement_byline"]/text()',
        "annc_title"       : annc_head + "/text()",
        "annc_url"         : annc_head + "/@href",
        "annc_rating"      : annc_element + '//span[@class="rateUpCount"]//span/text()',
    },
    { # xpath for elements that need to stay a list
        "annc_text"        : annc_body + "/text()",
        "annc_listed_urls" : annc_body + '//a[@class="bb_link"]/@href',
    }]
    return elements

platforms  = [
{
"store"      : "Steam Store",
"store_icon" : profile_icon + "steam.png",
"thumbnail"  : thumbs + "steam.png",
"store_url"  : "https://store.steampowered.com/", # game_url for identifying platform
"hook_color" : 2302894,
"id_url"     : ["https://store.steampowered.com/app/"],
"game_title" : '//div[@class="apphub_AppName"]/text()',
"game_image" : '//img[@class="game_header_image_full"]/@src',
"game_desc"  : '//div[@class="game_description_snippet"]/text()',
},

{
"store"      : "Good old Games / GOG.com",
"store_icon" : profile_icon + "gog.png",
"thumbnail"  : thumbs + "gog.png",
"store_url"  : "https://www.gog.com/",
"hook_color" : 14139156,
"id_url"     : ["https://www.gog.com/game/", "https://www.gog.com/en/game/"],
"game_title" : '//h1[@class="productcard-basics__title"]/text()',
"game_image" : '//meta[@property="og:image"]/@content',
"game_desc"  : '//div[@class="description"]/text()',
},

{
"store"      : "Epic Games",
"store_icon" : profile_icon + "epic.png",
"thumbnail"  : thumbs + "epic.png",
"store_url"  : "https://www.store.epicgames.com/",
"hook_color" : 16777214,
"id_url"     : ["https://store.epicgames.com/en-US/p/"],
}
]
