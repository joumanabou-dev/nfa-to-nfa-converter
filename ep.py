# Authors:
#  Benzid Oumeima (Group 02 Cyber Security)
#  Gadda Maya   (Group 02 Cyber  Security),
#  Boufroukh Djemana (Group 01 Cyber Security),

# ε-NFA to NFA Conversion
# This program converts an ε-NFA to an equivalent NFA by removing epsilon transitions.

# Symbol used for epsilon
EPSILON = "ε"

# Allowed user inputs for epsilon (case-insensitive, normalized to EPSILON)
EPSILON_INPUTS = ["e", "eps", "epsilon", "ε"]


#  Function 1:
# Check if the NFA contains any epsilon transitions


def check_for_epsilon_transitions(nfa):
    for state in nfa["states"]:
        if state in nfa["transitions"]:
            # Check for any epsilon-like symbol in transitions
            for symbol in nfa["transitions"][state]:
                if symbol.lower() in ["e", "eps", "epsilon"] or symbol == EPSILON:
                    return True
    return False


#  Function 2:
# Calculate epsilon-closure of ONE state


def calculate_epsilon_closure(nfa, start_state):
    closure = set()
    stack = [start_state]

    while stack:
        state = stack.pop()
        if state not in closure:
            closure.add(state)
            # Add all epsilon transitions from this state
            epsilon_moves = nfa["transitions"].get(state, {}).get(EPSILON, [])
            for next_state in epsilon_moves:
                if next_state not in closure:
                    stack.append(next_state)
    return sorted(list(closure))


#  Function 3:
# Calculate epsilon-closure for ALL states


def calculate_all_epsilon_closures(nfa):
    closures = {}
    for state in nfa["states"]:
        closures[state] = calculate_epsilon_closure(nfa, state)
    return closures


#  Function 4:
# Create new  Epsilon-Free Transitions


def calculate_new_transitions(nfa, closures):
    # Dictionary to store the new transition function
    new_transitions = {}

    for state in nfa["states"]:
        # Initialize an empty transition dictionary for this state
        new_transitions[state] = {}

        # Iterate over each input symbol (excluding epsilon)
        for symbol in nfa["symbols"]:
            if symbol == EPSILON:  # skip epsilon symbols in alphabet
                continue

            # Set to collect all states reachable using this symbol
            reachable_states = set()

            # For every state in the epsilon-closure of the current state
            for c_state in closures[state]:
                # Get transitions from the closure state
                transitions_from_c_state = nfa["transitions"].get(c_state, {})

                # If there is a transition on the current symbol
                if symbol in transitions_from_c_state:
                    # Follow the transition to its target states
                    for target in transitions_from_c_state[symbol]:
                        # Add the epsilon-closure of each target state
                        reachable_states.update(closures[target])

            # Store the sorted list of reachable states for this symbol
            new_transitions[state][symbol] = sorted(list(reachable_states))

    return new_transitions


# Function 5:
#  Find new final states after removing epsilon


def determine_new_final_states(nfa, closures):
    new_finals = set()
    for state in nfa["states"]:
        # Check if any original final is in this state's closure
        if any(f in closures[state] for f in nfa["final_states"]):
            new_finals.add(state)
    return sorted(list(new_finals))


