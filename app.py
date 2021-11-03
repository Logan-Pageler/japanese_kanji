# app.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

css = ""
for line in open("app.css", "r").readlines():
    css += line

page = """
<html>
    <head>
        <style>
            {}
        </style>
    </head>
    <body>
        <h2>Welcome to kanji-learner!</h2>
        <form method ="post" action="/">
            <div>
                <p> Practice sections: (use format 1,3-4) </p>
                <input type="text" name="units" value = {}> 
                <button name="reset" value="reset"> Reset Accuracy </button>
                <p> Units avaible: 4-11 </p>
            </div>
            <<>>
        </form> 
    <body>
<html>
"""


def generate(prev_ans, accuracy, button, values):
    count = random.randrange(0, len(values))

    question = random.randrange(0, 2)
    ans = 0
    if question == 1:
        question = 1 + random.randrange(0, 3)
    else:
        ans = 1 + random.randrange(0, 3)

    answers = [val[ans] for val in random.sample(values, 3)]
    answers.append(values[count][ans])
    random.shuffle(answers)

    text = ""
    arr = accuracy.split("/")

    if prev_ans != None:
        arr[1] = int(arr[1]) + 1
        if prev_ans[4] == prev_ans[button]:
            arr[0] = int(arr[0]) + 1
            text += '<p class="correct"> Correct! </p>'
        else:
            text += '<p class="incorrect"> Incorrect! </p>'

        text = (
            text
            + f"\n<p> Previous Answer: {prev_ans[4]}  Accuracy: {arr[0]}/{arr[1]} </p>"
        )

    text = (
        f"""
            <div class="button-panel">
                <p class="question"> {values[count][question]}</p>
                <div>
                    <button name="button 1" value="1" class="answer-button"> {answers[0]} </button>
                    <button name="button 2" value="2" class="answer-button"> {answers[1]} </button>
                </div>
                <div>
                    <button name="button 3" value="3" class="answer-button"> {answers[2]} </button>
                    <button name="button 4" value="4" class="answer-button"> {answers[3]} </button>
                </div>
                <input class="answer" name="prev" type="hidden" value="{answers+[values[count][ans], f"{arr[0]}/{arr[1]}"]}"> 
            </div>
            """
        + text
    )

    return text


lessons = []
for i in range(4, 12):
    lessons += [
        [
            line[:-1].split(",")
            for line in open(f"kanji/lesson{i}.txt", "r", encoding="utf-8").readlines()
        ]
    ]


@app.route("/", methods=["POST"])
def post_something():
    new = "Something broke... try refreshing"
    range = request.form.get("units")
    range = "".join(range.split())
    range = range.split(",")
    values = []
    for r in range:
        try:
            if "-" in r:
                temp = r.split("-")
                values += [
                    j for i in lessons[int(temp[0]) - 4 : int(temp[1]) - 4] for j in i
                ]
            else:
                values += lessons[int(r) - 4]
        except:
            values = [j for i in lessons for j in i]
    if request.form.get("button 1"):
        prev_ans = [txt[1:-1] for txt in request.form.get("prev")[1:-1].split(", ")]
        new = page.replace(
            "<<>>",
            generate(prev_ans, prev_ans[5], 0, values),
        ).format(css, request.form.get("units"))
    elif request.form.get("button 2"):
        prev_ans = [txt[1:-1] for txt in request.form.get("prev")[1:-1].split(", ")]
        new = page.replace(
            "<<>>",
            generate(prev_ans, prev_ans[5], 1, values),
        ).format(css, request.form.get("units"))
    elif request.form.get("button 3"):
        prev_ans = [txt[1:-1] for txt in request.form.get("prev")[1:-1].split(", ")]
        new = page.replace(
            "<<>>",
            generate(prev_ans, prev_ans[5], 2, values),
        ).format(css, request.form.get("units"))
    elif request.form.get("button 4"):
        prev_ans = [txt[1:-1] for txt in request.form.get("prev")[1:-1].split(", ")]
        new = page.replace(
            "<<>>",
            generate(prev_ans, prev_ans[5], 3, values),
        ).format(css, request.form.get("units"))
    elif request.form.get("reset"):
        new = page.replace(
            "<<>>",
            generate(None, "0/0", None, values),
        ).format(css, request.form.get("units"))
    return new
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality


# A welcome message to test our server
@app.route("/", methods=["get"])
def index():
    new = page.replace(
        "<<>>",
        generate(None, "0/0", None, [j for i in lessons for j in i]),
    ).format(css, "4-11")
    return new


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
