## Term project start

# keyEventsDemo.py
#
# keyPressed, keyReleased
# with ctrl and shift

from Tkinter import *

def eventInfo(eventName, char, keysym, ctrl, shift):
    # helper function to create a string with the event's info
    # also, prints the string for debug info
    msg = eventName + ": "
    msg += "(ctrl=" + str(ctrl) + ")"
    msg += "(shift=" + str(shift) + ")"
    msg += "(char=" + char + ")"
    msg += "(keysym=" + keysym + ")"
    print msg
    return msg

def ignoreKey(event):
    # Helper function to return the key from the given event
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)

def timerFired(canvas):
    delta = 1
    if len(canvas.data.pressedDirections) != 0:
        for direction in canvas.data.pressedDirections:
            if direction == "Left":
                canvas.data.left -= delta
            if direction == "Right":
                canvas.data.left += delta
            if direction == "Up":
                canvas.data.top -= delta
            if direction == "Down":
                canvas.data.top += delta
    redrawAll(canvas)
    delay = 3
    if "s" in canvas.data.pressedLetters:
        delay = 1
    canvas.after(delay, timerFired, canvas)
    

def keyPressed(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data.info = eventInfo("keyPressed", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        # it's an alphabetic (A-Za-z)
        if (event.keysym not in canvas.data.pressedLetters):
            canvas.data.pressedLetters.append(event.keysym)
    directions = ["Left", "Right", "Up", "Down"]
    if (event.keysym in directions):
        if event.keysym not in canvas.data.pressedDirections:
            canvas.data.pressedDirections.append(event.keysym)
    redrawAll(canvas)    

def keyReleased(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data.info = eventInfo("keyReleased", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        # it's an alphabetic (A-Za-z)
        if (event.keysym in canvas.data.pressedLetters):
            canvas.data.pressedLetters.remove(event.keysym)
    directions = ["Left", "Right", "Up", "Down"]
    if (event.keysym in directions):
        if event.keysym in canvas.data.pressedDirections:
            canvas.data.pressedDirections.remove(event.keysym)
    redrawAll(canvas)    

def redrawAll(canvas):
    canvas.delete(ALL)
    canvas.create_rectangle(0, 0, canvas.data.width, canvas.data.height,
                            fill = "green")
    # Draw the pressedLetters
    font = ("Arial", 16, "bold")
    msg = "Pressed Letters: " + str([x for x in canvas.data.pressedLetters])
    canvas.create_text(400, 125, text=msg, font=font)
    # Draw the stupid circle
    left, top, r = canvas.data.left, canvas.data.top, canvas.data.radius
    canvas.create_oval(left, top, left + r, top + r, fill="black")
    # Draw the event info message
    font = ("Arial", 16, "bold")
    info = canvas.data.info
    canvas.create_text(400, 50, text=info, font=font)

def deltaDraw(canvas):
    delta

def init(canvas):
    canvas.data.info = "Key Events Demo"
    canvas.data.pressedLetters = [ ]
    canvas.data.pressedDirections = [ ]
    (canvas.data.left, canvas.data.top,
     canvas.data.radius) = (100, 100, 50)
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    width = 800
    height = 8000
    canvas = Canvas(root, width= width, height= height)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width = width
    canvas.data.height = height
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    root.bind("<KeyPress>", keyPressed)
    root.bind("<KeyRelease>", keyReleased)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()