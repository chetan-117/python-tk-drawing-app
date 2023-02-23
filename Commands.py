# for handling objects of goto command
class GoToCommand:
    def __init__(self, x, y, w=1, color='black'):
        self.x = x
        self.y = y
        self.width = w
        self.color = color

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

    # every command class must have its own str method. it is tricky to save the commands in a xml file because
    # the commands here are of classes, and they can not just be converted into a xml file. so we are writing a
    # str method that will be called everytime we are converting our command into string and storing in the xml
    # file. only one argument is needed here because every command will have its own str method.
    def __str__(self):
        # e.g:- <Command x="10" y="30" width="22.1" color="green">GoTo</Command>
        return '<Command x="' + str(self.x) + '" y="' + str(self.y) + '" width="' + str(
            self.width) + '" color="' + self.color + '">GoTo</Command>'
        # so experimentally, It has been found that it is working very fine.
        # Good Work. Now do the work for the remaining commands.


# for managing circle command
class CircleCommand:
    def __init__(self, r, w=1, c='black'):
        self.radius = r
        self.width = w
        self.color = c

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)

    def __str__(self):
        # e.g:-- <Command radius="3" width="2" color="orange">Circle</Command>
        return '<Command radius="' + str(self.radius) + '" width="' + str(
            self.width) + '" color="' + self.color + '">Circle</Command>'


# for handling begin fill command
class BeginFillCommand:
    def __init__(self, c='black'):
        self.color = c

    def draw(self, turtle):
        turtle.color(self.color)
        turtle.begin_fill()

    def __str__(self):
        # e.g:-- <Command color="blue">BeginFill</Command>
        return '<Command color="' + self.color + '">BeginFill</Command>'


class EndFillCommand:
    def __init__(self):
        # this is just a placeholder object meaning NULL value.
        pass

    def draw(self, turtle):
        turtle.end_fill()

    def __str__(self):
        return '<Command>EndFill</Command>'


class PenUpCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.penup()

    def __str__(self):
        return '<Command>PenUp</Command>'


class PenDownCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.pendown()

    def __str__(self):
        return '<Command>PenDown</Command>'
