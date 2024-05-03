import os
from cmu_graphics import * # type: ignore
from utils import cities_alphabetical
import tkinter as tk
from tkinter import filedialog
import cv2
from tensorflow.keras.models import load_model # type: ignore

def imgToLabel(app, url):
    img = cv2.imread(url)   
    scaled_image = cv2.resize(img, (256, 256), 
                              interpolation=cv2.INTER_AREA)
    scaled_image = scaled_image.reshape((1, *scaled_image.shape))
    output = app.model.predict(scaled_image)[0]
    indexes = output.argsort()[-3:][::-1]
    probabilities = output[indexes]
    return indexes, probabilities


def onAppStart(app):
    app.state = 'menu'
    app.stuff = None
    app.menuSelection = 0
    app.loadSelection = 0
    app.cities = cities_alphabetical()
    app.model = load_model("cities_classifier.keras")
    app.imageUrl = ''
    app.x = 0
    app.y = 0

def onMousePress(app, x, y):
    if app.state == 'menu':
        if 160 <= x <= 440:
            if 211 <= y <= 290:
                app.state = 'load'
                app.menuSelection = 0
            elif 315 <= y <= 390:
                app.state = 'info'
                app.menuSelection = 1
            elif 410 <= y <= 490:
                app.menuSelection = 2
                exit()
    elif app.state == 'load':
        if 160 <= x <= 440:
            if 230 <= y <= 310:
                if fileSelection(app):
                    app.state = 'image'
            elif 390 <= y <= 460:
                app.state = 'menu'
                app.menuSelection = 0
                app.loadSelection = 0
    elif app.state == 'image':
        if 160 <= x <= 440 and 460 <= y <= 540:
            app.state = 'load'
            app.menuSelection = 0
            app.loadSelection = 0

def onKeyPress(app, key):
    if key == 'down':
        if app.state == 'menu':
            app.menuSelection = (app.menuSelection + 1) % 3
        elif app.state == 'load':
            app.loadSelection = (app.loadSelection + 1) % 2
    elif key == 'up':
        if app.state == 'menu':
            app.menuSelection = (app.menuSelection - 1) % 3
        elif app.state == 'load':
            app.loadSelection = (app.loadSelection - 1) % 2
    elif key == 'enter':    
        if app.state == 'menu':
            if app.menuSelection == 0:
                app.state = 'load'
            elif app.menuSelection == 1:
                app.state = 'info'
            else:
                exit()
        elif app.state == 'load':
            if app.loadSelection == 0:
                if fileSelection(app):
                    app.state = 'image'
            elif app.loadSelection == 1:
                app.state = 'menu'
                app.menuSelection = 0
                app.loadSelection = 0
        elif app.state == 'image':
            app.state = 'menu'
            app.menuSelection = 0
            app.loadSelection = 0
    elif key == 'escape':
        if app.state == 'menu':
            exit()
        elif app.state == 'load' or app.state == 'info':
            app.state = 'menu'
        elif app.state == 'image':
            app.state = 'load'


def fileSelection(app):
    root = tk.Tk()
    root.withdraw()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    file = filedialog.askopenfile(title='Select Image file', filetypes=[('Image Files', '*.jpeg *.jpg *.webp *.png')])
    if file is None:
        return False
    app.imageUrl = file.name
    app.stuff = imgToLabel(app, app.imageUrl)
    return True

def drawOptionsMenu(app):
    name = ["START","INFO","QUIT"]
    centerX = app.width / 2
    cellWidth = 280
    cellHeight = 80
    for i, _ in enumerate(name):
        centerY = 250 + i*100
        if i == app.menuSelection:
            drawRect(centerX, centerY, cellWidth + 15, cellHeight + 15, fill=None, border="skyblue",borderWidth=5, align='center')
            drawLabel(name[i], centerX, centerY, size=30, fill="skyblue", align="center", bold=True)  
        else:
            drawRect(centerX, centerY, cellWidth, cellHeight, fill=None, border="gray", borderWidth=3,align='center')
            drawLabel(name[i], centerX, centerY, size=25, fill="skyblue", align="center", bold=True)


def drawOptionsLoad(app):
    name = ["Load Image", "Back"]
    centerX = app.width / 2
    cellWidth = 280
    cellHeight = 80
    for i, _ in enumerate(name):
        centerY = 275 + i*150
        if i == app.loadSelection:
            drawRect(centerX, centerY, cellWidth + 15, cellHeight + 15, fill=None, border="skyblue",borderWidth=5, align='center')
            drawLabel(name[i], centerX, centerY, size=30, fill="skyblue", align="center", bold=True)  
        else:
            drawRect(centerX, centerY, cellWidth, cellHeight, fill=None, border="gray", borderWidth=3,align='center')
            drawLabel(name[i], centerX, centerY, size=25, fill="skyblue", align="center", bold=True)

def onMouseMove(app, x, y):
    if app.state == 'menu':
        if 160 <= x <= 440:
            if 211 <= y <= 290:
                app.menuSelection = 0
            elif 315 <= y <= 390:
                app.menuSelection = 1
            elif 410 <= y <= 490:
                app.menuSelection = 2

    elif app.state == 'load':
        if 160 <= x <= 440:
            if 230 <= y <= 310:
                app.loadSelection = 0
            elif 390 <= y <= 460:
                app.loadSelection = 1
        
def redrawAll(app): 
    if app.state == "menu":
        drawLabel("City Predictor", 300, 80, size=50,fill="steelblue",bold = True)
        drawOptionsMenu(app)
    elif app.state == "load":
        drawLabel("Load the Image", 300, 80, size=50,fill="steelblue",bold = True)
        drawOptionsLoad(app)
    elif app.state == "info":
        pass
    elif app.state == "image":
        # Draw prediction title
        drawLabel("Prediction", 300, 50, size=50, fill="steelblue", align="center",bold = True)

        # Draw the image
        drawImage(app.imageUrl, 150, 275, width=250, height=250, align='center')

        # Draw information labels

        # Get predicted cities and probabilities
        indexes, probs = app.stuff
        cities = [app.cities[i] for i in indexes]

        drawLabel("The image is from...", 450, 175, size=20, fill="black")
        drawLabel(f"{cities[0]} : {100*probs[0]:.3f}%", 450, 225, size=20, fill="black")
        
        # Draw top predicted city and probability
        count = -1
        drawLabel("It could also be from:", 450, 275, size=18)
        for i, city in enumerate(cities[1:]):
            if probs[i+1] >= 0.05:
                count+=1
                drawLabel(f"{i+1}. {cities[i+1]} : {100*probs[i+1]:.3f}%", 450, 325 + count*50, size=18)

        # Draw back button
        drawRect(300, 500, 280 + 15, 80 + 15, fill=None, border="skyblue",borderWidth=5, align='center')
        drawLabel("Back", 300, 500, size=30, fill="skyblue", align="center", bold=True)  
        # drawRect(300, 500, 280, 80, align='center', border='black', fill='yellow')
        # drawLabel("Back", 300, 500, size=25)


if __name__ == "__main__":
    runApp(600, 600)
