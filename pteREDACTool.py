#python3

#THINGS TO DO GO HERE - OMIT FIRST PAGE REDACTION ON DOCX AND PDF 

import PySimpleGUI as sg
import os
import sys
import datetime
import time
import glob2
import hashlib
import zipfile
from PIL import Image, ImageFilter
import io
import fitz
from distutils.dir_util import copy_tree
from nudenet import NudeClassifier
from nudenet import NudeDetector

#global image file extensions
ImageExts = (".JPG", ".JPEG", ".PNG", ".BMP", ".HEIC", ".HEIF", ".jpg", ".jpeg", ".jpe", ".jif",
            ".jfif", ".heif", ".heic", ".gif", ".png", ".bmp")
#global video file extensions
VideoExts = (".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".mp4", ".m4v", ".m4p", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd", ".mkv",
            ".ogg", ".webm", ".MPG", ".MP2", ".MPEG", ".MPE", ".MPV", ".MP4", ".M4V", ".M4P", ".AVI", ".WMV", ".MOV", ".QT", ".FLV", ".SWF",
            ".AVCHD", ".MKV", ".OGG", ".WEBM")



def make_report():
    savePath = (values['OUTPUT'])
    global org_stdout
    org_stdout = sys.stdout
    reportName = ("REDACTION REPORT")
    global completeName
    completeName = os.path.join(savePath, reportName+".txt")
    
    now = datetime.datetime.now()
    org_stdout = sys.stdout
    with open(completeName, 'w') as report:
        sys.stdout = report
        print("**********************     Redaction Report - pteREDACTool     **********************", '\n',
              "       _      ______ ___________  ___  _____ _____           _                  $ + ",'\n',                               
              "      | |     | ___ \  ___|  _  \/ _ \/  __ \_   _|         | |                   $... ",'\n',                              
              " _ __ | |_ ___| |_/ / |__ | | | / /_\ \ /  \/ | | ___   ___ | |                    $=Z$7777I. ",'\n',                        
              "|  _ \| __/ _ \    /|  __|| | | |  _  | |     | |/ _ \ / _ \| |               ,$   $ZZ77$77777777",'\n',                    
              "| |_) | ||  __/ |\ \| |___| |/ /| | | | \__/\ | | (_) | (_) | |             77$.   777$777777777... ",'\n',                 
              "| .__/ \__\___\_| \_\____/|___/ \_| |_/\____/ \_/\___/ \___/|_|           777$     7$7$$7I7777  ",'\n',                     
              "| |                                                                    $7$?$I     +7$77$77777+ ",'\n',                      
              "|_|                                                                  I77I7II       7$$77$77. ",'\n',                        
              "                                                           Z        77?.I7$7I      $77$77$77   ",'\n',                       
              "                                                         .DD       7. ~7. ,+7?     7$$7777777  ",'\n',                        
              "                                                         ONZ.      7      :7Z$?,Z$$77$777$77  ",'\n',                        
              "                                                          I?OZ$$=         . 78Z8$$?IZ77$77.  ",'\n',                          
              "                                                         $O?Z7$777$7,.... 7$Z8I$7+ZZ77$7   ",'\n',                           
              "                                                        7I$7$77$$777777$$$77I+:O$$Z$$$7    ",'\n',                           
              "                                                        ?777$7$7$7$7777777$77$ON8Z$$7$     ",'\n',                           
              "                                                       777$7$7777$$777777777777Z77$7$7     ",'\n',                          
              "                                                     +7II77I7777$77$$7777$777I7777$77+     ",'\n',                           
              "                                                      77I?II7.   .7$7. ..??$777$77$ 77     ",'\n',                           
              "                                                      7.                    .I7  ~7= 77     ",'\n',                          
              "                                                                             .7    7, ?.    ",'\n',                          
              "                                                                             I.      $$$7  ",'\n',                           
              "                                                                             .7      . .   ",'\n',                          
              "                                                                             $$$.          ",'\n', 
              "Redaction Performed On:  ", now.strftime("%Y-%m-%d %H:%M:%S"), '\n',
              "Redaction Performed By User:  ", os.getlogin(), '\n',
              "Source Directory:  ", values['SOURCE'], '\n',
              "Output Directory:  ", values['OUTPUT'], '\n',
              "User Settings:", '\n',
              "\t", "Redact Image Files - ", values['IMAGES'], '\t\t\t\t', "Redact Video Files - ", values['VIDEOS'], '\n',
              "\t", "Redact Based on Nudity Level - ", values['NUDITY'], '\t\t\t', "Redact Based on MD5 Hash - ", values['HASH'], '\n',
              "\t", "Redact Images from PDFs - ", values['PDF'], '\t\t\t', "Redact Images from DOCXs - ", values['DOCX'], '\n\n',
              "#######################  FILES REDACTED   #######################")
             
    sys.stdout = org_stdout  
       

