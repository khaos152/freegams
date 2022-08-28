from sys import argv
import main

if __name__ == "__main__":
    args  = argv[1:]
    cycle = 0

    for a in args:
        arg = a.lower()
        url = []
        if "https://" in arg: # look for webhookurl
            url.append(arg)

        elif arg == "new":
            main.run(url, debug=False)
            break

        elif arg == "loop":
            while True:
                main.run(url, debug=False)
                sleep(timer)
            break

        elif arg == "debug":
            main.run(url, debug=True)
            break
