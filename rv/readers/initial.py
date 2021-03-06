from rv.readers.reader import Reader, ReaderFinished
from rv.readers.sunsynth import SunSynthReader
from rv.readers.sunvox import SunVoxReader


class InitialReader(Reader):
    def process_svox(self, _):
        self.object = SunVoxReader(self.f).object

    def process_ssyn(self, _):
        self.object = SunSynthReader(self.f).object

    def process_end_of_file(self):
        raise ReaderFinished()