def run_fast_scandir(dir, ext):    #iterates over target folder. recursive thru all contents. makes list files based on ext provided
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

def nudity_filter():        #FILTER BY NUDITY LEVEL AND REMOVE FILES
    classifier = NudeClassifier()
    allList = (classifier.classify(files,  batch_size=1))
    if (values['NUDITYLEVEL']) != 'Normal Filter':
        nudlev = float('.1')
    else:
        nudlev = float('.5')
    badfiles = {k:v for k,v in allList.items() if v['unsafe'] >= nudlev}
    removefiles = list(badfiles.keys())  #FILES TO REMOVE
    
    for f in removefiles: ##DELETION OF BAD FILES
        sg.Print("Removing file based on nudity content: ", f)
        window.refresh()
        with open(completeName, 'a') as report:
            sys.stdout = report
            print(f)
            sys.stdout = org_stdout
        os.remove(f)

def copy_folder():   #COPIES THE SOURCE FOLDER
    try:
        copy_tree(values['SOURCE'], values['OUTPUT'])
        for root, dirs, files in os.walk(values['OUTPUT']):
            
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)
    except Exception:
        sg.Print('Error Copying- verify user access to files and folders')
        pass            

def image_delete():            #delete image files by file extension
    dir_name = (values['OUTPUT'])
    ImageItems = os.walk(dir_name)
    ImageExts = (".JPG", ".JPEG", ".PNG", ".BMP", ".HEIC", ".HEIF", ".jpg", ".jpeg", ".jpe", ".jif",
                 ".jfif", ".heif", ".heic", ".gif", ".png", ".bmp")

    for root, dirs, files in ImageItems:
        for file in files:
            if file.endswith(ImageExts):
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(os.path.join(root,file))
                sys.stdout = org_stdout
                sg.Print("Redacting Image File: ", os.path.join(root,file))
                window.refresh()
                os.remove(os.path.join(root, file))
                

def video_delete():             #delete video files by file extension
    dir_name = (values['OUTPUT'])
    VideoItems = os.walk(dir_name)
    VideoExts = (".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".mp4", ".m4v", ".m4p", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd", ".mkv",
            ".ogg", ".webm", ".MPG", ".MP2", ".MPEG", ".MPE", ".MPV", ".MP4", ".M4V", ".M4P", ".AVI", ".WMV", ".MOV", ".QT", ".FLV", ".SWF",
            ".AVCHD", ".MKV", ".OGG", ".WEBM")

    for root, dirs, files in VideoItems:
        for file in files:
            if file.endswith(VideoExts):
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(os.path.join(root,file))
                sys.stdout = org_stdout
                sg.Print("Redacting Video File: ", os.path.join(root,file))
                window.refresh()
                os.remove(os.path.join(root, file))

def md5_remove():
    name = (values['OUTPUT'])

    with open(values['HASHLIST'], 'r') as f:   #opens file cont hash list
        HLvariableCase = f.read().splitlines()

    remove = [x.lower() for x in HLvariableCase]  #hashes moved to lower case to work with code below    

    for root, subfolder, files in os.walk(name):
        for items in files:
            filename = os.path.join(root, items)
            with open(filename, 'rb') as inputfile:
                data = inputfile.read()
            hash_list = ([filename, hashlib.md5(data).hexdigest()])
            inputfile.close()
            #print(hash_list)

            if hash_list[1] in remove:  #Compare file hashes with hashes in list file.
                remove_list = (hash_list[0])
                sg.Print("Removing File Based on MD5: ", remove_list)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(remove_list)
                sys.stdout = org_stdout
                os.remove(remove_list)


