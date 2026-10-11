import subprocess
import time

import schedule


def popup(title, text):
    script = 'display notification "{}" with title "{}"'.format(
        text.replace('"', '\\"'), title.replace('"', '\\"')
    )
    subprocess.run(["osascript", "-e", script])


def eye_rest():
    popup("Eye Rest", "Look at something far away for a few seconds.")


def stretch():
    popup("Stretch Time", "Stand up and stretch your back and arms.")


def main():
    schedule.every(15).seconds.do(eye_rest)
    schedule.every(30).seconds.do(stretch)

    print("Reminders are on. Press Ctrl+C to quit.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
