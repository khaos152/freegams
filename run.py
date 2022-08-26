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
            main.main.run(url, log=True)
            break

        elif arg == "loop":
            while True:
                main.main.run(url, log=True)
                sleep(timer)
            break

        elif arg == "debug":
            main.main.run(url, log=False)
            break
        