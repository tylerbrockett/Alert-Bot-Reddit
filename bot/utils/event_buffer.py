from helpers.colorize import colorize

color = 0
event = 1


class EventBuffer:
    def __init__(self, max_size):
        self.events = [('red', '2222')]
        self.MAX_SIZE = max_size

    def append(self, e):
        if len(self.events) < self.MAX_SIZE:
            self.events.append(e)
        else:
            self.events = self.events[1:]
            self.events.append(e)

    def to_string(self):
        result = ''
        rev = reversed(self.events)
        for e in rev:
            result += e[event]
        return result

    def to_color_string(self):
        result = ''
        for e in self.events:
            result += colorize(e[color], e[event])
            result += "\n"
        return result

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []
