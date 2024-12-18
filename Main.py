from tkinter import *
import ctypes


def preprocess_command(command):
    synonym_map = {
        "switch on": "turn on",
        "activate": "turn on",
        "shut down": "turn off",
        "lamp": "light"
    }

    for key, value in synonym_map.items():
        command = command.replace(key, value)
    return command.lower()


dfa_keywords = {"turn", "on", "off", "light", "fan", "heater", "change", "volume"}


# checks for unexpected tokens on the command determining if it should be a NFA
def count_unexpected_tokens(tokens, dfa_keywords):
    return sum(1 for token in tokens if token not in dfa_keywords)


# Decides if it should be a dfa or a nfa
def decide_automaton(command, dfa_keywords, threshold=1):
    tokens = preprocess_command(command).split()
    unexpected_count = count_unexpected_tokens(tokens, dfa_keywords)

    if unexpected_count <= threshold:
        print("Using DFA")
        return "DFA"
    else:
        print("Using NFA")
        return "NFA"


# simulate the decided one
def run_command(command, dfa_keywords):
    # Decide which automaton to use
    automaton = decide_automaton(command, dfa_keywords)

    tokens = preprocess_command(command).split()

    if automaton == "DFA":
        dfa = generate_dfa(tokens)
        print(dfa)
        if simulate_dfa(dfa, tokens):
            is_valid = True
            print(is_valid)  # True

            materilize_command(is_valid, dfa)
            return print("Command accepted by DFA! Action performed.")
        else:
            return print("DFA failed. Command not recognized.")

    elif automaton == "NFA":
        nfa = generate_nfa_from_command(tokens)
        print(nfa)

        if simulate_nfa(nfa, tokens):
            materialize_nfa(nfa)

            return print("Command accepted by NFA! Action performed.")
        else:
            return print("NFA failed. Command not recognized.")


def materialize_nfa(nfa):
    if nfa["alphabet"] == {"turn", "on", "light", "ε"}:
        turn_lights_on()
    elif nfa["alphabet"] == {"turn", "off", "light", "ε"}:
        turn_lights_off()
    elif nfa["alphabet"] == {"change", "volume", "ε", "50"}:
        set_volume(50)
    else:
        print("command not recognized")


# DFA setup
def generate_dfa(tokens):
    dfa = {
        "states": set(),
        "alphabet": set(),
        "transitions": {},
        "start_state": "q0",
        "accepting_states": set()
    }
    current_state = "q0"

    for token in tokens:
        next_state = f"q{len(dfa['states']) + 1}"
        dfa["states"].update({current_state, next_state})
        dfa["alphabet"].add(token)
        if current_state not in dfa["transitions"]:
            dfa["transitions"][current_state] = {}
        dfa["transitions"][current_state][token] = next_state
        current_state = next_state

    dfa["accepting_states"].add(current_state)
    return dfa


def simulate_dfa(dfa, tokens):
    current_state = dfa["start_state"]
    for token in tokens:
        if token in dfa["transitions"].get(current_state, {}):
            current_state = dfa["transitions"][current_state][token]
        else:
            return False
    return current_state in dfa["accepting_states"]


# NFA setup
def simulate_nfa(nfa, tokens):
    def epsilon_closure(state):
        """Find all states reachable from `state` via epsilon transitions."""
        stack = [state]
        closure = {state}
        while stack:
            current = stack.pop()
            for next_state in nfa["transitions"].get(current, {}).get("ε", []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(states, token):
        """Find all possible next states for a set of states and an input token."""
        next_states = set()
        for state in states:
            for next_state in nfa["transitions"].get(state, {}).get(token, []):
                next_states.add(next_state)
        return next_states

    # Start simulation
    current_states = epsilon_closure(nfa["start_state"])
    for token in tokens:
        current_states = move(current_states, token)
        # Include epsilon transitions after each move
        next_states = set()
        for state in current_states:
            next_states.update(epsilon_closure(state))
        current_states = next_states

    # Check if any current state is an accepting state
    return any(state in nfa["accepting_states"] for state in current_states)


def generate_nfa_from_command(tokens):
    nfa = {
        "states": set(),
        "alphabet": set(),
        "transitions": {},
        "start_state": "q0",
        "accepting_states": set()
    }

    current_state = "q0"
    nfa["states"].add(current_state)

    for token in tokens:
        next_state = f"q{len(nfa['states']) + 1}"
        nfa["states"].add(next_state)
        if token in dfa_keywords:
            nfa["alphabet"].add(token)
        else:
            nfa["alphabet"].add("ε")

        if current_state not in nfa["transitions"]:
            nfa["transitions"][current_state] = {}
        nfa["transitions"][current_state][token] = {next_state}
        current_state = next_state

    nfa["accepting_states"].add(current_state)
    return nfa


def turn_lights_off():
    window.config(bg="black")
    print("Lights are off")


def turn_lights_on():
    window.config(bg="yellow")
    print("Lights are on")


def set_volume(volume):

    if 0 <= volume <= 100:
        volume = max(0, min(100, volume))
        new_volume = int(volume * 65535 / 100)
        ctypes.windll.user32.waveOutSetVolume(0, new_volume | (new_volume << 16))
    else:
        print("Volume value not accepted")


def materilize_command(is_valid, dfa):
    if is_valid:
        if dfa["alphabet"] == {"turn", "on", "light"}:
            turn_lights_on()
        elif dfa["alphabet"] == {"turn", "off", "light"}:
            turn_lights_off()
        elif dfa["alphabet"] == {"change", "volume", "50"}:
            set_volume(50)
        else:
            print("command not recognized")
    else:
        print("command not valid")


def on_click(show=None):
    command = entry.get()
    run_command(command, dfa_keywords)


def default_on_click():
    window.config(bg="grey")


window = Tk()  # instantiate an instance of a window
window.geometry("750x750")
window.title("Language Parser")
window.config(background="grey")
label = Label(window,
              text="Natural Language Parser",
              font=('Arial', 40, 'bold'),
              fg='#fff1f1',
              bg='#601010',
              relief=RAISED,
              bd=10,
              padx=20,
              pady=20)
label.pack()
entry = Entry(window, width=30)
entry.config(font=('Arial', 20, 'bold'))
entry.pack(padx=20, pady=10, ipadx=5)
accept_button = Button(window, text="Accept", command=on_click)
accept_button.pack(pady=10)
default_button = Button(window, text="Default", command=default_on_click)
default_button.pack(pady=10)
window.mainloop()
