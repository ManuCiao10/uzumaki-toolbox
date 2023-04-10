import threading
from master.start import Start


def main():
    threading.Thread(target=Start).start()


if __name__ == "__main__":
    main()
