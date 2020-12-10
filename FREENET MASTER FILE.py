#! python3
# Freenet Parser Master File

from __future__ import print_function
import glob
import argparse

_author_ = ['Copyright 2020 North Loop Consulting']
_copy_ = ['(C) 2020']
_description_ = ("---Rabbit-Hole: A Freenet Parser v. 0.1---" 
                 " To run the tool, enter the volume letter (ex. 'C') containing the Freenet installation.  "
                 "Then enter the report output location (ex. filepath\\report.txt).  " 
                    "An example might be: rabbithole.exe -v C 'F:\\Forensic Reports\\freenet_report.txt'.  "
                    "This tool looks for data in the default installation path: '...\\Username\\AppData\\Local\\Freenet' directory."
                 )

parser = argparse.ArgumentParser(
    description=_description_,
    epilog="{}".format(
        ", ".join(_author_), _copy_))


#Add positional arguments
parser.add_argument("INPUT_FOLDER", help="Path to the input folder")
parser.add_argument("OUTPUT_FILE", help="Path to the output file")

# Optional Arguments
parser.add_argument("-v", "--verbose", help="Report will include additional data beyond basic node and download activity")
                    

#Parsing and using the arguments

args = parser.parse_args()

input_folder = args.INPUT_FOLDER
output_file = args.OUTPUT_FILE






#TODO Add file output

#Function parses the Target Node ID and IP usage
def node():
    node_directory = input_folder + (":\\Users\\*\\AppData\\Local\\Freenet\\node-[0-9]*")
    for Nodefile in glob.glob(node_directory):
        file = open(Nodefile, "r")
        lines = file.readlines()
        file.close()
    print("Source File:  ", Nodefile, '\n')
    #Pull the Location ID and IP usage information
    for line in lines:
        line = line.strip()                                          #strips the empty double space btw output lines
        line = line.split("=", 1)
        if line[0] == 'location':                                    #target ID
            print('Target Node Location ID:', line[1])
        elif line[0] == 'physical.udp':                              #target IPs - use this for browser examination
            ipList = line[1]
            ipList = ipList.split(";")
            print('\n''Freenet Network/IP Use:', ("\n"'\t\t\t'.join(ipList)))

            #TODO Figure out formatting of the output
           
print('\n\n',"****** Target Node Identifiers - 'Freenet\\node-*' ******",'\n\n')
node()

#Function parses recent download file
def downloadlistfile():
    DList_directory = input_folder + (":\\Users\\*\\AppData\\Local\\Freenet\\completed.list.downloads")
    for DList in glob.glob(DList_directory):
        file = open(DList, 'r')
        lines = file.readlines()
        file.close()
    print("Source File:  ", DList, '\n')
    for line in lines:
        line = line.strip()
        print(line)
    file_length = len(lines)
    if file_length == 0:
        print('--- No Data Found in Target File --- Data Clears as a Normal Function of Freenet ---')

print('\n\n',"****** Recent download list stored in - \\Freenet\\completed.list.downloads ******", '\n\n')
downloadlistfile()

    
#Function list filenames stored in Freenet download directory    
def downloadfolder():
    DL_directory = input_folder + (":\\Users\\*\\AppData\\Local\\Freenet\\downloads\\*")
    for DFolder in glob.glob(DL_directory):
        print(DFolder)

print('\n\n',"****** Downloaded files stored in directory - \\Freenet\\downloads ******", '\n\n')
downloadfolder()


#Function parses peer-lists
def peerList():
    PEER_directory = input_folder + (":\\Users\\*\\AppData\\Local\\Freenet\\openpeers-[0-9]*.bak")
    for PList in glob.glob(PEER_directory):
        file = open(PList, "r")
        lines = file.readlines()
        file.close()
    print("Source File:  ", PList, '\n')
    #Pull the Location ID and IP usage information
    for line in lines:
        line = line.strip()
        line = line.split("=", 1)
        if line[0] == 'location':
            print('Peer Node Location ID: ', line[1])
        elif line[0] == 'physical.udp':
            print('Peer IP Address/es: ', line[1])
        elif line[0] == 'metadata.peersLocation':
            print('Other Peers of Peer Node (Location IDs): ')
            locationList = line[1]
            locationList = locationList.split(";")
            for a,b,c in zip(locationList[::3],locationList[1::3],locationList[2::3]):   #prints to 3 columns
                print('{:<30}{:<30}{:<}'.format(a,b,c))
            
        elif line[0] == 'End':
            print('\n\n')
                    
print('\n',"****** Peer ID (1 Hop) - Peer of Peer IDs (2 Hops) - Peer IP Address ******", '\n\n')
peerList()
