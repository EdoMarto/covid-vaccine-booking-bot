from datetime import datetime

from vaccine_bot.models import Slot


def test_slots_sort_by_time():
    a = Slot("Padova Fiera", datetime(2021, 6, 2, 9, 0))
    b = Slot("Padova Fiera", datetime(2021, 6, 1, 15, 30))
    assert sorted([a, b], key=lambda s: s.when)[0] is b


def test_slot_str_is_human_readable():
    slot = Slot("Padova Fiera", datetime(2021, 6, 1, 15, 30))
    assert str(slot) == "01/06/2021 15:30 @ Padova Fiera"
