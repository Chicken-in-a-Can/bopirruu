import tkinter as tk
from tkinter import ttk
import os
import random
import time
import requests

ip = "10.5.32.1"

def getPackageList(search):
    packageList = []
    address = f"http://{ip}/bopirruu.php?query={search}"
    # address = "http://" + ip + "/bopirruu.php?query=" + search
    string = requests.get(address).text
    return string.split(',')[0:-1]

root = tk.Tk()
root.title("Bopirru User Interface")

root.geometry("800x400")

tabControl = ttk.Notebook(root)
homeTab = ttk.Frame(tabControl)
tabControl.add(homeTab, text = "Home")

#textFormatting
featuredTitle = ttk.Label(homeTab, text = "Featured Packages:", font=("Times",24))
featuredTitle.grid(column = 0, row = 0, padx = 10, pady = 10, sticky = "W")

spacing = ttk.Label(homeTab, text = " "*10)
spacing.grid(column = 1, row = 0, sticky = "W")

searchLabel = ttk.Label(homeTab, text = "Search Packages:", font = ("Times", 12))
searchLabel.grid(column = 2, row = 0, sticky = "W", padx = 10, pady = 10)

def openPackagePage(event):
    packageScreen = tk.Tk()
    packageScreen.title(searchBar.get())
    packageScreen.geometry("800x400")
 
    infoAddress = "http://" + ip + "/bopirruu.php?getinfo=" + searchBar.get()
    fileText = requests.get(infoAddress).text
    
    arr = fileText.split("<br />\n")
    if len(arr) > 4:
        for i in range(4, len(arr)):
            arr[3] = arr[3] + "  " + arr[i]
    nameLabel = ttk.Label(packageScreen, text = "Package Name:", font = ("Times", 12))
    nameVLabel = ttk.Label(packageScreen, text = "\t" + arr[0], font = ("Times", 12))
    versionLabel = ttk.Label(packageScreen, text = "Version Number:", font = ("Times", 12))
    versionVLabel = ttk.Label(packageScreen, text = "\t" + arr[1], font = ("Times", 12))
    architectureLabel = ttk.Label(packageScreen, text = "Architecture:", font = ("Times", 12))
    architectureVLabel = ttk.Label(packageScreen, text = "\t" + arr[2], font = ("Times", 12))
    descriptionLabel = ttk.Label(packageScreen, text = "Package Description:", font = ("Times", 12))
    descriptionVLabel = ttk.Label(packageScreen, text = "\t" + arr[3], font = ("Times", 12))
    
    nameLabel.grid(column = 0, row = 1, sticky = "W", padx = 10, pady = 5)
    nameVLabel.grid(column = 0, row = 2, sticky = "W", padx = 10, pady = 2)
    versionLabel.grid(column = 0, row = 3, sticky = "W", padx = 10, pady = 5)
    versionVLabel.grid(column = 0, row = 4, sticky = "W", padx = 10, pady = 2)
    architectureLabel.grid(column = 0, row = 5, sticky = "W", padx = 10, pady = 5)
    architectureVLabel.grid(column = 0, row = 6, sticky = "W", padx = 10, pady = 2)
    descriptionLabel.grid(column = 0, row = 7, sticky = "W", padx = 10, pady = 5)
    descriptionVLabel.grid(column = 0, row = 8, sticky = "W", padx = 10, pady = 2)
    
    
    def installCommand():
        progressBar = ttk.Progressbar(packageScreen, orient = "horizontal", mode = "indeterminate", length = 250)
        progressBar.grid(column = 0, row = 10, sticky = "W", padx = 10, pady = 10)
        installButton['text'] = "Installing..."
        installButton['state'] = "disabled"
        #ADD INSTALL COMMAND HERE, use packageAddress as package file location
        progressBar.start(25)
        
        #REPLACE NEXT LINE WITH EVENT DETECTOR FOR END OF INSTALL
        root.after(7500, progressBar.stop)
        
        installButton['text'] = "Installed"
        
    packageAddressPHPAddress = f"http://{ip}/bopirruu.php?getpath={searchBar.get()}"
    # packageAddressPHPAddress = "http://" + ip + "/bopirruu.php?getpath="+searchBar.get()
    packageAddress = "http://" + ip + "/" + requests.get(packageAddressPHPAddress).text
    
    installButton = ttk.Button(packageScreen, text = "Install", command = installCommand)
    installButton.grid(column = 0, row = 9, sticky = "W", pady = 10, padx = 10)
    
    exitButton = ttk.Button(packageScreen, text = "Exit", command = packageScreen.destroy)
    exitButton.grid(column = 0, row = 0, sticky = "W", padx = 10, pady = 10)
    
    def report():
        print("reported jk lmao") #Add report functionality later
    reportButton = ttk.Button(packageScreen, text = "Report", command = report)
    reportButton.grid(column = 1, row = 0, sticky = "W", padx = 10, pady = 10)
    
    
    packageScreen.mainloop()
#searchBar


currentPackageString = tk.StringVar()
packageList = getPackageList(currentPackageString.get())
def updatePackageList(*args):
    packageList = getPackageList(currentPackageString.get())
    searchBar['value'] = packageList
currentPackageString.trace("w", updatePackageList)


searchBar = ttk.Combobox(homeTab, values = packageList, height = 10, textvariable = currentPackageString)
searchBar.grid(column = 3, row = 0, sticky = "E", pady = 10, padx = 10)
searchBar.bind("<<ComboboxSelected>>", openPackagePage)

#assemble
tabControl.grid(column = 1, row = 0, padx = 50, pady = 10)
root.mainloop()