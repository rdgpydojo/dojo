import turtle
import random
#import pdb; pdb.set_trace()
OFFSET=10

def main(pen):
    posx = -500
    posy = -300
    pen.goto(posx, posy)
    for x in range(8):
        width = draw_building(pen, posx, posy)
        pen.up()
        posx += width + OFFSET
        
def draw_building(pen, x, y):
    print x, y
    pen.goto(x, y)
    pen.down()
    
    width = random.randint(30, 200)
    height = random.randint(30, 500)
    
    pen.forward(height)
    pen.right(90)
    pen.forward(width)
    pen.right(90)
    pen.forward(height)
    pen.right(90)
    pen.forward(width)
    pen.right(90)
    pen.up()
    
    draw_windows(pen, height, width)

    return width

def draw_windows(pen, height, width):
    window_size = 15
    posx, posy = pen.pos()
    posx = int(posx)
    posy = int(posy)
    
    for i in range(7):
        pen.up()
        x = random.randint(posx+2, posx+width-window_size)
        y = random.randint(posy+2, posy+height-window_size)
        draw_window(pen, x, y, window_size, window_size)
    pen.goto(posx, posy)
        

def draw_window(t, x, y, width, height):
    t.setheading(0)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.forward(width)
    t.right(90)
    t.forward(height)
    t.right(90)
    t.forward(width)
    t.right(90)
    t.forward(height)

    t.goto(x + width / 2, y)

    t.setheading(270)
    t.forward(height)

    t.penup()

    t.goto(x, y - height / 2)
    t.setheading(0)
    t.pendown()
    t.forward(width)
    t.penup()
    t.goto(x, y)

    t.setheading(90)
    return


    
if __name__ == "__main__":
    #turtle.mode("standard")
    t = turtle.Turtle()
    
    t.speed(0)
    t.up()
    t.right(-90)
    main(t)
    raw_input("===>")