from .waveform import WaveformChunk


class DirtyWaveformChunk(WaveformChunk):

    fixed_length = 32
    fixed_format = WaveformChunk.Format.mono_8bit
    fixed_freq = 44100

    default = [
        0x00,
        0x9C,
        0xA6,
        0x00,
        0x5A,
        0x89,
        0xEC,
        0x2D,
        0x02,
        0xEC,
        0x6F,
        0xE9,
        0x02,
        0x9E,
        0x3C,
        0x20,
        0x64,
        0x32,
        0x00,
        0xCE,
        0x41,
        0x62,
        0x32,
        0x20,
        0xA6,
        0x88,
        0x64,
        0x5A,
        0x3B,
        0x15,
        0x00,
        0x36,
    ]


__all__ = ["DirtyWaveformChunk"]
