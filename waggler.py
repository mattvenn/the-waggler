import time
import RPi.GPIO as GPIO
import random
import driver

score = 0
up = 13
down = 15
butt = 19

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(butt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    #attach interrupts for up and down
    GPIO.add_event_detect(up,GPIO.FALLING,callback=inc_score,bouncetime=10)
    GPIO.add_event_detect(down,GPIO.FALLING,callback=inc_score,bouncetime=10)

def inc_score(channel):
    global score
    score += 1

def main():
    global score
    counter = 10
    for i in range(counter,0,-1):
        time.sleep(0.1)
        if random.randint(0,10) > 5:
            score += 1
        output = "%02d.%02d" % (i,score)
        print(output)
        leds.update(output)


if __name__ == '__main__':
    setup()
    leds = driver.driver()
    leds.set_pwm(100)
    while True:
   #     GPIO.wait_for_edge(butt,GPIO.FALLING)
        print("wait for button")
        raw_input()
        main()
    
