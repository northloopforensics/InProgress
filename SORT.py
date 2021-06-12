#python3

import PySimpleGUI as sg
from nudenet import NudeClassifier
from nudenet import NudeDetector
import os
import shutil
import random
import datetime


#print = sg.Print   

splash = ["Welcome ICAC, hero!!!", "Thanks for EVERYTHING you do!!! Let's get the bad guys!", "Welcome back, rockstar!!! Ready to keep some people safe?",
          "I'm fired up! Let's investigate!", "Seen too much already today? Take a break. Otherwise, let's get through this fast.",
          "I hope you are having a great day, hero! Let's get to work!"]
welcome = random.choice(splash)

now = datetime.datetime.now()
then = datetime.datetime.now()

def run_fast_scandir(dir, ext):
    
    subfolders, files = [], []

    
    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)

        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)
    
    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files
        

def detect_parts():
    
    subfolders, files = run_fast_scandir(d, [".jpg", ".bmp", ".jpeg", ".jfif", ".png"])
    detector = NudeDetector()
    for f in files:
        parts = detector.detect(f)
        result_list = []
        
        femaleface = any(d['label'] == 'FACE_F' for d in parts)  ##true or false for body part presence in image
        if values['FFACE'] and femaleface == True:              ##creates relationship between checkbox element and body part
            print(f, 'Female Face')
            shutil.copy(f, values['OUTPUT'])
        maleface = any(d['label'] == 'FACE_M' for d in parts)    
        if values['MFACE'] and maleface == True:
            print(f, "Male Face")
            shutil.copy(f, values['OUTPUT'])
        anus = any(d['label'] == 'EXPOSED_ANUS' for d in parts)        
        if values['ANUS'] and anus == True:
            print(f, "Exposed Anus")
            shutil.copy(f, values['OUTPUT'])
        covbelly = any(d['label'] == 'COVERED_BELLY' for d in parts)    
        if values['CBELLY'] and covbelly == True:
           print(f, "Covered Belly")
           shutil.copy(f, values['OUTPUT'])
        exbelly = any(d['label'] == 'EXPOSED_BELLY' for d in parts)   
        if values['EBELLY'] and exbelly == True:
           print(f, "Exposed Belly")
           shutil.copy(f, values['OUTPUT'])
        covbutt = any(d['label'] == 'COVERED_BUTTOCKS' for d in parts)    
        if values['CBUTT'] and covbutt == True:
            print(f, "Covered Buttocks")
            shutil.copy(f, values['OUTPUT'])
        exbutt = any(d['label'] == 'EXPOSED_BUTTOCKS' for d in parts)    
        if values['EBUTT'] and exbutt == True:
            print(f, "Exposed Buttocks")
            shutil.copy(f, values['OUTPUT'])
        covfeet = any(d['label'] == 'COVERED_FEET' for d in parts)    
        if values['CFEET'] and covfeet == True:
            print(f, "Covered Feet")
            shutil.copy(f, values['OUTPUT'])
        exfeet = any(d['label'] == 'EXPOSED_FEET' for d in parts)    
        if values['EFEET'] and exfeet == True:
            print(f, "Exposed Feet")
            shutil.copy(f, values['OUTPUT'])
        covchestF = any(d['label'] == 'COVERED_BREAST_F' for d in parts)    
        if values['FCCHEST'] and covchestF == True:
            print(f, "Female Chest Covered")
            shutil.copy(f, values['OUTPUT'])
        exchestF = any(d['label'] == 'EXPOSED_BREAST_F' for d in parts)    
        if values['FECHEST'] and exchestF == True:
            print(f, "Female Chest Exposed")
            shutil.copy(f, values['OUTPUT'])
        exchestM = any(d['label'] == 'EXPOSED_BREAST_M' for d in parts)    
        if values['MCHEST'] and exchestM == True:
            print(f, "Male Chest Exposed")
            shutil.copy(f, values['OUTPUT'])
        CovgenF = any(d['label'] == 'COVERED_GENITALIA_F' for d in parts)    
        if values['FCGEN'] and CovgenF == True:
            print(f, "Female Genitalia Covered")
            shutil.copy(f, values['OUTPUT'])
        exgenF = any(d['label'] == 'EXPOSED_GENITALIA_F' for d in parts)    
        if values['FEGEN'] and exgenF == True:
            print(f, "Female Genitalia Exposed")
            shutil.copy(f, values['OUTPUT'])
        exgenM = any(d['label'] == 'EXPOSED_GENITALIA_M' for d in parts)    
        if values['MGEN'] and exgenM == True:
            print(f, "Male Genitalia Exposed")
            shutil.copy(f, values['OUTPUT'])
    


