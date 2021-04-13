import sys
import time
import types
import platform
import random

from graphics import *

# alter this number to change the width of the screen
width = 30.0

# alter this number to change the height of the screen
height = 30.0

# alter this number to change the size of the cells on the screen
box_pixel_size = 20

# default colors below - changeable upon instantiation of the game
default_alive_color = "#" + ("%02x%02x%02x" % (0, 0, 0))
default_dead_color = "#" + ("%02x%02x%02x" % (255, 255, 255))

default_special_alive_color = "#" + ("%02x%02x%02x" % (254, 194, 40))  # GMU Yellow
default_special_dead_color = "#" + ("%02x%02x%02x" % (12, 88, 48))  # GMU Green

# default delay between updates (in seconds)
default_update_delay = 0.2

win = None
stage = 0


##############################################
# Gets student code from their file
##############################################

def import_student_code(filename):
    """Gets student code from file into module 'student'"""
    f = open(filename)
    code = f.read()
    f.close()

    module = types.ModuleType("student")
    sys.modules["student"] = module
    exec(code, module.__dict__)

    return module


def point_to_cell(point):
    return int(point.getY()), int(point.getX())


class ConwaysGame:

    def __init__(self, window,
                 alive_color=default_alive_color,
                 dead_color=default_dead_color,
                 delay=default_update_delay):
        """Creates the graphics for the grid, sets up the data structure with student code."""

        self.window = window

        # try to create the empty cells with student's code
        try:
            self.cells = student.init_empty_cells(int(width), int(height))
        except Exception as e:
            msg = "Your code for creating an {} empty grid failed.\nError: {}"
            print(msg.format(str(int(width)) + "x" + str(int(height)), str(e)))
            window.destroy()
            sys.exit()

        self.grid = student.init_empty_cells(int(width), int(height))  # no try needed, would have failed above
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        self.alive_color = alive_color
        self.dead_color = dead_color
        self.delay = delay
        self.life_stage = 0

        for x in range(int(self.width)):
            for y in range(int(self.height)):

                rect = Rectangle(Point(x, y), Point(x + 1, y + 1))
                self.grid[y][x] = rect  # save a reference for later

                if self.cells[y][x] == 0:
                    rect.setFill(self.dead_color)
                elif self.cells[y][x] == 1:
                    rect.setFill(self.alive_color)
                else:
                    rect.setFill("red")  # make any wrong cells red!

                rect.setOutline("black")
                rect.draw(win)

    def toggle_cell(self, row, column):

        # try to toggle a single cell with the student's code
        try:
            success = student.toggle_cell(row, column, self.cells)
            if not success:
                print("Failed to toggle the cell ({}, {}) (your toggle() function returned False)".format(row, column))

        except Exception as e:
            msg = "There was an error in your code when you tried to toggle the cell ({}, {})."
            msg += "\nError: {}"
            print(msg.format(row, column, e))
            self.window.destroy()
            sys.exit()

        self._update_grid()

    def _update_grid(self):
        # update the colors based on the current alive and dead cells
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j]:
                    self.grid[i][j].setFill("black")
                else:
                    self.grid[i][j].setFill("white")

        # g{1-4} are the different forms a glider traveling towards the bottom right will take
        # b1 is a simple block surrounded by dead cells
        shapes = {"g1": [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
                  "g2": [[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],
                  "g3": [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 0, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]],
                  "g4": [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]],
                  "b1": [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
                  "bl1": [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
                  "bl2": [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
                  }

        # find and color any shapes if you are on that stage
        if stage >= 3.2:
            for name, shape in shapes.items():
                found = self._find_pattern(shape)
                for i in range(len(found)):
                    for j in range(len(found[i])):
                        if found[i][j] == "s1":
                            self.grid[i][j].setFill(default_special_alive_color)
                        elif found[i][j] == "s0":
                            self.grid[i][j].setFill(default_special_dead_color)

        self.window.master.title("Conway's Game of Life: (Step #" +
                                 str(self.life_stage) + ")")

        time.sleep(self.delay)
        self.window.update()

    def update_cells(self):
        # try to apply the CGL rules as written by the student
        try:
            self.cells = student.update(self.cells)  # student code used here
            self.life_stage += 1
        except Exception as e:
            print("Your code for updating the cells to the next stage of life had an error")
            print("\tError: " + str(e))
            self.window.destroy()
            sys.exit()

        self._update_grid()

    def create_pattern(self, i, j, name=""):
        if not name:
            name = random.choice(["blinker", "block", "R", "bigblock", "glider"])

        try:
            student.set_pattern(name, i, j, self.cells)
        except Exception as e:
            print("Failed to set a shape on the grid properly. Check your code!")
            print("Error: " + str(e))
            self.window.destroy()
            sys.exit()

        self._update_grid()

    def _find_pattern(self, pattern=None):
        """pattern is a two dimensional list of a pattern to be found and marked"""
        if pattern is None:
            pattern = [[1, 1], [1, 1]]  # basic block

        try:
            marked_grid = student.find(pattern, self.cells)
        except Exception as e:
            print("Failed to find a shape on the grid properly. Check your code!")
            print("Error: " + str(e))
            self.window.destroy()
            sys.exit()

        return marked_grid

    def pause(self):
        print("Game paused. Press 'ESC' to continue...")
        while True:
            key = self.window.getKey()
            if key == "Escape":
                break

    def translate(self, direction):
        # use the student's code to translate the grid up, down, left, right, or a combo
        try:
            self.cells = student.translate(self.cells, direction)
        except Exception as e:
            msg = "Failed to translate the grid in the direction '{}'. \n\tError: {}"
            print(msg.format(direction, e))
            self.window.destroy()
            sys.exit()

        self._update_grid()

    def reflect(self, axis):
        try:
            self.cells = student.reflect(self.cells, axis)
        except Exception as e:
            print("Something went wrong while executing your code for reflecting the cells.")
            print("Error: {}".format(e))
            self.window.destroy()
            sys.exit()
        self._update_grid()

    def invert(self):
        try:
            student.invert(self.cells)
        except Exception as e:
            print("Something went wrong while executing your code for inverting the cells.")
            print("Error: {}".format(e))
            self.window.destroy()
            sys.exit()
        self._update_grid()


def show_grid(shapes, toggle):
    # create an instance of the game
    game = ConwaysGame(win)

    if shapes and toggle:

        # put a random pattern in the middle
        game.create_pattern(int(width // 2), int(height // 2))

        # toggle cells until you hit the "ESC" key
        while True:
            point = game.window.checkMouse()
            key = game.window.checkKey()

            if point:
                game.toggle_cell(*point_to_cell(point))

            if key == "Escape":
                break

    elif shapes:
        game.create_pattern(10, 10, "block")
        game.create_pattern(10, 18, "bigblock")
        game.create_pattern(10, 24, "R")
        game.create_pattern(20, 10, "blinker")
        game.create_pattern(20, 18, "glider")
        game.pause()

    elif toggle:
        while True:
            point = game.window.checkMouse()
            key = game.window.checkKey()

            if point:
                game.toggle_cell(*point_to_cell(point))

            if key == "Escape":
                break

    else:
        # when both false, this will just show a blank grid
        game.pause()


def translate():
    game = ConwaysGame(win)

    while True:

        # obtain key/mouse press if they were made
        key = game.window.checkKey()
        point = game.window.checkMouse()

        # toggle cell if clicked
        if point:
            game.toggle_cell(*point_to_cell(point))

        # translate grid if key pressed
        if key in ["d", "D", "Right"]:
            game.translate("right")
        elif key in ["a", "A", "Left"]:
            game.translate("left")
        elif key in ["w", "W", "Up"]:
            game.translate("up")
        elif key in ["s", "S", "Down"]:
            game.translate("down")

        # stop simulating if 'ESC' pressed
        if key == "Escape":
            print("Done.")
            break


def reflect_and_invert():
    game = ConwaysGame(win)
    while True:
        key = game.window.checkKey()
        point = game.window.checkMouse()

        # toggle cell if clicked
        if point:
            game.toggle_cell(*point_to_cell(point))

        if key == "x" or key == "X":
            game.reflect("x")
        elif key == "y" or key == "Y":
            game.reflect("y")
        elif key == "i" or key == "I":
            game.invert()

        if key == "Escape":
            "Done."
            break


def play_cgl(forever):
    game = ConwaysGame(win)

    if stage == 3.2:
        game.create_pattern(5, 5, name="glider")
        game.create_pattern(10, 10, name="block")
    else:
        game.create_pattern(12, 13, name="R")

    go = False

    while True:
        key = game.window.checkKey()
        point = game.window.checkMouse()

        if point and stage == 3.2:
            game.toggle_cell(*point_to_cell(point))

        # update cells if you're allowed to
        if (not forever and key == "Return") or (forever and go):
            game.update_cells()  # advance one step in the life

        # no manipulation unless steps aren't happening while going forever
        elif forever and not go:

            if point:
                game.toggle_cell(*point_to_cell(point))

            # figure out what to do with key press
            if key == "x" or key == "X":
                game.reflect("x")
            elif key == "y" or key == "Y":
                game.reflect("y")
            elif key == "i" or key == "I":
                game.invert()
            elif key in ["d", "D", "Right"]:
                game.translate("right")
            elif key in ["a", "A", "Left"]:
                game.translate("left")
            elif key in ["w", "W", "Up"]:
                game.translate("up")
            elif key in ["s", "S", "Down"]:
                game.translate("down")
            elif key != "" and key != "Return" and key != "Escape":
                print("You pressed and invalid key: {}".format(key))

        # if you pressed a key, then either resume or pause (flip previous state)
        if key == "Return":
            go = not go

        if key == "Escape":
            print("Done.")
            break


def main():
    global python_command, win, stage

    python_command = "python" if platform.system() == 'Windows' else "python3"

    if len(sys.argv) < 2:
        raise Exception("needed student's file name as command-line argument:"
                        + "\n\t\"" + python_command + ' provided.py gmason76_2xx_Px.py stage"')
    elif len(sys.argv) < 3:
        raise Exception("needed desired stage as command-line argument:"
                        + "\n\t\"" + python_command + ' provided.py gmason76_2xx_Px.py stage"')
    elif sys.argv[2] not in ["0", "1A", "1a", "1B", "1b", "1C", "1c", "2A", "2a", "2B", "2b",
                             "3A", "3a", "3B", "3b", "4"]:
        raise Exception("the stage given as a command-line argument is not valid")

    win = GraphWin("Conway's Game of Life",
                   (width * box_pixel_size),
                   height * box_pixel_size, autoflush=False)

    win.setCoords(0.0, height, width, 0.0)

    # get student code as module for use in the game
    global student
    student = import_student_code(sys.argv[1])

    # stage 0... just as a first time command
    if sys.argv[2] == "0":
        print("Starting Stage 0...")
        stage = 0
        t = Text(Point(width // 2, height // 2 - 1), "If you can read this, you've completed Stage 0!")
        t.setSize(24)
        t.draw(win)
        t.setStyle("bold")
        t = Text(Point(width // 2, height // 2 + 2), "Press any key to quit.")
        t.setSize(24)
        t.setStyle("bold")
        t.draw(win)
        win.setBackground("#ba88f7")
        while True:
            key = win.checkKey()
            if key:
                break

    # stage 1A: display the empty grid
    if sys.argv[2] == "1A" or sys.argv[2] == "1a":
        stage = 1
        print("Starting stage 1A...")  # display an empty grid
        print("You should see an empty grid with grid lines filling the window.")
        print("Press 'ESC' to quit.")
        show_grid(False, False)

    # stage 1B: display grid with random shape and ability to toggle cells
    if sys.argv[2] == "1B" or sys.argv[2] == "1b":
        stage = 1
        print("Starting stage 1B...")
        print("You should have the ability to toggle cells on/off by clicking on them.")
        print("Press 'ESC' to quit.")
        show_grid(False, True)

    # stage 1C: display grid with shapes written into it
    if sys.argv[2] == "1C" or sys.argv[2] == "1c":
        stage = 1
        print("Starting stage 1C...")
        print("You should see all of the required shapes in different places on the grid.")
        print("Press 'ESC' to quit.")
        show_grid(True, False)

    # stage 2A: key presses that invoke reflect() and invert()
    if sys.argv[2] == "2A" or sys.argv[2] == "2a":
        stage = 2
        print("Press 'x' to reflect the cells on the x axis, or or press 'y' to reflect along the y axis.")
        print("Press 'i' to invert the cells.")
        print("Make sure that you set some cells to 'alive' first!")
        reflect_and_invert()

    # stage 2B: display grid and allow key presses to translate the grid in a direction
    if sys.argv[2] == "2B" or sys.argv[2] == "2b":
        stage = 2
        print("Starting stage 2B...")
        print("Use w/a/s/d or the arrow keys to translate the grid up/left/down/right.")
        print("Make sure that you set some cells to 'alive' first!")
        translate()

    # stage 3A: update grid should be working now
    if sys.argv[2] == "3A" or sys.argv[2] == "3a":
        stage = 3.1
        print("Starting stage 3A...")
        print("This time, you should be able to press 'Enter' or 'Return' "
              "on your keyboard to advance one step in the life of the system.")
        play_cgl(False)

    # stage 3B:  display grid and allow any key press to advance one life in CGL
    if sys.argv[2] == "3B" or sys.argv[2] == "3b":
        stage = 3.2
        print("Starting stage 3B...")
        print("Should be able to see shapes colored in with Mason colors!")
        print("If you toggle cells, you can see the colors come and go appropriately.")
        play_cgl(False)

    # stage 4 (final stage): any key press will continue the game indefinitely
    # cell manipulation (translation, flipping/inverting, toggling, etc) allowed on game pause
    # aka sandbox mode!
    if sys.argv[2] == "4":
        stage = 4
        print("Starting stage 4...")
        print("Running full simulation. Press Enter or Return to pause, press it again to resume.")
        print("When the simulation is paused, you can translate/invert/reflect the cells")
        print("using the same keys as you did in the previous stages.")
        play_cgl(True)


# run the program if called from command line
if __name__ == "__main__":
    main()
