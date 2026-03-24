## originally created by Aki
# Pypi: https://pypi.org/user/Mommy_Aki/
# Github: https://github.com/Mommy-Aki/Mommy-Aki

## forked by <person>
# <links here>

# Imports
try: # checks if all imports are avaliable, sadly no Pathlib thanks to the shit that is pyinstaller
    #from pathlib import Path
    from os import remove, listdir
    from shutil import rmtree
    from tkinter import Tk, Frame, Button, Label, END, Checkbutton, Entry, IntVar
    from easygui import diropenbox
    from time import sleep as Wait
    
except: # installs all required modules
    from subprocess import run
        
    run("pip install --upgrade easygui", shell = True)

    #from pathlib import Path
    from os import remove, listdir
    from shutil import rmtree
    from tkinter import Tk, Frame, Button, Label, END, Checkbutton, Entry, IntVar
    from easygui import diropenbox
    from time import sleep as Wait

        
    
class Config: # Configs that are changed then applied
    NukeRoute = None
    PrintInConsole = True
    DeleteFolder = False

class UI: # Everything UI related
    def SetupUI(Title:str = "Nuke the Luke", Size:list = [500, 500]): # Sets the UI up
            
        # Main Window
        UI.Window = Tk()
        UI.Window.title(Title)
        UI.MainFrame = Frame(master = UI.Window, width = Size[0], height = Size[1])
        UI.MainFrame.bind(func = Scripts.UI.Reset)
            
        # Variables
        UI.DeleteBox = IntVar()
            
        # Buttons
        UI.ConfirmationButton = Button(master = UI.MainFrame, width = 40, height = 2, text = "Nuke Folder", bg = "#AAFFAA", command = Scripts.UI.Confirm)
        UI.SearchPath = Button(master = UI.MainFrame, width = 5, height = 1, text = "...", command = Scripts.Main.FindPath)
        UI.DeleteFolder = Checkbutton(master = UI.MainFrame, variable = UI.DeleteBox)

        # Text Boxes
        UI.PathInput = Entry(master = UI.MainFrame, width = 45)
        UI.DeleteExplaination = Label(master = UI.MainFrame, width = 20, height = 1, text = "Delete folder after nuke: ")
        UI.PathInput.insert(0, "N/A")
        
        # Packing / Placing Elements
        UI.MainFrame.pack()
        UI.DeleteFolder.place(x = 310, y = 350)
        UI.DeleteExplaination.place(x = 170, y = 350)
        UI.PathInput.place(x = 115 , y = 300)
        UI.SearchPath.place(x = 425, y = 295)
        UI.ConfirmationButton.place(x = 115, y = 380)
    
    def RunUI(): # Runs the UI
        try:
            UI.Window.mainloop()
        except:
            exit()

