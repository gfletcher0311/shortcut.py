#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: Gavin Fletcher
Date: 10/21/23
Version: 1.0
'''
#Import useful package(s)
import subprocess
import os
import time

def createLink(linkPlace, fileName):
    found_files = [] # List of all files incase duplicates are found
    output =subprocess.run(f"find / -name \"{fileName}\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if (output.stdout.decode() == ""): # Means no such file exists
        print("No such file exists\n\n Returning to main menu")
        time.sleep(3)
        return                                                  
    results = output.stdout.decode().split("\n") # Plits entries on new lines
    results.pop() # Removes the last newline character so you dont have a blank line
    for result in results:
        found_files.append(result) #Append all files (including files with same name in different locations)

    for file in found_files:
        print("File found: ",file) # Print the current file from the list of foudn files
        user_choice = input("Was this the correct file (y/n) 'q' to quit: ")
        if (user_choice.lower() == "y"):
            link = subprocess.check_output(f"ln -s \"{file}\" \"{ linkPlace}\"", shell=True, stderr=subprocess.DEVNULL).decode() # Runs a command that takes the file path and links it to the desktop
            print("Link successfully made. Returning to main menu!")
            time.sleep(3) # Wait 3 seconds before returning to menu
            return

        elif (user_choice.lower() == "n"): # Continue loop to get the next file in the list of files
            continue
        elif (user_choice.lower() == "q"):
            return # Instantly break out of loop and return to menu
        
    return
                        
def removeLink(linkPlace, filename):
    files = os.listdir(linkPlace) # returns a list of directories in the specific dir.
    if filename not in files: # Not found, so we can break out of loop
        print("File to rm not found, returning to menu. . . \n")
        time.sleep(3)
        return
    user_choice = input(f"Remove file: {filename}? (y/n) >> ") # Confirmation from user to remove link
    if user_choice.lower() == "n":
        print("Returning to menu. . . \n")
        time.sleep(3)
        return
    else:
        os.remove(f"{linkPlace}/{filename}") # uses os module to remove file
        print("Link successfully removed. . . Returning to menu")
        time.sleep(3)
        subprocess.call("clear", shell=True)

    

def linkReport():
    print("Your current directory is: ",os.environ["HOME"]) # prints the working directory using the os module
    print("Number of links is: ",len(os.listdir(os.environ["HOME"]+"/Desktop")))
    for link in os.listdir(os.environ["HOME"]+"/Desktop"): # Prints each link that is found in the desktop directory
        filePath = subprocess.run(f"readlink \"{os.environ['HOME']+'/Desktop'}/{link}\"", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        print(f"{link} --> ",filePath.stdout.decode()) # coding the output to point to the original link
    input("Press enter to return to main menu: \n")

def main():
    subprocess.call("clear", shell=True)
    user_input = '' # Define user input so loop can run
    linkPlace = os.environ["HOME"]+"/Desktop" # Uses the OS module to get the home path and adds /Desktop
    while (user_input.lower() != "quit"):
        print("Current Working Directory:", os.environ["HOME"]+"\n\n") # prints the current working directory
        print("Options available for Shortcuts:\n\n") 
        print("(1.) Create a shortcut in your home directory.\n(2.) Remove a shortcut from your home directory.\n(3.) Run shortcut report\n\nPlease enter a number (1-3) or type 'q' to quit.")
        user_input = input("Enter command: ")
        if (user_input.lower() == "q" or user_input.lower() == "quit"): # Quits if the user types q or quit
            subprocess.call("clear", shell=True) # Clear terminal before printing
            print("Application successfully closed")
            break
        
        elif(user_input == "1"):
            subprocess.call("clear", shell=True) # Clear terminal
            fileName = input("Enter the name of your file: ") # get name of  file to make link
            createLink(linkPlace, fileName) # Call the createlink() function

        elif (user_input == "2"):
            subprocess.call("clear", shell=True)
            fileName = input("Enter the name of your file you wish to remove ")
            removeLink(linkPlace, fileName) # Cll the remove link function
        
        elif (user_input == "3"):
            linkReport() # Calls the link_report which gives info about linksm ade in desktop
        else:
            subprocess.call("clear", shell=True) # Clear the rrminal and reprompt them with the same prompt

if __name__ == "__main__":
    main()
