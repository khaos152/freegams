from sys import argv

self    = "freegams"
version = 1.0

if __name__ == "__main__":
    args  = argv[1:]
    cycle = 0

    for a in args:
        arg = a.lower()
        url = ""
        if "https://" in arg: # look for webhookurl
            url += arg

        elif arg == "new":
            main.run(url, log=True, url=url)
            break

        elif arg == "loop":
            while True:
                main.run(url, log=True, url=url)
                sleep(timer)
            break

        elif arg == "debug":
            main.run(url, log=False, url=url)
            break
        