version = "1.0"
devmode = False

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from time import sleep as wait
import os, pickle
from tkinter import messagebox
from colorama import Fore as color
import colorama

# Global some variables because python sucks
global pixels

# Create the main window and set up colors
root = tk.Tk()
colorama.init(autoreset=True)

def update_img(img):
    # Create an ImageTk object to display the image
    img_tk = ImageTk.PhotoImage(img.resize((300, 300), resample=Image.NEAREST))
    # Update the image in the label
    label.config(image=img_tk)
    label.image = img_tk

def update_image(img):
    update_img(img)
    root.update()

def display_image(pixels: np.array, image_location: str, x=0, y=0):
    img = Image.open(image_location)
    pixels_img = np.array(img)
    if len(pixels_img[0, 0]) == 4:
        for i in range(max(x, 0), min(img.height + x, 30)):
            for j in range(max(y, 0), min(img.width + y, 30)):
                if pixels_img[i-x, j-y][3] != 0:
                    pixels[i, j] = [pixels_img[i-x, j-y][0], pixels_img[i-x, j-y][1], pixels_img[i-x, j-y][2]]
        return pixels
    else:
        for i in range(max(x, 0), min(img.height + x, 30)):
            for j in range(max(y, 0), min(img.width + y, 30)):
                pixels[i, j] = [pixels_img[i-x, j-y][0], pixels_img[i-x, j-y][1], pixels_img[i-x, j-y][2]]
        return pixels

# Frame variable
frame = 1

# Set up window
root.geometry("300x300")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"+{int(screen_width/2-150)}+{int(screen_height/2-150)}")
root.title(f"Minicraft {version}")
root.resizable(False, False)
root.iconbitmap("images/ico.ico")

# Set the row and column weights to 1
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the initial image
img = Image.new('RGB', (30, 30))
pixels = np.array(img)
pix = [[1, 1], [1, 2], [1, 3]]
for pixel in pix:
    pixels[pixel[0], pixel[1]] = [255, 255, 255]

# Create the image label
img_tk = ImageTk.PhotoImage(img.resize((300, 300), resample=Image.NEAREST))
label = tk.Label(root, image=img_tk)
label.grid(row=0, column=0, sticky="nsew")
label.pack()

# Tomcat spash screen
tomcatsplash_loadingbarcounter = 0
tomcatsplash_loadingbar = []

def create_image():
    img = Image.new('RGB', (30, 30))
    pixels = np.array(img)
    img = Image.fromarray(pixels)
    return pixels

if os.name == "nt" and __name__ == "__main__":
    os.system("cls")
print(f"{color.GREEN}Minicraft {version}\n{color.MAGENTA}Programmed by Tomcat\n{color.WHITE}Made for Cintill Development")

# Create the image
create_image()

# Bars
bar = [10, 10]
gamemode = "s"

# Loading bar
while not 29 in tomcatsplash_loadingbar:
    pixels = display_image(pixels, "images/splash.png")
    for pixel in tomcatsplash_loadingbar:
        pixels[24, pixel] = [255, 255, 255]
    if frame in list(range(1, 29)) and tomcatsplash_loadingbarcounter != 29:
        tomcatsplash_loadingbarcounter += 1
        tomcatsplash_loadingbar.append(tomcatsplash_loadingbarcounter)
    img = Image.fromarray(pixels)
    update_image(img)

blocks = np.asarray(pickle.load(open("data/world.dat", "rb")))
playing = True

def update_blocks(pix):
    # Load world from world.dat file + set void color to (150, 150, 255)
    pix = display_image(pix, "images/blocks/air.png")
    for i in range(15):
        for j in range(15):
            if blocks[i, j] != "air":
                pix = display_image(pix, "images/blocks/"+blocks[i, j]+".png", i*2, j*2)
    pix = display_image(pix, "images/steve.png", blocks[0, 15], blocks[1, 15])
    if blocks[2, 15] == "s":
        for i in range(len(bar)):
            if i == 0:
                for j in range(bar[0]):
                    pix[29, j] = [110,13,13]
            elif i == 1:
                for j in range(bar[1]):
                    pix[29, 29-j] = [84,43,0]
    elif blocks[2, 15] == "c":
        pass
    else:
        print(f"{color.RED}Error: Nonexistent gamemode (0)")
        wait(1)
        root.destroy()
        exit()
    return Image.fromarray(pix)
