"""
Project 79 — Finite State Machine (FSM) Engine + Simulator

Run:
    python fsm_engine.py

Features:
- Define states with entry/exit actions
- Define transitions triggered by events
- Run a continuous or manual-step FSM
- Persist current state in state.db (simple text)
- Traffic light demo FSM included
"""

import time
import os


STATE_FILE = "state.db"


class State:
    def __init__(self, name, on_enter=None, on_exit=None):
        self.name = name
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.transitions = {}   # event -> next_state_name

    def add_transition(self, event, next_state):
        self.transitions[event] = next_state


class FSM:
    def __init__(self, initial):
        self.states = {}
        self.current = initial

    def add_state(self, state):
        self.states[state.name] = state

    def trigger(self, event):
        state = self.states[self.current]
        if event not in state.transitions:
            return f"No transition for event '{event}' in state '{self.current}'"

        next_state_name = state.transitions[event]
        next_state = self.states[next_state_name]

        # exit action
        if state.on_exit:
            state.on_exit(self.current)

        # change state
        self.current = next_state_name

        # enter action
        if next_state.on_enter:
            next_state.on_enter(self.current)
        self.save_state()
        return f"Transitioned to {self.current}"

    def save_state(self):
        with open(STATE_FILE, "w") as f:
            f.write(self.current)

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                self.current = f.read().strip()


# ------------------------------
# Traffic Light Demo FSM
# ------------------------------

def on_enter(state):
    print(f"[ENTER] {state}")

def on_exit(state):
    print(f"[EXIT] {state}")

def build_traffic_light_fsm():
    fsm = FSM("RED")
