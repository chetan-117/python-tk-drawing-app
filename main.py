import tkinter
from app import DrawingApplication


def main():
    root = tkinter.Tk()
    drawingApp = DrawingApplication(root)

    drawingApp.mainloop()

    # when this mainloop terminate, we have exited from the app and printing the success line at the end.
    print('Program Execution Completed. I hope you liked it. \
            \nIf you found any bug, then feel free to send me a mail at chetan_11914067@nitkkr.ac.in')


if __name__ == '__main__':
    main()
