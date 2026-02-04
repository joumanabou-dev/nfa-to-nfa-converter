class NFA:
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()
        self.epsilon = "ε"

    def add_state(self, state):
        """Add a new state"""
        self.states.add(state)

    def add_symbol(self, symbol):
        """Add a symbol to the alphabet"""
        if symbol != self.epsilon:
            self.alphabet.add(symbol)

    def add_transition(self, from_state, symbol, to_state):
        """Add a transition"""
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = set()
        self.transitions[from_state][symbol].add(to_state)


def read_nfa():
    """Task 1: Read NFA from user"""
    nfa = NFA()

    print("=== Enter NFA ===")

    # Input states
    states_input = input("Enter states (space-separated, e.g., q0 q1 q2): ")
    states = states_input.split()
    for state in states:
        nfa.add_state(state)

    # Input alphabet
    alphabet_input = input("Enter alphabet (space-separated, e.g., a b): ")
    symbols = alphabet_input.split()
    for symbol in symbols:
        nfa.add_symbol(symbol)

    # Input start state
    nfa.start_state = input("Enter start state: ")

    # Input final states
    final_input = input("Enter final states (space-separated): ")
    final_states = final_input.split()
    for state in final_states:
        nfa.final_states.add(state)

    # Input transitions
    print("\nEnter transitions (type 'done' when finished):")
    print("Format: from_state symbol to_state")
    print("Example: q0 a q1")
    print("For ε-transition, use 'e' or 'epsilon'")

    while True:
        transition_input = input("> ")
        if transition_input.lower() == "done":
            break

        parts = transition_input.split()
        if len(parts) != 3:
            print("Format error. Try again.")
            continue

        from_state, symbol_str, to_state = parts

        # Handle epsilon symbol
        if symbol_str in ["e", "epsilon", "ε"]:
            symbol = nfa.epsilon
        else:
            symbol = symbol_str
            nfa.add_symbol(symbol)

        nfa.add_transition(from_state, symbol, to_state)

    return nfa


def epsilon_closure(nfa, state, visited=None):
    """Task 2: Calculate epsilon closure for a given state"""
    if visited is None:
        visited = set()

    # Closure includes the state itself
    closure = {state}

    # If we've visited this state before, no need to search again
    if state in visited:
        return closure
    visited.add(state)

    # Find all epsilon transitions from this state
    if state in nfa.transitions and nfa.epsilon in nfa.transitions[state]:
        for next_state in nfa.transitions[state][nfa.epsilon]:
            # Recursively find epsilon closure of next state
            closure.update(epsilon_closure(nfa, next_state, visited))

    return closure


def compute_all_epsilon_closures(nfa):
    """Compute epsilon closure for all states"""
    closures = {}
    for state in nfa.states:
        closures[state] = epsilon_closure(nfa, state)

    # Display results
    print("\n=== Epsilon Closures for Each State ===")
    for state in sorted(closures.keys()):
        print(f"ε-closure({state}) = {sorted(closures[state])}")

    return closures


def compute_new_transitions(nfa, closures):
    """Task 3: Compute new transitions without epsilon"""
    new_transitions = {}

    # For each state in original NFA
    for state in nfa.states:
        if state not in new_transitions:
            new_transitions[state] = {}

        # For each symbol in alphabet (without epsilon)
        for symbol in nfa.alphabet:
            new_transitions[state][symbol] = set()

            # For each state in epsilon closure of current state
            for closure_state in closures[state]:
                # If there's a transition with symbol from closure state
                if (
                    closure_state in nfa.transitions
                    and symbol in nfa.transitions[closure_state]
                ):
                    # Add all target states
                    for target_state in nfa.transitions[closure_state][symbol]:
                        # Add epsilon closure of target state
                        new_transitions[state][symbol].update(closures[target_state])

    return new_transitions


def compute_new_final_states(nfa, closures):
    """Task 4: Determine new final states"""
    new_final_states = set()

    # A state is final if its epsilon closure contains a final state
    for state in nfa.states:
        for final_state in nfa.final_states:
            if final_state in closures[state]:
                new_final_states.add(state)
                break

    return new_final_states


def display_new_automaton(nfa, new_transitions, new_final_states):
    """Task 5: Display the new automaton without epsilon"""
    print("\n" + "=" * 50)
    print("New NFA without ε-transitions")
    print("=" * 50)

    print(f"\n1. States: {sorted(nfa.states)}")
    print(f"2. Alphabet: {sorted(nfa.alphabet)}")
    print(f"3. Start State: {nfa.start_state}")
    print(f"4. Final States: {sorted(new_final_states)}")

    print("\n5. Transition Table:")
    print("-" * 40)

    # Display transition table in organized format
    header = "State | " + " | ".join(sorted(nfa.alphabet))
    print(header)
    print("-" * len(header))

    for state in sorted(nfa.states):
        row = f"{state:^6}"
        for symbol in sorted(nfa.alphabet):
            if (
                state in new_transitions
                and symbol in new_transitions[state]
                and new_transitions[state][symbol]
            ):
                targets = sorted(new_transitions[state][symbol])
                row += f" | {targets}"
            else:
                row += " | {}"
        print(row)


def main():
    """Main function coordinating all tasks"""
    print("Lab: Removing ε-transitions from NFA")
    print("=" * 50)

    # Task 1: Read NFA
    nfa = read_nfa()

    # Task 2: Compute epsilon closure for each state
    closures = compute_all_epsilon_closures(nfa)

    # Task 3: Compute new transitions
    new_transitions = compute_new_transitions(nfa, closures)

    # Task 4: Determine new final states
    new_final_states = compute_new_final_states(nfa, closures)

    # Task 5: Display new automaton
    display_new_automaton(nfa, new_transitions, new_final_states)

    print("\n" + "=" * 50)
    print("NFA successfully converted!")
    print("=" * 50)


# Example run with test data
def run_example():
    """Run a test example without user input"""
    print("Example Run:")
    print("=" * 50)

    nfa = NFA()

    # Simple example from automata theory
    nfa.states = {"q0", "q1", "q2"}
    nfa.alphabet = {"a", "b"}
    nfa.start_state = "q0"
    nfa.final_states = {"q2"}

    # Add transitions
    nfa.add_transition("q0", "ε", "q1")
    nfa.add_transition("q0", "a", "q0")
    nfa.add_transition("q1", "ε", "q2")
    nfa.add_transition("q1", "b", "q1")
    nfa.add_transition("q2", "a", "q2")
    nfa.add_transition("q2", "b", "q2")

    print(f"States: {sorted(nfa.states)}")
    print(f"Alphabet: {sorted(nfa.alphabet)}")
    print(f"Start State: {nfa.start_state}")
    print(f"Final States: {sorted(nfa.final_states)}")

    # Compute epsilon closures
    closures = compute_all_epsilon_closures(nfa)

    # Compute new transitions
    new_transitions = compute_new_transitions(nfa, closures)

    # Determine new final states
    new_final_states = compute_new_final_states(nfa, closures)

    # Display new automaton
    display_new_automaton(nfa, new_transitions, new_final_states)


if __name__ == "__main__":
    print("Select mode:")
    print("1. Manual input")
    print("2. Run test example")

    choice = input("Enter option number (1 or 2): ")

    if choice == "1":
        main()
    elif choice == "2":
        run_example()
    else:
        print("Invalid choice. Running manual mode...")
        main()
