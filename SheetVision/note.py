from rectangle import Rectangle

note_step = 0.0625

note_defs = {
     -5: ("g5", 91),
     -4: ("f5", 89),
     -3: ("e5", 87),
     -2: ("d5", 86),
     -1: ("c5", 84),
      0: ("b5", 82),
      1: ("a4", 81),
      2: ("g4", 79),
      3: ("f4", 77),
      4: ("e4", 75),
      5: ("d4", 74),
      6: ("c4", 72),
      7: ("b4", 70),
      8: ("a3", 69),
      9: ("g3", 67),
     10: ("f3", 65),
     11: ("e3", 63),
     12: ("d3", 62),
     13: ("c3", 60),
     14: ("b3", 58),
     15: ("a2", 57),
     16: ("g2", 55),
     17: ("f2", 53),
}

class Note(object):
    def __init__(self, rec, sym, staff_rec, sharp_notes = [], flat_notes = []):
        self.rec = rec
        self.sym = sym

        middle = rec.y + (rec.h / 2.0)
        height = (middle - staff_rec.y) / staff_rec.h
        note_def = note_defs[int(height/note_step + 0.5)]
        self.note = note_def[0]
        self.pitch = note_def[1]

        #if any(n for n in sharp_notes if n.note == self.note):
        #    self.note += "#"
        #    self.pitch += 1
        #if any(n for n in flat_notes if n.note == self.note):
        #    self.note += "b"
        #    self.pitch -= 1
        
    def set_key(self, key_sharps = [], key_flats = []):
        '''
        조표에 있는 sharp과 flat을 받아 note들에 sharp으로 된 조표 적용
        '''
        if any(sharp for sharp in key_sharps if sharp.note[0] == self.note[0]):
            self.note += "#"
            self.pitch += 1
        if any(flat for flat in key_flats if flat.note == self.note):
            self.note += "b"
            self.pitch -= 1


