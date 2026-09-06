"""Tests for AppState (observer pattern + thread-safe event queue)."""

import gc

from app.models.app_state import AppState


def test_initialization():
    state = AppState()
    assert state.selected_algorithm == "BERTopic"
    assert state.current_result is None
    assert state.analysis_in_progress is False
    assert state.analysis_error is None


def test_subscribe_and_notify():
    state = AppState()
    calls = []
    state.subscribe(lambda s: calls.append(s))
    state.notify()
    state.process_events()
    assert len(calls) == 1
    assert calls[0] is state


def test_notify_queues_event():
    state = AppState()
    state.notify()
    assert not state.event_queue.empty()


def test_call_on_main():
    state = AppState()
    ran = []
    state.call_on_main(lambda: ran.append(True))
    state.process_events()
    assert ran == [True]


def test_weakref_pruning():
    state = AppState()

    class Subscriber:
        def __init__(self):
            self.calls = 0

        def on_change(self, state):
            self.calls += 1

    sub = Subscriber()
    state.subscribe(sub.on_change)
    state.notify()
    state.process_events()
    assert sub.calls == 1

    del sub
    gc.collect()
    state.notify()
    state.process_events()  # must not raise; dead weak ref is pruned
    assert len(state._observers) == 0