def redact_PDF():
    dir_name = (values['OUTPUT'])
    for root, subfolder, files in os.walk(dir_name):
        for items in files:
            try:
            #print(items)
                filename = os.path.join(root, items)
            #print(filename)
                if filename.endswith(".pdf"):     #Walks the directories and finds the PDFs
        
                    sg.Print("Redacting Images from PDF: ", filename)
                    window.refresh()
                    doc = fitz.open(filename)    #Opens PDF file

                    if values['FIRSTPAGE'] == True:
                        for pageNumber, page in enumerate(doc.pages(1, None)):  #get page numbers for pdf and skips 1st page 
                            for imgNumber, img in enumerate(page.getImageList(), start=1):#get image numbers for each page
                                #print(img[7])         
                                box = page.getImageBbox(img[7])  #img[7] provides the image name
        
                            # colors for redaction box
                                yellow = (1, 1, 0)
                                black = (0, 0, 0)
        
                                for line in box:    #Loop allows redaction for pages with more than 1 image
                                    #print(line)
                                    page.addRedactAnnot(box, "REDACTED",align=fitz.TEXT_ALIGN_CENTER, fill=black, text_color=yellow)

                            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)   #applies redactions per page, prevents image modification and forces replacement

                    else:
                        for pageNumber, page in enumerate(doc.pages()):  #get page numbers for pdf and skips 1st page 
                            for imgNumber, img in enumerate(page.getImageList(), start=1):#get image numbers for each page
                                #print(img[7])         
                                box = page.getImageBbox(img[7])  #img[7] provides the image name
        
                            # colors for redaction box
                                yellow = (1, 1, 0)
                                black = (0, 0, 0)
        
                                for line in box:    #Loop allows redaction for pages with more than 1 image
                                    #print(line)
                                    page.addRedactAnnot(box, "REDACTED",align=fitz.TEXT_ALIGN_CENTER, fill=black, text_color=yellow)

                            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE)   #applies redactions per page, prevents image modification and forces replacement
                    with open(completeName, 'a') as report:
                        sys.stdout = report
                        print(filename)
                    sys.stdout = org_stdout  
                    redactedFile = os.path.join(root, "REDACTED-" + items)
                doc.save(redactedFile, garbage=3, deflate=True)  #saves the new redacted PDF with amended file name, deflate removes spare areas
            except ValueError:
                sg.Print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                sys.stdout = org_stdout
                pass
            except Exception:
                sg.Print('There was an error redacting ' + filename)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print('There was an error redacting ' + filename + ". Please review its status in the output folder.")
                sys.stdout = org_stdout
              
            

#breaking on other office files like pptx & xlsx
def redact_imagesDOCX():
    dir_name = (values['OUTPUT'])
    blur = ImageFilter.GaussianBlur(150)
    for root, subfolder, files in os.walk(dir_name):
        for items in files:
            filename = os.path.join(root, items)
            #print(filename)
            if filename.endswith(".docx"):
                sg.Print("Redacting Images from DOCX: ", filename)
                window.refresh()
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print(filename)
                sys.stdout = org_stdout
                
                outfile = os.path.join(root, 'REDACTED-' + items)
                #print(outfile)
                
                with zipfile.ZipFile(filename) as inzip:
                    with zipfile.ZipFile(outfile, "w") as outzip:
                        for info in inzip.infolist():
                            name = info.filename
                                #print(info)
                            content = inzip.read(info)
                            if name.endswith((".png", ".jpeg", ".bmp", ".gif")):
                                fmt = name.split(".")[-1]
                                img = Image.open(io.BytesIO(content))
                                img = img.convert().filter(blur)
                                outb = io.BytesIO()
                                img.save(outb, fmt)
                                content = outb.getvalue()
                                info.file_size = len(content)
                                info.CRC = zipfile.crc32(content)
                            outzip.writestr(info, content)

    

sg.theme('DarkGrey13')   # Add a touch of color
# All the stuff inside your window.
popup =  [sg.popup("This tool is intended to assist, not replace, a human being in producing documents and files for use in legal proceedings.",
                   "The user must click 'OK' to acknowledge any productions made with this tool should be manually reviewed.",
                   "Use this tool at your own risk.  No warranty or guarantee is offered in its use.", no_titlebar=True, grab_anywhere=True)]