class Scripts: # Scripts for the function
    class UI: # Scripts for UI elements
            


        def Confirm(): # confirms decision
            UI.ConfirmationButton.configure(text="Confirm?", command = Scripts.Main.DeleteFiles) # asks user if they want to nuke folder
                
            if UI.PathInput.get().strip() == "": # ensures something is put inside the path box
                UI.PathInput.delete(0, END)
                UI.PathInput.insert(0,"N/A")
                    
            Config.NukeRoute = UI.PathInput.get() # sets current path to nuke
            Config.DeleteFolder = True if UI.DeleteBox.get() == 1 else False # sets if the folder should be deleted afterward
            #print(f"Confirm Started, got '{Config.NukeRoute}'") # logs
        
        def Reset(): # resets to initial view [cancels confirmation]
            UI.ConfirmationButton.configure(text="Nuke Folder", command = Scripts.UI.Confirm) # resets message on button

            # resets values to prevent them stacking
            Config.NukeRoute = None
            Config.DeleteFolder = False
                
            #print("Reset") # logs
    
    class Main: # Scrpts fo rain functions
        def FindPath(): # sets path to a specififc point
            
            NewDir = diropenbox() # opens menu to open a directory
            #print(NewDir) # Logs the route found
                
            UI.PathInput.delete(0,END) # removes data from path
                    
            if NewDir != None: # checks if use has actually chosen a path
                UI.PathInput.insert(0, NewDir)
            else:
                UI.PathInput.insert(0, "N/A")
                
            Scripts.UI.Reset() # resets confirmation
            
        def DeleteFiles(Overide:str = None): # actua nuking for the folder
            #print(f"Running...") # Log to tell if this subroutine works
            
            if Overide == None: # allows the path to be chnaged if provided
                LocalPath = Config.NukeRoute
            else:
                LocalPath = Overide

            if LocalPath == None: # stops functinality if no path is supplied
                print("No Path")
                Scripts.UI.Reset()
                return None
            
            FoundPath = LocalPath # gets / creates the abslute path to ensure it is going to the correct area
            
            try:
                Files = listdir(FoundPath) # lists all children is parent path provided
            except:
                Scripts.UI.Reset()
                return None

            for item in Files: # does this for every child

                PathToObj = f"{FoundPath}\\{item}" # creates a path that goes to the child
                

                # Fuck you pyinstaller, had to ruin one of my fav modules 'Pathlib', go fuck yurself
                

                try:
                    listdir(PathToObj) # checks if it can be listed [aka if its a folder]
                    # Here for some reaosn gets the program to rash but i have no clue, future Ak[i] will figure this shit out

                except: # is a file
                    print(f"Removing '{PathToObj}' ..", end="")
                    try: # attempts to delete / remove the child
                        remove(PathToObj)
                    except Exception as Error:
                        print(f".[x]: {Error}")
                    else:
                        print(f".[/]")
                        
                else: # is a folder
                    if listdir(PathToObj).__len__() > 0: # checks if the child has content, and runs the script to clear the content of the child
                        print(f"Removing '{PathToObj}' ...[...]")
                        Scripts.Main.DeleteFiles(PathToObj)
                        print(f"'{PathToObj}' cleared successfully...!")
                
                    print(f"Removing '{PathToObj}' ..", end="")
                    try: # tries to remove the empty folder
                        rmtree(PathToObj)
                    except Exception as Error:
                        print(f".[x]: {Error}")
                    else:
                        print(f".[/]")

                """if PathToObj.is_dir(): # reruns script with the child directory if the child is a folder
                    if listdir(PathToObj).__len__() > 0: # checks if the child has content, and runs the script to clear the content of the child
                        print(f"Removing '{PathToObj}' ...[...]")
                        Scripts.Main.DeleteFiles(PathToObj)
                        print(f"'{PathToObj}' cleared successfully...!")
                
                    print(f"Removing '{PathToObj}' ..", end="")
                    try: # tries to remove the empty folder
                        rmtree(PathToObj)
                    except Exception as Error:
                        print(f".[x]: {Error}")
                    else:
                        print(f".[/]")

                else: # deletes the child assuming its a file
                    print(f"Removing '{PathToObj}' ..", end="")
                    try: # attempts to delete / remove the child
                        remove(PathToObj)
                    except Exception as Error:
                        print(f".[x]: {Error}")
                    else:
                        print(f".[/]")"""
                
            if Config.DeleteFolder: # attempts to delete parent folder when the user asks for the folder to be removed
                try:
                    rmtree(FoundPath)
                except:
                    pass
                    

            Wait(.9)
            UI.Window.quit() # stops the UI from staying active
            



def Main(): # Main sequence of events
    if __name__ == "__main__":
        UI.SetupUI() # sets UI up
        UI.RunUI() # Runs Ui until it stops
        Wait(.7)
        print(f"Finshed Nuking the Folder: {Config.NukeRoute}...[/]" if Config.NukeRoute != None else "", end="" if Config.NukeRoute == None else "\n") # logs that process has finished
        exit() # leaves program




Main()
