import time
import sys
import os

def main():
    i = 0
    while True:
        print("script_2.py")
        time.sleep(1)
        i = i + 1
        if i > 3:
            import signal
            os.kill(os.getppid(), signal.SIGTERM)

if __name__ == '__main__':
    main()