# Load world
# def load_world():
pixels = create_image()
img = update_blocks(pixels)
update_image(img)

# Run the main event loop
# load_world()
try:
    while True:
        # Keypress functions
        def reload(event):
            print("Reloading...")
            root.destroy()
            os.system("python main.py")
        def rewrite_world_dat(event):
            global blocks, img
            ask_if_yes = messagebox.askquestion("Confirm World Reset", "You just pressed the keybind to reset the current world (Control+Alt+O).\nAre you sure you want to do this?", icon="warning")
            if ask_if_yes == "yes":
                data = [['grass' for _ in range(16)] for _ in range(15)]
                for _ in range(15):
                    if _ == 0:
                        data[_][15] = 12
                    elif _ == 1:
                        data[_][15] = 14
                    else:
                        data[_][15] = None
                pickle.dump(data, open("data/world.dat", "wb"))
                blocks = np.asarray(data)
                img = update_blocks(pixels)
                print("Overwrote! Hopefully you didn't do this on accident...")
        def cmd(event):
            while True:
                command = input("> ").split(" ")
                if command[0] == "gamemode":
                    blocks[2, 15] = command[1]
                elif command[0] == "help":
                    cmds = [["help : Provides command help", "gamemode : Switches your gamemode", "exit: Closes the command prompt", "reload: Reloads the game"]]
                    cmdsraw = ["help", "gamemode", "exit", "reload"]
                    cmdsmi = {"help": "Provides command help\n\nSyntax:\nhelp [page id/command name]", "gamemode":"Switches your gamemode\n\nSyntax:\ngamemode [s/c]", "exit": "Closes the command prompt\n\nSyntax:\nexit", "reload": "Reloads the game (same thing as CTRL+R with devmode on)\n\nSyntax:\nreload"}
                    print("Commands Help:")
                    if len(command) == 1:
                        print("\n".join(cmds[0]))
                        print(f"Page 1/{len(cmds)}")
                    else:
                        if command[1] in cmdsraw:
                            print(cmdsmi[command[1]])
                        else:
                            print("\n".join(cmds[int(command[1])-1]))
                            print(f"Page {command[1]}/{len(cmds)}")
                elif command[0] == "exit":
                    if os.name == "nt":
                        os.system("cls")
                    print(f"{color.GREEN}Minicraft {version}\n{color.MAGENTA}Programmed by Tomcat\n{color.WHITE}Made for Cintill Development")
                    break
                elif command[0] == "reload":
                    reload(None)
                else:
                    print(f"{color.RED}Error: Invalid command (1)")
        # Bind functions
        if devmode == True:
            root.bind("<Control-r>", reload)
            root.bind("/", cmd)
        root.bind("<Control-Alt-o>", rewrite_world_dat)
        # Add movement keybinds
        if playing == True:
            def up(event):
                global img
                blocks[0, 15] -= 2
                img = update_blocks(pixels)
            def down(event):
                global img
                blocks[0, 15] += 2
                img = update_blocks(pixels)
            def left(event):
                global img
                blocks[1, 15] += 2
                img = update_blocks(pixels)
            def right(event):
                global img
                blocks[1, 15] -= 2
                img = update_blocks(pixels)
            root.bind("w", up)
            root.bind("a", right)
            root.bind("s", down)
            root.bind("d", left)

        update_image(img)

        frame += 1
except:
    pickle.dump(blocks, open("data/world.dat", "wb"))
    if os.name == "nt" and __name__ == "__main__":
        os.system("cls")
    print(f"{color.YELLOW}Exiting game...\nThank you for playing!")