import random
import turtle

words = ["RAISE", "STRUM", "SORRY", "DOGMA", "PITCH", "HITCH", "PATCH", "HATCH", "LATCH", "CATCH", "ARISE", "DOUBT", "HELLO", "ANNEX", "APPLY", "APPLE", "HAPPY", "SLYLY", "SHYLY", "HAVEN", "RAVEN", "WOVEN", "JOLLY", "HOLLY", "QUICK", "CLOWN", "CROWD", "CLOUD", "CHUNK", "CHOMP", "PHASE", "FLAKE", "BAKER", "POKER", "HONEY", "ROCKY", "CRANE", "FREAK", "FOUND", "TOOTH", "TEETH", "FORTY", "FIFTY", "SIXTY", "FLOWN", "FLUFF", "STUFF", "BUDGE", "RIDGE", "HINGE", "ALERT", "ABOUT", "BLEND", "CRISP", "GLORY", "PLANT", "FRANK", "GHOST", "BRINK", "SNIPE", "TWIST", "SHARP", "BLUSH", "GRACE", "SMILE", "TRAIN", "MOVER", "GRAZE", "VIVID", "ZEBRA", "QUILT", "QUERY", "BLOOM", "BRASS", "CINCH", "DREAM", "EMBER", "FABLE", "GAMMA", "HEART", "IGLOO", "JUICE", "KNOCK", "LLAMA", "MAGIC", "NINJA", "OPERA", "PRIDE", "QUEEN", "ROAST", "SCALE", "TANGO", "ULCER", "VAPOR", "WALTZ", "XENON", "YOUNG", "ZIPPY", "BRINE", "CRUSH", "TWIRL", "SHONE", "BLAST", "GRIND", "SMASH", "THORN", "PRISM", "BRUTE", "SWEET", "TRUST", "GLINT", "SWIRL", "PLUSH", "BRIAR", "GUILD", "SPOON", "TRAIL", "SNAKE", "SCOPE", "GRAIN", "SPEND", "TRICK", "SLICK", "BRISK", "FLOOR", "STACK", "GROVE", "BRAND", "CLIMB", "DRINK", "FLINT", "GRASP", "MARCH", "NERVE", "OVERT", "PRONG", "QUOTA", "ROUND", "SHOOT", "STONE", "TRUMP", "VAULT", "WHEAT", "WRONG", "YIELD", "ZONED"]
answer = random.choice(words)
guesses = 0

screen = turtle.Screen()
pen = turtle.Turtle()
screen.tracer(0) 
pen.hideturtle()
pen.penup()
pen.goto(0, 280)
pen.pendown()
pen.write("WORDLE", align="center", font=("Arial", 50, "bold"))

x_pos = -195
y_pos = 200

for i in range(6):
    for j in range(5):
        pen.penup()
        pen.goto(x_pos, y_pos)
        pen.pendown()
        for _ in range(4):
            pen.forward(70)
            pen.left(90)
        x_pos+=80
    x_pos = -195
    y_pos-=80

screen.update()

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()

# Box parameters from your original code
x_start = -195
y_start = 200
box_size = 70
row_spacing = 80
font_size = 32
box_centers = []

for row in range(6):
    row_centers = []
    for col in range(5):
        x = x_start + col * row_spacing
        y = y_start - row * row_spacing

        # Calculate exact center of the box
        cx = x + box_size / 2 + 2
        cy = y - box_size / 2 + font_size / 4 + 40 # compensate for font baseline

        row_centers.append((cx, cy))
    box_centers.append(row_centers)

current_row = 0
current_col = 0
typed = [[""] * 5 for _ in range(6)]


def redraw_all_rows():
    """Redraw letters for all rows up to the current row."""
    writer.clear()
    for row in range(current_row + 1):
        for col in range(5):
            letter = typed[row][col]
            if letter != "":
                cx, cy = box_centers[row][col]
                writer.goto(cx, cy)
                writer.write(letter, align="center", font=("Arial", font_size, "bold"))


def add_letter(letter):
    """Add a capital letter in the current row, max 5 letters."""
    global current_col
    if current_col >= 5:
        return
    typed[current_row][current_col] = letter.upper()
    current_col += 1
    redraw_all_rows()


def backspace():
    """Remove the last letter typed in the current row."""
    global current_col
    if current_col == 0:
        return
    current_col -= 1
    typed[current_row][current_col] = ""
    redraw_all_rows()

def letter_allowed(letter, row):
    guess = typed[row]

    # Count how many of this letter appear in the answer
    total = answer.count(letter)

    # Count greens (exact matches)
    greens = sum(1 for i in range(5) if guess[i] == answer[i] == letter)

    # Count how many of this letter have already been marked yellow earlier in the guess
    yellows_so_far = 0
    for i in range(5):
        if guess[i] == letter and guess[i] != answer[i]:
            if greens + yellows_so_far >= total:
                return False
            yellows_so_far += 1

    return True

def compute_colors(row):
    guess = typed[row]
    colors = ["gray"] * 5

    # Step 1: count letters in answer
    remaining = {}
    for ch in answer:
        remaining[ch] = remaining.get(ch, 0) + 1

    # Step 2: fill greens first
    for i in range(5):
        if guess[i] == answer[i]:
            colors[i] = "green"
            remaining[guess[i]] -= 1

    # Step 3: fill yellows
    for i in range(5):
        if colors[i] == "gray" and guess[i] in remaining and remaining[guess[i]] > 0:
            colors[i] = "yellow"
            remaining[guess[i]] -= 1

    return colors

def next_row():
    global current_row, current_col, guesses

    if current_col < 5:
        return

    guesses += 1
    colors = compute_colors(current_row)

    for i in range(5):
        x = x_start + i*80
        y = y_start - current_row*80
        pen.penup()
        pen.goto(x, y)
        pen.pendown()
        pen.fillcolor(colors[i])
        pen.begin_fill()
        for _ in range(4):
            pen.forward(70)
            pen.left(90)
        pen.end_fill()
        pen.penup()

    screen.update()

    redraw_all_rows()

    if "".join(typed[current_row]) == answer:
        pen.penup()
        pen.goto(0, -280)
        pen.pendown()
        if guesses != 1:
            pen.write("You won in " + str(guesses) + " tries!", align="center", font=("Arial", 30, "bold"))
            return
        else:
            pen.write("You won in 1 try!", align="center", font=("Arial", 30, "bold"))
            return
    elif guesses == 6:
        pen.penup()
        pen.goto(0, -280)
        pen.pendown()
        pen.write("You lost! The word was " + answer + "!", align="center", font=("Arial", 30, "bold"))
        return

    current_row += 1
    current_col = 0
    


# ----------------- KEY BINDINGS -----------------
for ch in "abcdefghijklmnopqrstuvwxyz":
    screen.onkeypress(lambda c=ch: add_letter(c), ch)

screen.onkeypress(backspace, "BackSpace")
screen.onkeypress(next_row, "Return")  # Enter key
screen.listen()

turtle.done()