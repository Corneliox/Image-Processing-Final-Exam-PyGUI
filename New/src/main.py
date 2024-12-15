import PySimpleGUI as sg
import os
import edgedetection
import imagesegmentation
import sharpening
import smoothing

def main():
    # Layout utama untuk menu
    layout = [
        [sg.Text('Main Menu', size=(20, 1), justification='center', font=('Helvetica', 25))],
        [sg.Button('Edge Detection', size=(20, 2))],
        [sg.Button('Image Segmentation', size=(20, 2))],
        [sg.Button('Sharpening', size=(20, 2))],
        [sg.Button('Smoothing', size=(20, 2))],
        [sg.Button('Exit', size=(20, 2))]
    ]

    window = sg.Window('Main Menu', layout, element_justification='center')

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break

        # Navigation to other modules
        if event == 'Edge Detection':
            window.hide()
            edgedetection.main()
            window.un_hide()

        elif event == 'Image Segmentation':
            window.hide()
            imagesegmentation.main()
            window.un_hide()

        elif event == 'Sharpening':
            window.hide()
            sharpening.main()
            window.un_hide()

        elif event == 'Smoothing':
            window.hide()
            smoothing.main()
            window.un_hide()

    window.close()

if __name__ == "__main__":
    main()
