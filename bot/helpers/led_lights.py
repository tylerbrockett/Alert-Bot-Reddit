# import RPi.GPIO as gpio

PIN = 0
STATE = 1
COLOR = 2


class LedHelper:

    def __init__(self):
        self.active = True
        self.force_on = False
        self.led_green = (17, True, 'Green')
        self.led_blue = (18, True, 'Blue')
        self.led_red = (19, True, 'Red')
        self.lights = [self.led_green, self.led_blue, self.led_red]
        # gpio.setup(self.led_green[0], gpio.OUT)
        # gpio.setup(self.led_blue[0], gpio.OUT)
        # gpio.setup(self.led_red[0], gpio.OUT)
        print 'initialized'

    def get_green_state(self):
        return self.led_green[STATE]

    def get_blue_state(self):
        return self.led_blue[STATE]

    def get_red_state(self):
        return self.led_red[STATE]

    def set_green_state(self, state):
        previous_state = self.get_green_state()
        self.led_green = (self.led_green[PIN], state, self.led_green[COLOR])
        if state is not previous_state:
            self.update([self.led_green])

    def set_blue_state(self, state):
        previous_state = self.get_blue_state()
        self.led_blue = (self.led_blue[PIN], state, self.led_blue[COLOR])
        if state is not previous_state:
            self.update([self.led_blue])

    def set_red_state(self, state):
        previous_state = self.get_red_state()
        self.led_red = (self.led_red[PIN], state, self.led_red[COLOR])
        if state is not previous_state:
            self.update([self.led_red])

    def turn_off(self):
        self.active = False
        for light in self.lights:
            print 'Turned off ' + light[COLOR]
            # gpio.output(light[PIN], False)

    def turn_on(self):
        self.active = True
        self.update(self.lights)

    def force_on(self, value):
        self.force_on = value

    def monitor_crashed(self):
        self.set_green_state(False)
        self.set_blue_state(False)
        self.set_red_state(True)

    def update(self, lights_to_update):
        if self.active or self.force_on:
            for light in lights_to_update:
                print light[COLOR], 'state changed'
                # gpio.output(light[PIN], light[STATE])
