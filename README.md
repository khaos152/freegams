# freegams

Free Game Notifier, Discord-Webhook

(This script merely scans its [source](https://steamcommunity.com/groups/freegamesfinders/announcements) for new content and sends an according message to your Discord-Webhook.)

------------------------------------------
<p align="center">
<a href="https://steamcommunity.com/groups/freegamesfinders/announcements"><img title="Free Game Finders" src="https://avatars.cloudflare.steamstatic.com/cebef01be773032093af3b4b453bb25ae85e0c93_full.jpg" height="150"></a>
<a href="https://discord.gg/pTUupKE"><img title="FGF Discord Server" src="https://wallpaperaccess.com/full/765574.jpg" width="150"></a>
<a href="https://discord.com/invite/AYAW26ycee"><img title="Freegams Discord Server" src="https://media.glassdoor.com/sqll/910317/discord-squarelogo-1497339636473.png" height="150"></a>
<a href="https://steamcommunity.com/profiles/76561197995443256"><img title="Creator of FGF SteamCommunity" src="https://avatars.cloudflare.steamstatic.com/e3d4765b84b1736a0819cb954b13f7b648c5ea1e_full.jpg" height="150"></a>
<a href="https://steamcommunity.com/id/Prometheus152/"><img title="Creator of Freegams" src="https://avatars.cloudflare.steamstatic.com/ba1f8273c0c475ecc43955acddcd9e5466ae06a2_full.jpg" height="150"></a>
</p>

------------------------------------------

# Setup:

* create a file for your webhook-urls
* get dependencies ```python -m pip install -U wheel lxml requests discordwebhook datefinder```
* start freegams ```python3 run.py new```
* start freegams as loop ```python3 run.py loop```

# Distributors:
*Steam, (Epic Games), Good old Games*

(language might change according to your ip address)

<p align="center">
<a href="https://www.gog.com/"><img title="Good Old Games" src="https://github.com/khaos152/freegams/blob/main/example/gog.png?raw=true" width="400"></a>
</p>

------------------------------------------
*hint: if a game has 'refused classification' the script might be unable to find it!(for exaple: Postal 2 in Germany and Austria)* 
<br />
*hint: since the epic games store prohibits web scraping, the notifications for their offers lack details such as images, descriptions and game titles!*
