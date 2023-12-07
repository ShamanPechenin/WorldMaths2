import random
import time
import json


try:
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    fancy_console = True
except AttributeError:
    fancy_console = False
    print("Not on windows")


def error():
    print("radās kritiska kļūda, lūdzu, mēģiniet vēlāk")
    raise ValueError


try:
    with open("maths_leaderboard.json", 'r+') as file:
        leaderboard = json.loads(file.read())
except json.decoder.JSONDecodeError:
    leaderboard = {"stats": []}
except FileNotFoundError:
    leaderboard = None

LOGO = """
--------------------------------------------------------------
SQRT -(WORLD MATHS^2) v0.1 DEV BUILD
(c) MAKSIMS, ARTJOMS, SERGEJS, KIRILS INC. ALL RIGHTS RESERVED
--------------------------------------------------------------
"""

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

DIFFICULTY_LOOKUP = [  # Max numbers, Subtraction allowed
    [5, False],
    [10, False],
    [50, False],
    [100, False],
    [10, True],
    [50, True],
    [100, True],
    [1000, True],
]

print(LOGO)

difficulty = input("ievadiet grūtības pakāpi no 0 līdz 7: ")
try:
    difficulty = int(difficulty)
    max_nums, subtraction_allowed = DIFFICULTY_LOOKUP[difficulty]
except ValueError:
    error()

print(f"Maksimālais skaitlis: {max_nums}; Atņemšana: {'ir' if subtraction_allowed else 'nav'}")

n_right = 0
answers_times = []

for i in range(10):
    num_1 = random.randint(0, max_nums)
    num_2 = random.randint(0, max_nums)
    if num_2 > num_1:
        num_1, num_2 = num_2, num_1

    if subtraction_allowed and random.randint(0, 1) == 1:
        subtract = True
        right_answer = num_1 - num_2
    else:
        subtract = False
        right_answer = num_1 + num_2

    start = time.perf_counter()
    answer = input(f"Jautājums {i}: {num_1}{'-' if subtract else '+'}{num_2}=")
    end = time.perf_counter()
    answers_times.append(end - start)

    if fancy_console:
        print(CURSOR_UP_ONE + "\x1b[30C", flush=True, end="")

    try:
        answer = int(answer)
    except ValueError:
        error()

    if answer == right_answer:
        print("Pareizi!")
        n_right += 1
    else:
        print(f"Kļūda, atbilde bija {right_answer}")

if fancy_console:
    print(CURSOR_UP_ONE + ERASE_LINE, flush=True, end="\r")

mean_time = sum(answers_times)/len(answers_times)
print(f"{n_right}/{len(answers_times)}")
print(f"Videjais laiks atbildem: {mean_time:6f}±0.000005s")

if leaderboard is not None:
    name = input("Ievadiet savu vārdu: ")
    leaderboard["stats"].append({"name": name, "accuracy": n_right/len(answers_times), "time": mean_time})
    with open("maths_leaderboard.json", 'w') as file:
        file.write(json.dumps(leaderboard, indent=2))

    print("--------------------------------------------------------------\nRekordu tabula:")
    results = leaderboard["stats"]
    results = sorted(results, key=lambda x: x["time"])
    for i, player in enumerate(results[:10]):
        print(f"{i}. vieta  {player['name']}:   {player['time']:6f}s")
    print("--------------------------------------------------------------")
