from rectangle import Rectangle

note_step = 0.0625    # 오선지에서 한 칸 높이의 비율

note_defs = {
     -4 : ("g5", 79),
     -3 : ("f5", 77),
     -2 : ("e5", 76),
     -1 : ("d5", 74),
      0 : ("c5", 72),
      1 : ("b4", 71),
      2 : ("a4", 69),
      3 : ("g4", 67),
      4 : ("f4", 65),
      5 : ("e4", 64),
      6 : ("d4", 62),
      7 : ("c4", 60),
      8 : ("b3", 59),
      9 : ("a3", 57),
     10 : ("g3", 55),
     11 : ("f3", 53),
     12 : ("e3", 52),
     13 : ("d3", 50),
     14 : ("c3", 48),
     15 : ("b2", 47),
     16 : ("a2", 45),
     17 : ("f2", 53),
}

class Note(object):
    def __init__(self, rec, sym, staff_rec, sharp_notes = [], flat_notes = []):
        '''
        심볼과 오선 Rectangle 받아 음정 계산하는 class

        @param rec    Rectangle 심볼의 위치정보 담고 있는 객체
        @param sym    string 심볼 이름 
        @param staff_rec    Rectangle 오선 하나 위치 저장한 객체
        '''
        self.rec = rec    
        self.sym = sym    

        middle = rec.y + (rec.h / 2.0)    # 심볼의 y 중점 좌표
        height = (middle - staff_rec.y) / staff_rec.h    # 오선 높이에서 y중점 위치의 비율(내분점 개념?)
        note_def = note_defs[int(height/note_step + 0.5)]    # 몇 번째 칸/줄인지 계산하고, 음 높이로 변환
        self.note = note_def[0]    # 음정 string. 음표의 경우 n분 음표의 n
        self.pitch = note_def[1]   # 음정 midi에 들어가는 int
        if any(n for n in sharp_notes if n.note[0] == self.note[0]):   # 현재 음에 샾이 붙었는지 확인
            self.note += "#"
            self.pitch += 1
        if any(n for n in flat_notes if n.note[0] == self.note[0]):    # 현재 음에 플랫 붙었는지 확인
            self.note += "b"
            self.pitch -= 1