layout = [  [sg.Text('pteREDACTool', size=(20, 1), font=('Arial Black', 20, 'bold underline'))],
            [sg.Text('Files in Source will be copied to Output. Unwanted files will then be removed from Output directory:')],
            [sg.Text('Source Directory:'),sg.Input(key='SOURCE'), sg.FolderBrowse(key='SOURCE')],
            [sg.Text('Output Directory:'),sg.Input(key='OUTPUT'), sg.FolderBrowse(key='OUTPUT')],
            [sg.Text('_'*100)],
            [sg.Text('SELECT ELEMENTS TO DELETE FROM OUTPUT DIRECTORY:')],
            [sg.Text('Delete Files by Image or Video File Extensions:')],
            [sg.Text(' '*5), sg.Checkbox('.jpg, .jpeg, .jpe, .jif, .jfif, .heif, .heic, .gif, .png, .bmp', default=False, disabled=False, key='IMAGES')],
            [sg.Text(' '*5), sg.Checkbox('.mpg,.mp2, .mpeg, .mpe, .mpv, .mp4, .m4v, .m4p, .avi, .wmv, .mov, .qt, .flv, .swf, .avchd, .mkv,.ogg, .webm', default=False, disabled=False, key='VIDEOS')],
            [sg.Text('_'*100)],
            [sg.Checkbox('Files Based on Nudity Level   |', default=False, key='NUDITY'),sg.Text('Select Nudity Filter Level: '), sg.Combo(['Normal Filter', 'Aggresive Filter'], key='NUDITYLEVEL')],
            [sg.Text('_'*100)],
            [sg.Checkbox('Files Based on MD5   |', default=False, key='HASH'), sg.Text("MD5 Hash List (.txt)"), sg.Input(key='HASHLIST'), sg.FileBrowse(key='HASHLIST')],
            [sg.Text('_'*100)],
            [sg.Text('REDACT IMAGES INSIDE DOCUMENTS:')],
            [sg.Checkbox('Redact Images from PDF   |', default=False, key='PDF'), sg.Checkbox('Do NOT Redact 1st Page of PDFs', default=False, key='FIRSTPAGE')],
            [sg.Checkbox('Redact Images from .DOCXs', default=False, key='DOCX')],
            [sg.Text('_'*100)],
            [sg.Button('Ok'), sg.Button('Exit'), sg.Text(' '*150), sg.Button('?', key='HELP')]]



# Create the Window
window = sg.Window('pteREDACTool - Image/Video Redaction Tool', layout, no_titlebar=True, alpha_channel=.92, grab_anywhere=True)
# Event Loop to process "events" and get the "values" of the inputs


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    elif event == 'HELP':
        popup = [sg.popup("pteREDACTool is a redaction tool designed to help those working on CSAM investigations..", '\n',
                          "The workflow of the program is basic.", 
                          "1. Copy evidence to new location.", 
                          "2. Remove files based on file extension, nudity level, or MD5 hash.", 
                          "3. Create Report.", '\n', no_titlebar=True, grab_anywhere=True)]
    elif event == 'Ok':
        
        if (values['SOURCE']) != 0:   #copies
            for i in range(100000):
                sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='COPYING...', font='Impact 16', text_color="Light Blue", background_color='Grey', transparent_color='Grey', time_between_frames=120)
            copy_folder()
            make_report()
            sg.PopupAnimated(None)
            if (values['IMAGES']) == True:  #deletes images in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING IMAGE FILES...', font='Impact 16', text_color="Orange", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                image_delete()
                window.refresh()
            if (values['VIDEOS']) == True: #deletes videos in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING VIDEO FILES...', font='Impact 16', text_color="Orange",background_color='Grey', transparent_color='Grey', time_between_frames=120)
                video_delete()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['NUDITY']) == True: #deletes based on nudity level in copy
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING NUDITY, THIS TAKES SOME TIME...', font='Impact 16', text_color="Orange", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                subfolders, files = run_fast_scandir(values['OUTPUT'], ImageExts)
                run_fast_scandir(values['OUTPUT'], ImageExts)
                nudity_filter()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['HASH']) == True: #deletes base on a list of provided md5 hashes
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING BASED ON MD5...', font='Impact 16', text_color="Orange", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                md5_remove()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['PDF']) == True:
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING PDF CONTENT...', font='Impact 16', text_color="Orange", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                redact_PDF()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            if (values['DOCX']) == True:
                for i in range(100000):
                    sg.PopupAnimated(sg.DEFAULT_BASE64_LOADING_GIF, message='REDACTING DOCUMENT CONTENT...', font='Impact 16', text_color="Orange", background_color='Grey', transparent_color='Grey', time_between_frames=120)
                redact_imagesDOCX()
                sg.PopupAnimated(None)      # close all Animated Popups
                window.refresh()
            sg.PopupAnimated(None)      # close all Animated Popups
        pop = [sg.popup("Looks like we're done. Here is the 'REDACTION REPORT.txt' now saved in your output directory.", no_titlebar=True, grab_anywhere=True)]
        time.sleep(1)
        os.startfile(completeName)
        window.refresh()

window.close()
