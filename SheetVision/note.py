#from rectangle import Rectangle

#note_step = 0.0625

g_note_defs = {
    -12: ("a6", 92),
    -11: ("g6", 90),
    -10: ("f6", 88),
    -9: ("e6", 87),
    -8: ("d6", 85),
    -7: ("c6", 84),
    -6: ("b5", 83),
    -5: ("a5", 81),
    -4: ("g5", 79),
    -3: ("f5", 77),
    -2: ("e5", 76),
    -1: ("d5", 74),
    0: ("c5", 72),
    1: ("b4", 71),
    2: ("a4", 69),
    3: ("g4", 67),
    4: ("f4", 65),
    5: ("e4", 64),
    6: ("d4", 62),
    7: ("c4", 60),
    8: ("b3", 59),
    9: ("a3", 57),
    10: ("g3", 55),
    11: ("f3", 53),
    12: ("e3", 52),
    13: ("d3", 50),
    14: ("c3", 48),
    15: ("b2", 47),
    16: ("a2", 45),
    17: ("g2", 43),
}
b_note_defs ={   #b,c / e,f
    -12: ("c5", 72),
    -11: ("b4", 71),
    -10: ("a4", 69),
    -9: ("g4", 67),
    -8: ("f4", 65),
    -7: ("e4", 64),
    -6: ("d4", 62),
    -5: ("c4", 60),
    -4: ("b4", 59),
    -3: ("a3", 57),
    -2: ("g3", 55),
    -1: ("f3", 53),
    0: ("e3", 52),
    1: ("d3", 50),
    2: ("c3", 48),
    3: ("b2", 47),
    4: ("a2", 45),
    5: ("g2", 43),
    6: ("f2", 41),
    7: ("e2", 40),
    8: ("d2", 38),
    9: ("c2", 36),
    10: ("b1", 35),
    11: ("a1", 33),
    12: ("g1", 31),
    13: ("f1", 29),
    14: ("e1", 28),
    15: ("d1", 26),
    16: ("c1", 24),
    17: ("b0", 23),
}
#note_defs = {
#     -5: ("g5", 91),
#     -4: ("f5", 89),
#     -3: ("e5", 87),
#     -2: ("d5", 86),
#     -1: ("c5", 84),
#      0: ("b5", 82),
#      1: ("a4", 81),
#      2: ("g4", 79),
#      3: ("f4", 77),
#      4: ("e4", 75),
#      5: ("d4", 74),
#      6: ("c4", 72),
#      7: ("b4", 70),
#      8: ("a3", 69),
#      9: ("g3", 67),
#     10: ("f3", 65),
#     11: ("e3", 63),
#     12: ("d3", 62),
#     13: ("c3", 60),
#     14: ("b3", 58),
#     15: ("a2", 57),
#     16: ("g2", 55),
#     17: ("f2", 53),
#}

#class Note(object):
#    def __init__(self, rec, sym, staff_rec, sharp_notes = [], flat_notes = []):
#        self.rec = rec
#        self.sym = sym
#        self.middle = rec.y + (rec.h / 2.0)
#        self.height = (self.middle - staff_rec.y) / staff_rec.h

#        middle = rec.y + (rec.h / 2.0)
#        height = (middle - staff_rec.y) / staff_rec.h
#        note_def = note_defs[int(height/note_step + 0.5)]
#        self.note = note_def[0]
#        self.pitch = note_def[1]

#        #if any(n for n in sharp_notes if n.note == self.note):
#        #    self.note += "#"
#        #    self.pitch += 1
#        #if any(n for n in flat_notes if n.note == self.note):
#        #    self.note += "b"
#        #    self.pitch -= 1
        