sg.theme('Reddit')   # Add a touch of color
# All the stuff inside your window.

popup = [sg.popup(welcome, font=("Arial", 13), no_titlebar=True, grab_anywhere=True)]

bodyimg = b"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"

    
col_MALE = [    [sg.Text('Male Anatomy Options:')],
                [sg.Checkbox('Male Face', key='MFACE')],
                [sg.Checkbox('Male Chest Exposed', key='MCHEST')],
                [sg.Checkbox('Male Genitalia Exposed', key='MGEN')],
                ]
                
                



col_FEMALE = [  [sg.Text('Female Anatomy Options:')],
                [sg.Checkbox('Female Face', key='FFACE')],
                [sg.Checkbox('Female Chest Covered', key='FCCHEST')],
                [sg.Checkbox('Female Chest Exposed', key='FECHEST')],
                [sg.Checkbox('Female Genitalia Covered', key='FCGEN')],
                [sg.Checkbox('Female Genitalia Exposed', key='FEGEN')]
                ]


col_ANY =   [   [sg.Text('Universal Anatomy Options:')],
                [sg.Checkbox('Exposed Anus', key='ANUS')],
                [sg.Checkbox('Covered Belly', key='CBELLY')],
                [sg.Checkbox('Exposed Belly', key='EBELLY')],
                [sg.Checkbox('Covered Buttocks', key='CBUTT')],
                [sg.Checkbox('Exposed Buttocks', key='EBUTT')],
                [sg.Checkbox('Covered Feet', key='CFEET')],
                [sg.Checkbox('Exposed Feet', key='EFEET')]
                ]
                


layout = [  [sg.Text('S.O.R.T.', size=(20, 1), font=('Impact', 50, 'bold underline'))],
            [sg.Text("SELECTIVE ORGAN RETRIEVAL TOOL", font=('Impact', 11,), text_color='dark gray')],
            
            [sg.Text('Source Directory:'),sg.Input(key='SOURCE'), sg.FolderBrowse(key='SOURCE')],
            [sg.Text('Output Directory:'),sg.Input(key='OUTPUT'), sg.FolderBrowse(key='OUTPUT')],
            [sg.Text('_'*110)],
            [sg.Text('SELECT ANATOMY TO BE RETURNED FROM SEARCH:')],
            [sg.Text('Will return images containing any of the checked criteria.')],
            [sg.Column(col_ANY), sg.VerticalSeparator(pad=None), sg.Column(col_FEMALE), sg.VerticalSeparator(pad=None), sg.Column(col_MALE), sg.VerticalSeparator(pad=None), sg.Image(".\\BODY.png")],
            [sg.Output(size=(107,7), key='-OUTPUT')],
            [sg.Text('_'*110)],
            
            [sg.Button('Ok'), sg.Button('Exit'), sg.Text(' '*165), sg.Button('?', key='HELP')]]

# Create the Window
window = sg.Window('S.O.R.T.', layout, no_titlebar=False, grab_anywhere=False)
# Event Loop to process "events" and get the "values" of the inputs



while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'HELP':
        popup = [sg.popup("S.O.R.T. - Selective Organ Retrieval Tool", '\n',
                          "The tool makes use of machine learning to attempt to identify body parts deemed relevant to an investigation.",
                          "This automated review process is NOT perfect. Please review the results.",
                          "The workflow of the program:", 
                          "1. Select Source Directory containing images to be searched.", 
                          "2. Select an Output Directory for the report and copies of retrieved images.",
                          "3. Select anatomical features for the search.", 
                          "4. Select 'Ok'", 
                          "5. Review the returns. Remember it's AI. The results will not be perfect.", '\n',
                          "If the tool is not operating, don't feel bad. I don't read directions either. Go review the ReadMe to troubleshoot your issue (likely you started the tool for the first time without an internet connection).",
                          "\n", "No warranty or guarantee is offered with the use of this tool.",
                          "                                     ©2021 North Loop Consulting, LLC", no_titlebar=True, background_color="Light Gray", grab_anywhere=True)]
    elif event == 'Ok':
        print("SORTing started...")
        d = (values['SOURCE'])
        detect_parts()
        print("*****SORTing Complete*****", '\n', then.strftime("%Y-%m-%d %H:%M:%S"), '\n', "File results stored to " + (values['OUTPUT']))
        sg.PopupAnimated(None)
        window.refresh()
    window.refresh()
    
        
        

window.close()
