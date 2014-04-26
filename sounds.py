import os
import threading

class SoundThread(threading.Thread):
    def __init__(self,wav_file):
        super(SoundThread,self).__init__()
        self.file = wav_file

        """ setup to use analog output"""
        os.system('amixer cset numid=3 1')

    def run(self):
        os.system('aplay %s' % self.file)

class Sound():
    def __init__(self,wav_file):
        self.file = wav_file

    def play(self):
        thread=SoundThread(self.file)
        thread.start()
        thread.join()
        
if __name__ == '__main__':
    thread=SoundThread("game_over.wav")
    thread.start()
    thread.join()
