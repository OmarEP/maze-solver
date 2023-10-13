from graphics import Window
from line import Line 
from point import Point 

def main():
    win = Window(800, 600)
    line = Line(Point(25, 25), Point(123, 200))
    win.draw_line(line, "red")
    win.wait_for_close()

main()