import random
import time
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def error():
    print("radās kritiska kļūda, lūdzu, mēģiniet vēlāk")
    raise ValueError


LOGO = """
SQRT -(WORLD MATHS^2) v0.1 DEV BUILD
(c) MAKSIMS, ARTJOMS, SERGEJS, KIRILS INC. ALL RIGHTS RESERVED
--------------------------------------------------------------
"""

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

DIFFICULTY_LOOKUP = [  # Max numbers, Subtraction allowed, time to answer
    [5, False, 120],
    [10, False, 120],
    [50, False, 120],
    [100, False, 120],
    [10, True, 20],
    [50, True, 20],
    [100, True, 20],
    [1000, True, 60],
    [1000, True, 30],
    [1000, True, 20],
    [1000, True, 10]
]

print(LOGO)

difficulty = input("ievadiet grūtības pakāpi no 0 līdz 10: ")
try:
    difficulty = int(difficulty)
    max_nums, subtraction_allowed, time_to_answer = DIFFICULTY_LOOKUP[difficulty]
except ValueError:
    error()

print(f"Maksimālais skaitlis: {max_nums}; Atņemšana: {'ir' if subtraction_allowed else 'nav'}; laiks atbildēi: {time_to_answer} sekundes")

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
    #print(CURSOR_UP_ONE + ERASE_LINE, flush=True, end="")

print(CURSOR_UP_ONE + ERASE_LINE, flush=True, end="\r")

print(f"{n_right}/{len(answers_times)}")
print(f"Videjais laiks atbildem: {sum(answers_times)/len(answers_times):6f}±0.000005s")
