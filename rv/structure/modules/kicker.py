from enum import IntEnum

from rv.structure.controller import Controller
from rv.structure.module import GenericModule


class Waveform(IntEnum):

    TRIANGLE = 0
    SQUARE = 1


class KickerModule(GenericModule):

    class controller_types:
        volume = Controller(0x01, (0, 256))
        waveform = Controller(0x02, Waveform)
        panning = Controller(0x03, (-128, 128))
        attack = Controller(0x04, (0, 512))
        release = Controller(0x05, (0, 512))
        vol_addition = Controller(0x06, (0, 1024))
        env_acceleration = Controller(0x07, (0, 1024))
        polyphony_ch = Controller(0x08, (1, 4))
        anticlick = Controller(0x09, bool)