#    def set_key(self, isGclef, key_sharps = [], key_flats = [], sharp_notes = [], flat_notes = []):
#        '''
#        조표에 있는 sharp과 flat을 받아 note들에 sharp으로 된 조표 적용
#        '''
#        if isGclef == True:  # 높은 음자리표
#            note_def = g_note_defs[int((self.height / note_step + 0.5) - 5)]
#        else:  # 낮은 음자리표
#            note_def = b_note_defs[int((self.height / note_step + 0.5) - 5)]
#        self.note = note_def[0]
#        self.pitch = note_def[1]
#        if len(key_sharps) > 0 :
#            if len(key_sharps) == 1:
#                # 사장조
#                if self.pitch % 12 == 5:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 2:
#                # 라장조
#                if self.pitch % 12 == 5 or 0:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 3:
#                # 가장조
#                if self.pitch % 12 == 5 or 0 or 7:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 4:
#                # 마장조
#                if self.pitch % 12 == 5 or 0 or 7 or 2:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 5:
#                # 나장조
#                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 6:
#                # 올림바장조
#                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9 or 4:
#                    self.note += "#"
#                    self.pitch += 1
#            elif len(key_sharps) == 7:
#                # 올림다장조
#                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9 or 4 or 11:
#                    self.note += "#"
#                    self.pitch += 1
#        elif len(key_flats) > 0:
#            if len(key_flats) == 1:
#                # 바장조
#                if self.pitch % 12 == 11:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 2:
#                # 내림나장조
#                if self.pitch % 12 == 11 or 4:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 3:
#                # 내림마장조
#                if self.pitch % 12 == 11 or 4 or 9:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 4:
#                # 내림가장조
#                if self.pitch % 12 == 11 or 4 or 9 or 2:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 5:
#                # 내림라장조
#                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 6:
#                # 내림사장조
#                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7 or 0:
#                    self.note += "b"
#                    self.pitch -= 1
#            elif len(key_flats) == 7:
#                # 내림다장조
#                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7 or 0 or 5:
#                    self.note += "b"
#                    self.pitch -= 1
#        if any(n for n in sharp_notes if n.note[0] == self.note[0]):
#            self.note += "#"
#            self.pitch += 1	
#        if any(flat for flat in key_flats if flat.note[0] == self.note[0]):
#            self.note += "b"
#            self.pitch -= 1	


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
        self.middle = rec.y + (rec.h / 2.0)
        self.height = (self.middle - staff_rec.y) / staff_rec.h
        if sym in ["sharp","flat","4","8","2","1"]:
            x, middle_y=staff_rec.middle
            flag=(self.rec.y-middle_y)/(staff_rec.h/12)
            flag+=0.25
            flag//=0.5
            flag+=8
            note_def=note_defs[flag]
            self.note = note_def[0]
            self.pitch = note_def[1]

        #if any(n for n in sharp_notes if n.note == self.note):
        #    self.note += "#"
        #    self.pitch += 1
        #if any(n for n in flat_notes if n.note == self.note):
        #    self.note += "b"
        #    self.pitch -= 1
        
    def set_key(self, isGclef, key_sharps = [], key_flats = [], sharp_notes = [], flat_notes = []):
        '''
        조표에 있는 sharp과 flat을 받아 note들에 sharp으로 된 조표 적용
        '''
        if isGclef == True:  # 높은 음자리표
            note_def = g_note_defs[int((self.height / note_step + 0.5) - 5)]
        else:  # 낮은 음자리표
            note_def = b_note_defs[int((self.height / note_step + 0.5) - 5)]
        self.note = note_def[0]
        self.pitch = note_def[1]
        if len(key_sharps) > 0 :
            if len(key_sharps) == 1:
                # 사장조
                if self.pitch % 12 == 5:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 2:
                # 라장조
                if self.pitch % 12 == 5 or 0:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 3:
                # 가장조
                if self.pitch % 12 == 5 or 0 or 7:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 4:
                # 마장조
                if self.pitch % 12 == 5 or 0 or 7 or 2:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 5:
                # 나장조
                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 6:
                # 올림바장조
                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9 or 4:
                    self.note += "#"
                    self.pitch += 1
            elif len(key_sharps) == 7:
                # 올림다장조
                if self.pitch % 12 == 5 or 0 or 7 or 2 or 9 or 4 or 11:
                    self.note += "#"
                    self.pitch += 1
        elif len(key_flats) > 0:
            if len(key_flats) == 1:
                # 바장조
                if self.pitch % 12 == 11:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 2:
                # 내림나장조
                if self.pitch % 12 == 11 or 4:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 3:
                # 내림마장조
                if self.pitch % 12 == 11 or 4 or 9:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 4:
                # 내림가장조
                if self.pitch % 12 == 11 or 4 or 9 or 2:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 5:
                # 내림라장조
                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 6:
                # 내림사장조
                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7 or 0:
                    self.note += "b"
                    self.pitch -= 1
            elif len(key_flats) == 7:
                # 내림다장조
                if self.pitch % 12 == 11 or 4 or 9 or 2 or 7 or 0 or 5:
                    self.note += "b"
                    self.pitch -= 1
        if any(n for n in sharp_notes if n.note[0] == self.note[0]):
            self.note += "#"
            self.pitch += 1	
        if any(flat for flat in key_flats if flat.note[0] == self.note[0]):
            self.note += "b"
            self.pitch -= 1	

