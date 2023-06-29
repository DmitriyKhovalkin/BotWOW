import random
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as Keyb
import pyaudio
import audioop
import time
import math
import psutil
import ctypes
import pyautogui
from random import randint


PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

dev = False
keyboard = Keyb()
mouse = Controller()
path = 'trash/trash.png'
random_second = [0.3, 0.4, 0.5, 0.6, 0.7]

def check_process():
    print('Проверка WoW is running')
    wow_process_names = ["Wow.exe"]
    running = False
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if any(p.name() in s for s in wow_process_names):
            print(p.name())
            running = True
    if not running and not dev:
        print('WoW не запущен')
        exit()
    print('WoW запущен')
    return running


def send_float():
    print('Закидуем поплавок')
    keyboard.press('1')
    keyboard.release('1')
    print('Ждём анимацию')
    time.sleep(2.51)


def jump():
    print('Прыжок!')
    keyboard.press(Key.space)
    time.sleep(0.1)
    keyboard.release(Key.space)
    time.sleep(1 + random.choice(random_second))


def move_mouse(place):
    x, y = place[0], place[1]
    print("Moving cursor to " + str(place))
    mouse.position = x, y


def listen():
    print('Ну, теперь мы прислушиваемся к громким звукам...')
    success = False
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 20
    listening_start_time = time.time()

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 2)
            decibel = 20 * math.log10(rms)
            print(decibel)
            if decibel > 68 and i > 3:
                print('Ловись рыбка!')
                success = True
                break
            elif time.time() - listening_start_time > 20:
                print('Ничё не слышно!')
                break
        except ValueError:
            continue

    stream.stop_stream()
    stream.close()
    p.terminate()
    return success


def snatch():
    print('ЯЗЬЬЬ, Здоровенный ЯЯЯЯЯЗЬ!!!')
    keyboard.press(Key.shift)
    mouse.press(Button.right)
    time.sleep(0.1)
    mouse.release(Button.right)
    keyboard.release(Key.shift)


def main():
    if check_process() and not dev:
        print("Ждём 3 сек пока переключаемся на Wow")
        time.sleep(3)

    count = 0

    while count < 50000001:
        try:
            send_float()
            button = pyautogui.locateOnScreen(path, confidence=0.7)
            x, y, w, h = button
            mouse.position = x + 10, y + 20
            count += 1
            if not listen():
                print('Тут рыбы нет!')
                jump()
                continue
            time.sleep(random.choice(random_second))
            snatch()
            time.sleep(randint(3, 4))
        except TypeError:
            print('Какая-то хуйня')
            time.sleep(random.choice(random_second))


if __name__ == '__main__':

    main()






