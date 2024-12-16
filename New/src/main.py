# main.py
import PySimpleGUI as sg
import edgedetection
import imagesegmentation
import sharpening
import smoothing

def main(): #Main Display
    layout = [
        [sg.Text('Welcome to Image Processing Suite', size=(30, 1), justification='center')],
        [sg.Button('Edge Detection')],
        [sg.Button('Image Segmentation')],
        [sg.Button('Image Sharpening')],
        [sg.Button('Image Smoothing')],
        [sg.Button('Exit')]
    ]

    window = sg.Window('Main Menu', layout, finalize=True)

    while True:
        event, _ = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Edge Detection':
            window.hide()
            edgedetection.main()
            window.un_hide()

        if event == 'Image Segmentation':
            window.hide()
            imagesegmentation.main()
            window.un_hide()

        if event == 'Image Sharpening':
            window.hide()
            sharpening.main()
            window.un_hide()

        if event == 'Image Smoothing':
            window.hide()
            smoothing.main()
            window.un_hide()

    window.close()

if __name__ == '__main__':
    main()
