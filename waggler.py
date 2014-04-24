import time
import RPi.GPIO as GPIO
import random
import driver
import pickle

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

def main():
    counter = 10
    start_time = time.time()
    attach_int()
    while time.time() < start_time + counter:
        time.sleep(0.01)
        cur_time = counter - (time.time() - start_time)
        output = "%d.%03d" % (cur_time,score)
#        print(output)
        leds.update(output)
    detach_int()


if __name__ == '__main__':
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
        dot_time = 0.5
        #dot intro
        leds.update(' .   ')
        leds.set_pwm(max_pwm)
        time.sleep(dot_time)
        leds.update(' . .  ')
        time.sleep(dot_time)
        leds.update(' . . . ')
        time.sleep(dot_time)
        leds.update(' . . . . ')
        time.sleep(dot_time)

        main()  
        leds.update("%4d" % score )
        time.sleep(5)
        leds.fade(max_pwm,0,length)
        time.sleep(1)

        print("score = %d" % score)
        if score > high_score:
            #disco mode?
            print("new high score %d" % score)
            high_score = score
            pickle.dump(score,open("score.pk",'wb'))
    
