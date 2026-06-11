import random

MAX_REPEAT = 5


def split_options(text):
    options = []
    current = ""
    level = 0

    for c in text:
        if c == "(":
            level += 1
            current += c
        elif c == ")":
            level -= 1
            current += c
        elif c == "|" and level == 0:
            options.append(current)
            current = ""
        else:
            current += c

    options.append(current)
    return options


def generate(regex):

    i = 0
    result = ""

    while i < len(regex):

        char = regex[i]

        # grup ()
        if char == "(":

            level = 1
            j = i + 1

            while level > 0:
                if regex[j] == "(":
                    level += 1
                elif regex[j] == ")":
                    level -= 1
                j += 1

            inside = regex[i + 1:j - 1]

            options = split_options(inside)
            chosen = random.choice(options)

            generated = generate(chosen)

            repeat = 1

            if j < len(regex):

                if regex[j] == "?":
                    repeat = random.randint(0, 1)
                    j += 1

                elif regex[j] == "*":
                    repeat = random.randint(0, MAX_REPEAT)
                    j += 1

                elif regex[j] == "+":
                    repeat = random.randint(1, MAX_REPEAT)
                    j += 1

                elif regex[j] == "{":

                    end = regex.index("}", j)
                    repeat = int(regex[j + 1:end])
                    j = end + 1

            result += generated * repeat
            i = j
            continue

        # caracter simplu
        repeat = 1

        if i + 1 < len(regex):

            nxt = regex[i + 1]

            if nxt == "?":
                repeat = random.randint(0, 1)
                i += 1

            elif nxt == "*":
                repeat = random.randint(0, MAX_REPEAT)
                i += 1

            elif nxt == "+":
                repeat = random.randint(1, MAX_REPEAT)
                i += 1

            elif nxt == "{":

                end = regex.index("}", i + 1)
                repeat = int(regex[i + 2:end])
                i = end

        result += char * repeat
        i += 1

    return result


regexes = [
    "M?N{2}(O|P){3}Q*R+",
    "(X|Y|Z){3}8+(9|0)",
    "(H|I)(J|K)L*N?"
]


for regex in regexes:

    print("=" * 40)
    print("Regex:", regex)

    for _ in range(10):
        print(generate(regex))