###### _____________________________Read NFA from the user __________________________________ #####
def read_nfa():
    print("\nEnter NFA Information: ")
    print("_____________________")

    # Read states
    while True:
        # Users Must Enter States separated by space
        states_input = input("States (space-separated): ").split()

        # Ensure the state list is not empty
        if not states_input:
            print("State list cannot be empty. Try again.")
            continue

        # Remove duplicate states while preserving input order
        states = list(dict.fromkeys(states_input))

        if len(states) < len(states_input):
            print("!!! Duplicate states were removed:", set(states_input) - set(states))

        print("Accepted states:", states)
        break

    # Enter alphabet symbols
    while True:
        symbols_input = input("Alphabet symbols (space-separated): ").split()

        if not symbols_input:
            print("Alphabet cannot be empty. Try again.")
            continue

        # Remove epsilon symbols from alphabet if accidentally entered
        symbols_input = [s for s in symbols_input if s not in EPSILON_INPUTS]

        symbols = list(dict.fromkeys(symbols_input))

        if len(symbols) < len(symbols_input):
            print(
                "!!! Duplicate symbols were removed:", set(symbols_input) - set(symbols)
            )

        print("Accepted Symbols: ", symbols)
        break

    # Enter start state
    while True:
        start_state = input("Start state: ")
        if start_state not in states:
            print(f" Start state '{start_state}' is not in state list. Try again.")
        else:
            break

    # Enter final states (multiple allowed, type 'done' when finished)
    final_states = []

    print("\nEnter final states one by one. Type 'done' when finished:")

    while True:
        final_state_input = input("Final state: ").strip()

        if final_state_input.lower() == "done":
            if not final_states:
                print(
                    "!! No final states entered. The automaton will accept NO strings."
                )
            break

        if not final_state_input:
            print("!! Empty input. Enter a state or 'done'.")
            continue

        if final_state_input not in states:
            print(
                f"!! Final state '{final_state_input}' is not in the state list. Try again."
            )
            continue

        if final_state_input in final_states:
            print(f"!! Duplicate final state '{final_state_input}' ignored.")
            continue

        final_states.append(final_state_input)
        print(f"Accepted final states so far: {final_states}")

    # Enter transitions

    transitions = {}

    print("\nEnter transitions one by one in the format: from_state symbol to_state")
    print("Type 'done' when finished.\n")

    while True:
        line = input("Transition: ").strip()

        if line == "":
            print("!!! Empty input. Type 'done' to finish or enter a transition.")
            continue

        if line.lower() == "done":
            break

        parts = line.split()
        if len(parts) != 3:
            print("!!! Format error. Use: from_state symbol to_state")
            continue

        from_state, symbol, to_state = parts

        # Normalize epsilon input
        if symbol.lower() in EPSILON_INPUTS:
            symbol = EPSILON

        # Check if from_state and to_state exist
        if from_state not in states:
            print(f"!!! Unknown from-state '{from_state}'")
            continue

        if to_state not in states:
            print(f"!!! Unknown to-state '{to_state}'")
            continue

        # Check if symbol is valid (must be in alphabet or epsilon)
        if symbol != EPSILON and symbol not in symbols:
            print(f"!!! Symbol '{symbol}' not in alphabet. Transition ignored.")
            continue

        if from_state not in transitions:
            transitions[from_state] = {}

        if symbol not in transitions[from_state]:
            transitions[from_state][symbol] = set()

        if to_state in transitions[from_state][symbol]:
            print(
                f" Duplicate transition ignored: {from_state} --({symbol})--> {to_state}"
            )
        else:
            transitions[from_state][symbol].add(to_state)

    # convert sets to lists
    for from_state in transitions:
        for symbol in transitions[from_state]:
            transitions[from_state][symbol] = sorted(
                list(transitions[from_state][symbol])
            )

    return {
        "states": states,
        "symbols": symbols,
        "start_state": start_state,
        "final_states": final_states,
        "transitions": transitions,
    }


# Function to Display the new NFA without epsilon


def display_nfa(nfa, new_transitions, new_final_states):
    print("\n" + "=" * 40)
    print("NFA without ε-transitions")
    print("=" * 40)

    print("States:", nfa["states"])
    print("Alphabet:", nfa["symbols"])
    print("Start state:", nfa["start_state"])
    print("Final states:", new_final_states)

    print("\nTransition Table:")
    header = "State".center(6) + " | "
    for s in nfa["symbols"]:
        header += f"{s:^12} | "
    print(header)
    print("-" * len(header))

    for state in nfa["states"]:
        row = f"{state:^6} | "
        for s in nfa["symbols"]:
            if new_transitions[state].get(s):
                row += f"{str(new_transitions[state][s]):^12} | "
            else:
                row += f"{'Ø':^12} | "
        print(row)


# _____________________________MAIN____________________________________________________#


def main():
    print("=" * 50)
    print("ε-NFA to NFA Converter (Student Version)")
    print("=" * 50)

    while True:
        nfa = read_nfa()

        if not check_for_epsilon_transitions(nfa):
            print("\nℹ No ε-transitions found.")
            print("This is already a valid NFA.")
        else:
            closures = calculate_all_epsilon_closures(nfa)
            print("\nEpsilon Closures:")
            for state in closures:
                print(f"ε-closure({state}) = {closures[state]}")

            new_transitions = calculate_new_transitions(nfa, closures)
            new_final_states = determine_new_final_states(nfa, closures)

            display_nfa(nfa, new_transitions, new_final_states)

            print("\n ε-transitions removed successfully!")

        choice = input("\nDo you want to convert another NFA? (y/n): ").strip().lower()
        if choice != "y":
            print("\nExiting. Goodbye!")
            break


# Run Program
if __name__ == "__main__":
    main()
