# From CMU 15-112 at https://www.cs.cmu.edu/~112/notes/cmu_112_graphics.py
from cmu_112_graphics import *
import time

def appStarted(app):
    app.timerDelay = 5000
    app.timerStarted = False
    app.timerFinished = False
    app.isPaused = False
    app.timeLeft = ""
    app.waitingForInput = True
    while app.timeLeft == None or (not app.timeLeft.isdigit()):
        app.timeLeft = app.getUserInput("Enter quiz time in minutes: ")
    app.waitingForInput = False
    app.timeLeft = app.originalTime = 1000 * (int(app.timeLeft) * 60)  # milliseconds
    
    
    # start button
    app.buttonTopLeftX = app.width // 2 - app.width // 5
    app.buttonTopLeftY = int(app.height * 0.7)
    app.buttonBottomRightX = app.width // 2 + app.width // 5
    app.buttonBottomRightY = app.buttonTopLeftY + (app.height // 5)

    # Pause button
    app.pauseButtonTopLeftX = 0
    app.pauseButtonTopLeftY = 0
    app.pauseButtonBottomRightX = app.width // 12
    app.pauseButtonBottomRightY = app.height // 12
    

    # Reset button
    #app.resetButtonTopLeftX = 0
    #app.resetButtonTopLeftY = app.pauseButtonBottomRightY
    #app.resetButtonBottomRightX = app.pauseButtonBottomRightX
    #app.resetButtonBottomRightY = 2 * app.pauseButtonBottomRightY



def timerFired(app):
    if app.waitingForInput: return
    if not app.isPaused and app.timerStarted and app.timeLeft >= app.timerDelay:
        app.timeLeft -= app.timerDelay
    if isinstance(app.timeLeft, int) and app.timeLeft <= 0:
        app.timerFinished = True

def makeTimeString(n):  # n is time.time()
    fullTimeString = time.ctime(n)
    twentyFourWithSeconds = fullTimeString.split()[3]
    hours, minutes, seconds = twentyFourWithSeconds.split(':')
    updatedHours = (int(hours)) % 12
    if updatedHours == 0: updatedHours = 12
    return f'{updatedHours}:{minutes}'

def insideStartButton(app, x, y):
    if x < app.buttonTopLeftX:
        return False
    if x > app.buttonBottomRightX:
        return False
    if y < app.buttonTopLeftY:
        return False
    if y > app.buttonBottomRightY:
        return False
    return True

def insidePauseButton(app, x, y):
    if x < app.pauseButtonTopLeftX:
        return False
    if x > app.pauseButtonBottomRightX:
        return False
    if y < app.pauseButtonTopLeftY:
        return False
    if y > app.pauseButtonBottomRightY:
        return False
    return True

'''
def insideResetButton(app, x, y):
    if x < app.resetButtonTopLeftX:
        return False
    if x > app.resetButtonBottomRightX:
        return False
    if y < app.resetButtonTopLeftY:
        return False
    if y > app.resetButtonBottomRightY:
        return False
    return True
'''

def mousePressed(app, event):
    if app.waitingForInput: return
    if not app.timerStarted:
        app.timerStarted = True
        app.startTime = int(time.time())
        app.endTime = app.startTime + (app.timeLeft) // 1000

    elif not app.timerFinished: #  and insidePauseButton(app, event.x, event.y):
        app.isPaused = not app.isPaused
        print(f'App paused: {app.isPaused}')
    #elif not app.timerFinished and insideResetButton(app, event.x, event.y):
    #    app.timeLeft = app.originalTime
    #    app.timerStarted = False
    #    print('Timer reset')


def keyPressed(app, event):
    if app.waitingForInput: return
    if event.key == 'r':
        appStarted(app)
    elif event.key == 'e':
        app.timeLeft = 1


def drawCountdown(app, canvas):
    leftTextX = app.width // 8
    rightTextX = app.width * 2 // 3
    topTextY = app.height // 3
    bottomTextY = int((2/3) * app.height)
    timeOffset = app.height // 8

    startEndFont = "Arial 60 bold"
    # Start and end time
    canvas.create_text(leftTextX, topTextY, text = "Start time: ", 
                       font = startEndFont, fill = 'black')
    canvas.create_text(leftTextX, topTextY + timeOffset, 
                       text = makeTimeString(app.startTime),
                       font = startEndFont, fill = 'black')
    
    canvas.create_text(leftTextX, bottomTextY, text = "End time: ", 
                       font = startEndFont, fill = 'black')
    canvas.create_text(leftTextX, bottomTextY + timeOffset, 
                       text = makeTimeString(app.endTime), 
                       font = startEndFont, fill = 'black')
    
    # Time remaining
    remainingSeconds = (app.timeLeft // 1000) 
    secondsLeft = (((remainingSeconds) % 60)) 
    if secondsLeft < 10:
        secondsLeft = '0' + str(secondsLeft)
    minutesLeft = remainingSeconds // 60
    if minutesLeft < 10:
        minutesLeft = '0' + str(minutesLeft)
    timeString = f'{minutesLeft}:{secondsLeft}'
    canvas.create_text(rightTextX, topTextY, text = "Time remaining: ", 
                       font = "Arial 100 bold", fill = 'black')
    canvas.create_text(rightTextX, topTextY + 2 * timeOffset, text = timeString,
                       font = "Arial 200 bold", fill = 'black')

    drawExtraButtons(app, canvas)

def drawExtraButtons(app, canvas):
    buttonFont = 'Arial 25'

    canvas.create_rectangle(app.pauseButtonTopLeftX, app.pauseButtonTopLeftY,
                            app.pauseButtonBottomRightX, 
                            app.pauseButtonBottomRightY, outline = 'black')
    pauseX = (app.pauseButtonTopLeftX + app.pauseButtonBottomRightX) // 2
    pauseY = (app.pauseButtonTopLeftY + app.pauseButtonBottomRightY) // 2

    label = 'Unpause' if app.isPaused else 'Pause'
    canvas.create_text(pauseX, pauseY, text = label, font = buttonFont, 
                       fill = 'black')

    #canvas.create_rectangle(app.resetButtonTopLeftX, app.resetButtonTopLeftY,
    #                        app.resetButtonBottomRightX, 
    #                        app.resetButtonBottomRightY, outline = 'black')
    #resetX = (app.resetButtonTopLeftX + app.resetButtonBottomRightX) // 2
    #resetY = (app.resetButtonTopLeftY + app.resetButtonBottomRightY) // 2

    #canvas.create_text(resetX, resetY, text = 'Reset', font = buttonFont,
    #                   fill = 'black')
    


def drawFinished(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "00:00",
                       font = "Arial 100 bold", fill = 'black')

def drawBeginning(app, canvas):
    if isinstance(app.timeLeft, str): return
    timeInSeconds = (int(app.timeLeft)) // 1000
    timeInMinutes = timeInSeconds // 60
    canvas.create_text(app.width // 2, app.height // 2, 
                       text = f'{timeInMinutes}:00',
                       font = "Arial 60 bold", fill = 'black')

    canvas.create_rectangle(app.buttonTopLeftX, app.buttonTopLeftY, 
                            app.buttonBottomRightX, app.buttonBottomRightY, 
                            outline = 'black')
    canvas.create_text(app.width // 2, int(app.height * 0.8), text = "Begin",
                       font = "Arial 40 bold", fill='black')

def redrawAll(app, canvas):
    if app.waitingForInput: return
    if app.isPaused: canvas.create_rectangle(0, 0, app.width, app.height, fill='gray')
    if app.timerStarted and not app.timerFinished:
        drawCountdown(app, canvas)
    elif app.timerFinished:
        drawFinished(app, canvas)
    else:
        drawBeginning(app, canvas)

if __name__ == '__main__':
    runApp(width = 2000, height = 1000)