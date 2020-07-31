from threading import Thread, Event
from time import sleep


class MyTaskThread(Thread):
    def __init__(self, method, delay):
        super().__init__()
        self.flag = Event()
        self.method = method
        self.delay = delay
        self.suicide = False
        self.flag.set()

    def run(self):
        while self.flag.wait():
            sleep(self.delay)
            self.method()
            if self.suicide:
                break

    def setDelay(self, delay):
        self.delay = delay

    def pause(self):
        self.flag.clear()

    def resume(self):
        self.flag.set()

    def destroy(self):
        self.resume()
        self.suicide = True


class MyTimer(Thread):
    def __init__(self, time_limite):
        super().__init__()
        self.counter = 0
        self.time_limite = time_limite
        self.flag = Event()
        self.flag.set()
        self.done = False
        self.suicide = False

    def run(self):
        while self.flag.wait():
            sleep(1)
            self.counter += 1
            if self.counter == self.time_limite:
                self.done = True
                break
            if self.suicide:
                break

    def pause(self):
        self.flag.clear()

    def resume(self):
        self.flag.set()

    def destroy(self):
        self.resume()
        self.suicide = True


class MyMusicPlayer(Thread):
    def __init__(self, music, time_wait, vol=0):
        super().__init__()
        self.counter = 0
        self.time_wait = time_wait
        self.flag = Event()
        self.flag.set()
        self.done = False
        self.music = music
        self.music.set_volume(vol)
        self.suicide = False

    def run(self):
        while self.flag.wait():
            sleep(1)
            self.counter += 1
            if self.counter == self.time_wait:
                self.done = True
                self.music.play(-1)
                break
            if self.suicide:
                break

    def set_volume(self, vol):
        self.music.set_volume(vol)

    def play(self, sound=True):
        if sound:
            vol_max = 0.2
            vol = 0
            while vol < vol_max:
                vol += 0.08 * vol_max
                sleep(0.1)
                self.music.set_volume(vol)
            self.set_volume(vol_max)
        else:
            self.set_volume(0)

    def pause(self, sound=True):
        if sound:
            # self.music.set_volume(0)
            vol_max = 0.2
            vol = 0.1
            while vol > 0:
                vol -= 0.03 * vol_max
                sleep(0.1)
                self.music.set_volume(vol)
            self.set_volume(0)
        else:
            self.set_volume(0)

    def destroy(self):
        self.suicide = True
