# import RPi.GPIO as gpio

PIN = 0
STATE = 1
COLOR = 2


class LedHelper:

    def __init__(self):
        self.visible = True
        self.forceon = False
        self.led_green = (17, True, 'Green')
        self.led_blue = (18, True, 'Blue')
        self.led_red = (19, True, 'Red')
        self.lights = [self.led_green, self.led_blue, self.led_red]
        # gpio.setup(self.led_green[0], gpio.OUT)
        # gpio.setup(self.led_blue[0], gpio.OUT)
        # gpio.setup(self.led_red[0], gpio.OUT)
        print 'initialized'

    def getGreenState(self):
        return self.led_green[STATE]

    def getBlueState(self):
        return self.led_blue[STATE]

    def getRedState(self):
        return self.led_red[STATE]

    def setGreenState(self, state):
        previous_state = self.getGreenState()
        self.led_green = (self.led_green[PIN], state, self.led_green[COLOR])
        if state is not previous_state:
            self.update([self.led_green])

    def setBlueState(self, state):
        previous_state = self.getBlueState()
        self.led_blue = (self.led_blue[PIN], state, self.led_blue[COLOR])
        if state is not previous_state:
            self.update([self.led_blue])

    def setRedState(self, state):
        previous_state = self.getRedState()
        self.led_red = (self.led_red[PIN], state, self.led_red[COLOR])
        if state is not previous_state:
            self.update([self.led_red])

    def turnOff(self):
        self.visible = False
        for light in self.lights:
            print 'Turned off ' + light[COLOR]
            # gpio.output(light[PIN], False)

    def turnOn(self):
        self.visible = True
        self.update(self.lights)

    def forceOn(self, value):
        self.forceon = value

    def monitorCrashed(self):
        self.setGreenState(False)
        self.setBlueState(False)
        self.setRedState(True)

    def update(self, lights_to_update):
        if self.visible or self.forceon:
            for light in lights_to_update:
                print light[COLOR], 'state changed'
                #gpio.output(light[PIN], light[STATE])
