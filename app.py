import tkinter
import turtle
from tkinter import filedialog
from tkinter import colorchooser
import xml
from xml.dom import minidom

from Commands import *


class DrawingApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        # this list is going to be helpful to hold the commands
        self.graphicsCommands = []

    def buildWindow(self):
        """ this is the function that will be called at the instant when there is an instance is formed of this class.
            This function will contain and define all the functions and widgets that will be useful for the application
        """
        # giving a title to our application.
        self.master.title('Draw')

        # then creating a menu bar. We are making a nested menu here.
        bar = tkinter.Menu(self.master)
        file_menu = tkinter.Menu(bar, tearoff=0)

        # creating the command functions of the options available in the menu box.
        # event to start a new fresh window
        def newWindow():
            """ when this happens then we need to clear the screen, making the graphicCommand variable to None and so
                on
            """
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0, 0)
            theTurtle.pendown()
            screen.update()
            screen.listen()
            self.graphicsCommands.clear()

        # using the add_command method to bind this command to the file_menu.
        file_menu.add_command(label='New', command=newWindow)

        # now suppose that you also want to add the commands through an XML file into our program, then there is a
        # parse function. we passed the name of that file using the path returning function as
        # 'filedialog.askopenfilename'
        def parse(filename):
            xml_doc = xml.dom.minidom.parse(filename)
            # as we know that the xml files comprises the tag-names and we can access this file using the tags
            # of the file. this is the parent tag.
            graphics_commands_element = xml_doc.getElementsByTagName('GraphicsCommands')[0]

            # this is the first child tag. From this, we are getting the next tag data.
            graphicsCommands = graphics_commands_element.getElementsByTagName('Command')

            # here we are assuming that our xml file has the data in the required format.
            # the data is present in the tags, so the for loop will work very fine.
            for commandElement in graphicsCommands:
                # print(type(commandElement))
                command = commandElement.firstChild.data.strip()
                attr = commandElement.attributes

                # now we have got the command that is the tag name of the child tag, and we have also got the
                # attributes of that tag name. then we should check the commands and depending upon that we can take
                # appropriate action. to get the attribute value, use the syntax like this:
                # attr_object[attr_name].value
                if command == 'GoTo':
                    x = float(attr['x'].value)
                    y = float(attr['y'].value)
                    width = float(attr['width'].value)
                    color = attr['color'].value.strip()
                    # passing the data into our command classes for various commands.
                    cmd = GoToCommand(x, y, width, color)

                elif command == 'Circle':
                    r = float(attr['radius'].value)
                    w = float(attr['width'].value)
                    c = attr['color'].value.strip()
                    cmd = CircleCommand(r, w, c)

                elif command == 'BeginFill':
                    color = attr['color'].value.strip()
                    cmd = BeginFillCommand(color)

                elif command == 'EndFill':
                    cmd = EndFillCommand()

                elif command == 'PenDown':
                    cmd = PenDownCommand()

                elif command == 'PenUp':
                    cmd = PenUpCommand()

                # raising the error if we no option from the above choices appear.
                else:
                    raise RuntimeError('Unknown Command : ' + command)

                # appending the command received we need to append these commands in the object's commands list.
                self.graphicsCommands.append(cmd)

        # this is the actual function that we will bind with the file_menu, and it contains the function to process
        # that file using the parse method.
        def loadFile():
            # using the method as askopenfilename() that will return the path of the selected file.
            filename = tkinter.filedialog.askopenfilename(initialdir='/', title='Select a Graphics File')

            # after this, we need to get a new window to put those contents of the file there.
            newWindow()  # it will reset everything.

            # clearing the object's graphics commands sequence.
            self.graphicsCommands.clear()

            # now calling the parse method and the graphicsCommands will be filled with the graphics Commands taken
            # from the file.
            parse(filename)

            # now with the help of the Polymorphism, I will use the draw method in all those commands.
            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)

            # manually updating the screen
            screen.update()

        # now adding this loadFile method to our file_menu.
        file_menu.add_command(label='Load File', command=loadFile)

        # this is a function for the adding to the file. I don't understand its exact meaning now but let's see what
        # is this.
        def addToFile():
            """ add to file means that we were drawing something in the application, and then we load a file and all
            the commands of that file are also drawn on the screen canvas. We can do this by first taking the turtle
            to the origin or the center and changing its color to the black because in the program its color may have
            been changed several times. Then we parse the file in our parse() function and all the commands of the
            file will be appended in the graphicsCommands method of the object, and now we have all the command, and
            then we will draw them. Thus, we added a file to our current drawing.
            """
            filename = tkinter.filedialog.askopenfilename(initialdir='/', title='Select a Graphics File')

            # I don't know what this theTurtle keyword is. But let's use it as it is asking me to.
            theTurtle.penup()
            theTurtle.goto(0, 0)
            theTurtle.pendown()
            theTurtle.pencolor('#000000')
            theTurtle.fillcolor('#000000')
            cmd = PenUpCommand()
            self.graphicsCommands.append(cmd)
            cmd = GoToCommand(0, 0, 1, '#000000')
            self.graphicsCommands.append(cmd)
            cmd = PenDownCommand()
            self.graphicsCommands.append(cmd)

            # again updating manually
            screen.update()

            # parsing the file with the filename as the argument.
            parse(filename)

            # draw using polymorphism.
            for cmd in self.graphicsCommands:
                cmd.draw(theTurtle)

            # again updating the screen because it may be possible that the changes are not reflected early, and we
            # have to force it to reflect them
            screen.update()

        # one more command to be added in the file_menu object.
        file_menu.add_command(label='Load Into...', command=addToFile)

        # Now If we want to save the file, then we should save it in the XML file format, This format is mainly
        # useful for the storage of the data. for this purpose, we will form our own write method that will be called
        # to put all those commands in an XML file.
        def write(filename):
            # we have passed the filename in it as the argument from the saveFile function.
            # opening the file first in the write mode.
            file = open(filename, 'w')

            # writing the first line in the XML file to tell that it is the XML file.
            file.write('<?xml version="1.0" encoding="utf-8" standalone="no" ?>\n')

            # then making the Graphics Command tag.
            file.write('<GraphicsCommands>\n')

            # writing the other commands from our command list.
            for cmd in self.graphicsCommands:
                file.write('    ' + str(cmd) + '\n')

            # creating the ending tag at the end.
            file.write('</GraphicsCommands>\n')

            # then closing the file.
            file.close()

        # now the actual save function.
        def saveFile():
            filename = tkinter.filedialog.asksaveasfilename(title='Save Picture As')
            # calling the write function to write the commands in the filename.
            write(filename)

        # putting this command in the file_menu too.
        file_menu.add_command(label='Save As...', command=saveFile)

        # also adding the EXIT command if we wish to quit the application.
        file_menu.add_command(label='Exit', command=self.master.destroy)
        # now putting this file_menu in our main menu in the cascade manner.
        bar.add_cascade(label='File', menu=file_menu)

        # configuring the root window to also show the menubar.
        self.master.config(menu=bar)

        """ the work of the menu widget and its commands has been completed. So the another task is to
            put all the widgets and their commands on the tkinter root window
        """
        canvas = tkinter.Canvas(self, width=600, height=600)
        canvas.pack(side=tkinter.LEFT)

        # now creating a RawTurtle that is just a turtle with no canvas, and we have to provide a canvas for it to
        # draw on.
        theTurtle = turtle.RawTurtle(canvas)

        # changing the default shape of the turtle from arrow to a circle.
        theTurtle.shape('circle')

        # getting the screen object to perform some more tasks.
        screen = theTurtle.getscreen()

        # we are passing it to not the screen update its content when we do something until the update method has
        # been called. this helps so stable our program. Actually, I don't have any idea what this is doing here. I
        # just wrote it done and nothing else special.
        screen.tracer(0)

        # now creating a frame on the right side of the screen where all the buttons, label etc. would be placed.
        # it should fill in all the available space on the right side.
        sideBar = tkinter.Frame(self, padx=5, pady=5)
        sideBar.pack(fill=tkinter.BOTH, side=tkinter.RIGHT)

        # we are making a point label where we can change the width of the turtle lines.
        pointLabel = tkinter.Label(sideBar, text='Width')
        pointLabel.pack()

        # we need to create variables to be able to use the get() and the set() method. Initially, we must put it to 1.
        # It is to be converted into string because the Entry widget requires the string.
        widthSize = tkinter.StringVar()
        widthEntry = tkinter.Entry(sideBar, textvariable=widthSize)
        widthEntry.pack()

        # setting an initial value to our string variable.
        widthSize.set(str(1))

        # it seems to me that the x,y coordinates should be set using the mouse.
        # the radius of the circle should be set by us , So I am creating a radiusSize variable too.
        radiusLabel = tkinter.Label(sideBar, text='Radius')
        radiusLabel.pack()
        radiusSize = tkinter.StringVar()
        # creating the entry box for the radius size widget.
        radiusEntry = tkinter.Entry(sideBar, textvariable=radiusSize)
        radiusSize.set(str(10))
        radiusEntry.pack()

        # So right now, two entry buttons have been created, and we can set the values in it that can further be used
        # in our program. now creating other buttons to handle the circle and do other stuff of the turtle.
        def circleHandler():
            # making the use of the graphicsCommands list to store this command too.
            cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

            # I really don't understand the effect of these lines, but they help to put the focus back to our program
            # and also to listen to the key press.
            screen.update()
            screen.listen()

        # creating a circle button on the sideBar and putting the circleHandler command in it.
        circleButton = tkinter.Button(sideBar, text='Draw Circle', command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)

        # now it is time to write the codes for selecting the colors for our application.
        # this below line means that every kind of color is allowed in our canvas.
        screen.colormode(255)
        penLabel = tkinter.Label(sideBar, text='Pen Color')
        penLabel.pack()
        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sideBar, textvariable=penColor)
        penEntry.pack()

        # setting the default value to black to it.
        penColor.set('#000000')

        # this will provide the user the ability to pick his own color from the color chooser widget
        def getPenColor():
            color = tkinter.colorchooser.askcolor()
            if color is not None:
                penColor.set(str(color)[-9:-2])

        # now creating a button to use and actually set the penColor of the turtle.
        penColorButton = tkinter.Button(sideBar, text='Pick Pen Color', command=getPenColor)
        penColorButton.pack(fill=tkinter.BOTH)

        # now creating another label to start the color fillings.
        fillLabel = tkinter.Label(sideBar, text="Fill Color")
        fillLabel.pack()
        fillColor = tkinter.StringVar()
        fillEntry = tkinter.Entry(sideBar, textvariable=fillColor)
        fillEntry.pack()

        # setting the default value of color.
        fillColor.set('#000000')

        def getFillColor():
            color = tkinter.colorchooser.askcolor()
            if color is not None:
                fillColor.set(str(color)[-9:-2])

        # creating the button for fill color now.
        fillColorButton = tkinter.Button(sideBar, text='Pick Fill Color', command=getFillColor)
        fillColorButton.pack()

        # so till now we have selected the color that should be filled but right now the function to actually fill
        # the color are not there.
        def beginFillHandler():
            cmd = BeginFillCommand(fillColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        # creating a button for this begin fill command.
        beginFillButton = tkinter.Button(sideBar, text='Begin Fill', command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH)

        # similarly, there should be an end-fill handler.
        def endFillHandler():
            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        endFillButton = tkinter.Button(sideBar, text='End Fill', command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH)

        # creating a label too to tell whether the button is pressed or not and the pen is up or not.
        penLabel = tkinter.Label(sideBar, text='Pen Is Down')
        penLabel.pack()

        # similarly, the penup and pendown also don't have any arguments, so they can be directly created and passed
        # as the command to their respective button.
        def penUpHandler():
            cmd = PenUpCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            # also changing the label of the pencolor.
            penLabel.configure(text='Pen Is Up')

        penUpButton = tkinter.Button(sideBar, text='Pen Up', command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH)

        # there comes the pen down method that will also change the pen label to pen down when it is pressed.
        def penDownHandler():
            cmd = PenDownCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            # changing the label now.
            penLabel.configure(text='Pen is Down')

        # creating the pen down button.
        penDownButton = tkinter.Button(sideBar, text='Pen Down', command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)

        def clickHandler(x, y):
            cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        # I am typing the event listener of onclick to the function that I have designed for it
        # the onclick will maintain the coordinates where I have clicked on
        # this is how we tie the clickHandler with the mouse clicks.
        screen.onclick(clickHandler)

        def dragHandler(x, y):
            cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        # drag event
        theTurtle.ondrag(dragHandler)

        # the undo function should remove the last command from the graphics Commands list and then redrawing the
        # entire picture again.
        def undoHandler():
            """ We first need to ensure that our commands list is not empty"""
            if len(self.graphicsCommands) > 0:
                # then removing the last command and taking the turtle to home and reset everything.
                self.graphicsCommands.pop()
                theTurtle.clear()
                theTurtle.penup()
                theTurtle.goto(0, 0)
                theTurtle.pendown()

                # now drawing the entire image again.
                for cmd in self.graphicsCommands:
                    cmd.draw(theTurtle)

                # manually updating the screen and again start listening for further events
                screen.update()
                screen.listen()

        # now the function of undo that we made just now, We are binding it with a keypress.
        screen.onkeypress(undoHandler, 'u')
        screen.listen()

# this marks the code for a drawing application, now making the main function that will create a root window and this
# root window will be passed to our drawing application class and that will create all the widgets and the frames and
# other events.
