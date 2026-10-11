import turtle
import easygui

CHOICES = ["Rectangle", "Hexagon", "Spiral", "Flower"]


def ask_shape():
    return easygui.buttonbox("Which pattern should I draw?", "Shape Painter", CHOICES)


def ask_size():
    return easygui.integerbox("Size (40 to 200):", "Size", 100, 40, 200)


def ask_colour():
    text = easygui.enterbox("Pen colour (for example green, orange, purple):", "Colour", "green")
    if text is None:
        return None
    text = text.strip().lower()
    return text or "green"


def colour_works(name):
    t = turtle.Turtle()
    t.hideturtle()
    try:
        t.color(name)
        return True
    except turtle.TurtleGraphicsError:
        return False
    finally:
        t.clear()


def jump(t, x, y):
    t.penup()
    t.goto(x, y)
    t.pendown()


def rectangle(t, size, colour):
    jump(t, -size, -size / 2)
    t.color(colour, colour)
    t.begin_fill()
    for length in (size * 2, size, size * 2, size):
        t.forward(length)
        t.left(90)
    t.end_fill()


def hexagon(t, size, colour):
    jump(t, -size / 2, -size * 0.87)
    t.color(colour, colour)
    t.begin_fill()
    for _ in range(6):
        t.forward(size)
        t.left(60)
    t.end_fill()


def spiral(t, size, colour):
    jump(t, 0, 0)
    t.color(colour)
    step = 2
    while step < size * 2:
        t.forward(step)
        t.left(91)
        step += 2


def flower(t, size, colour):
    jump(t, 0, 0)
    t.color(colour)
    for _ in range(12):
        t.circle(size / 2)
        t.left(30)


DRAWERS = {
    "Rectangle": rectangle,
    "Hexagon": hexagon,
    "Spiral": spiral,
    "Flower": flower,
}


def main():
    shape = ask_shape()
    if shape is None:
        return
    size = ask_size()
    if size is None:
        return
    colour = ask_colour()
    if colour is None:
        return

    screen = turtle.Screen()
    screen.title("Shape Painter")
    screen.setup(640, 640)

    if not colour_works(colour):
        easygui.msgbox("I don't know that colour, so I'll use green.", "Colour")
        colour = "green"

    pen = turtle.Turtle()
    pen.speed(6)
    pen.pensize(3)
    DRAWERS[shape](pen, size, colour)
    pen.hideturtle()

    easygui.msgbox("Finished drawing: " + shape, "Done")
    turtle.bye()


if __name__ == "__main__":
    main()
