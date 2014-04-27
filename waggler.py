import time
import RPi.GPIO as GPIO
import random
import driver
import pickle
import cam
import twitter
from sounds import Sound

score = 0
up = 13
down = 15
butt = 19
last = 0 #last button

#fade params
max_pwm = 100
length = 1

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def attach_int():
    #attach interrupts for up and down
    GPIO.add_event_detect(up,GPIO.FALLING,callback=inc_score,bouncetime=10)
    GPIO.add_event_detect(down,GPIO.FALLING,callback=inc_score,bouncetime=10)

def detach_int():
    GPIO.remove_event_detect(up)
    GPIO.remove_event_detect(down)

def inc_score(channel):
    global last, score
    if channel != last:
        score += 1
        last = channel

def main(cam_thread):
    thread_started = False
    counter = 10
    start_time = time.time()
    attach_int()
    while time.time() < start_time + counter:
        time.sleep(0.01)
        cur_time = counter - (time.time() - start_time)
        output = "%d.%3d" % (cur_time,score)
#        print(output)
        leds.update(output)
        if cur_time <= 1 and not thread_started:
            print("start capture thread")
            cam_thread.start()
            thread_started = True

    cam_thread.join()
    detach_int()


if __name__ == '__main__':

    win_sound = Sound('win.wav')
    win_sound.play()
    end_sound = Sound('game_over.wav')
    start_sound = Sound('start.wav')
    #load high score
    #pickle.dump(0,open("score.pk",'wb'))
    try:
        high_score = pickle.load(open("score.pk",'rb'))
    except:
        high_score = 0

    print("high score = %d" % high_score)
    setup()
    leds = driver.driver()
    leds.set_pwm(max_pwm)
    while True:
        score = 0
        output = "%4d" % high_score
        leds.update(output)
        leds.fade(0,max_pwm,length)
        print("wait for button")
        GPIO.wait_for_edge(butt,GPIO.FALLING)
        leds.fade(max_pwm,0,length)
        cam_thread=cam.CamThread()
        dot_time = 0.5
        #dot intro
        leds.update('   4')
        start_sound.play()
        leds.set_pwm(max_pwm)
        time.sleep(dot_time)
        leds.update('   3')
        start_sound.play()
        time.sleep(dot_time)
        leds.update('   2')
        start_sound.play()
        time.sleep(dot_time)
        leds.update('   1')
        start_sound.play()
        time.sleep(dot_time)

        """ run the game """
        main(cam_thread)  

        print("score = %d" % score)
        leds.update("%4d" % score )


        if score > high_score:
            win_sound.play()
            #disco mode?
            print("new high score %d" % score)
            message = "I set a new high score on the waggler! %d #makerfaireuk" % score
            high_score = score
            pickle.dump(score,open("score.pk",'wb'))
        else:
            end_sound.play()
            message = "I got %d on the waggler! #makerfaireuk" % score
    
        tweet_thread=twitter.TweetThread(message)
        tweet_thread.start()

        time.sleep(4)
        leds.fade(max_pwm,0,length)
        time.sleep(1)
