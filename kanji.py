from graphics import *
import random


def in_rectangle(rect, point):
    return rect[0] <= point.x <= rect[2] and rect[1] <= point.y <= rect[3]


values = [line[:-1].split(",") for line in open("kanji.txt", "r").readlines()]

win = GraphWin(width=500, height=500)  # create a window
win.setCoords(
    0, 0, 10, 10
)  # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
buttons = [
    [1, 4, 5, 6],
    [5, 4, 9, 6],
    [1, 6, 5, 8],
    [5, 6, 9, 8],
]

button_graphics = [Rectangle(Point(b[0], b[1]), Point(b[2], b[3])) for b in buttons]

regenerate = True
answers = []
count = 0
ans = 0
text = []
question = 0
for b in button_graphics:
    b.draw(win)

while True:

    if regenerate:

        count = random.randrange(0, len(values))

        question = random.randrange(0, 4)
        ans = random.randrange(0, 3)
        if ans == question:
            ans += 1

        answers = [val[ans] for val in random.sample(values, 3)]
        answers.append(values[count][ans])
        random.shuffle(answers)

        text = [
            Text(
                Point(5, 2),
                values[count][question],
            ),
            Text(
                Point(3, 5),
                answers[0],
            ),
            Text(
                Point(7, 5),
                answers[1],
            ),
            Text(
                Point(3, 7),
                answers[2],
            ),
            Text(
                Point(7, 7),
                answers[3],
            ),
        ]
        for t in text:
            t.draw(win)
        regenerate = False

    pressed = -1
    mouse = win.getMouse()
    for i in range(0, len(buttons)):
        if in_rectangle(buttons[i], mouse):
            pressed = i
            break

    if pressed != -1:
        answer = values[count][ans]
        print(answer == answers[pressed])
        print(f"{values[count][question]}, {answer}")
        regenerate = True
        for t in text:
            t.undraw()
