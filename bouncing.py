#!/usr/bin/env python3

from graphics import *
from time import sleep, time
from random import randrange, random, uniform
from math import pi, sin, cos

# some configurable options
CIRCLE_COUNT = 10
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
COLORS = ["red", "blue", "green", "yellow", "black", "white", "purple"]

# tweaks the angle slightly for good looks
def adjustAngle(circle):
    circle.a += uniform(-pi/20, pi/20)

def main():
    # creates a window to put our stuff on
    win = GraphWin("hello", WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # create the circles
    circles = []
    for ci in range(0, CIRCLE_COUNT):
        # create a random radius, starting position, color, velocity, and angle
        radius = randrange(10, 20)
        startx = randrange(0 + radius, WINDOW_WIDTH - radius)
        starty = randrange(0 + radius, WINDOW_HEIGHT - radius)
        color = COLORS[randrange(0, len(COLORS))]
        velocity = uniform(100, 200)
        angle = uniform(0, 2 * pi)
        # create the circle with the values calculated above
        circle = Circle(Point(startx, starty), radius)
        circle.v = velocity
        circle.a = angle
        circle.setFill(color)
        circle.draw(win)
        # add the circle to our list of circles for later refernece
        circles.append(circle)
    
    # the main loop to handle the simulation
    lastTick = 0.0 # stores the time of the last tick
    tps = 10.0 # the current ticks per second
    tpsMultiplier = 1.0 # a multiplier used to speed up the TPS change when it's really needed
    tpsChanging = 1 # determines which direction the TPS is currently changing (1 for increasing, -1 for decreasing)
    while True:
        lastTick = time()
        
        # iterate over each circle
        for circle in circles:
            dx = circle.v/tps * sin(circle.a) # calculate the change in x
            dy = circle.v/tps * cos(circle.a) # calculate the change in y
            circle.move(dx, dy) # move the circle accordingly
            
            # handle collision with the walls
            if circle.getCenter().x <= 0 + circle.getRadius(): # if the ball is past the left side of the screen
                adjustAngle(circle)
                if circle.a < pi:
                    circle.a = pi - circle.a
                else:
                    circle.a = 2*pi - circle.a
            if circle.getCenter().x + circle.getRadius() >= WINDOW_WIDTH: # if the ball is past the right side of the screen
                adjustAngle(circle)
                circle.a = 2*pi - circle.a
            if circle.getCenter().y <= 0 + circle.getRadius(): # if the ball is past the top of the screen
                adjustAngle(circle)
                circle.a = pi - circle.a
            if circle.getCenter().y + circle.getRadius() >= WINDOW_HEIGHT: # if the ball is past the bottom of the screen
                adjustAngle(circle)
                circle.a = pi - circle.a
        
	# calculate the amount of time to sleep for
        now = time()
        sleepFor = 1.0/tps - (now - lastTick)
	
	# if sleeping would put us behind...
        if sleepFor < 0:
            # we're behind schedule, we need to slow down the TPS
            if tpsChanging > 0:
                tpsChanging = -1
                tpsMultiplier = 1.0
            tps -= tpsMultiplier
            tpsMultiplier *= 1.1
            # we can't go in reverse, so make it have a minimum value
            if tps <= 0:
                tps = 0.1
            print("Decreased TPS to " + str(tps))
        else:
            # we're doing fine, make the TPS a little faster
            if tpsChanging < 0:
                tpsChanging = 1
                tpsMultiplier = 1.0
            tps += tpsMultiplier
            tpsMultiplier *= 1.1
            print("Increased TPS to " + str(tps))
            # sleep to maintain the correct TPS
            sleep(sleepFor)

# run the program
main()
