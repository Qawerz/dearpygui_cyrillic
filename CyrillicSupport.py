import sys, os
import dearpygui.dearpygui as dpg

class CyrillicSupport:
    big_let_start = 0x00C0
    big_let_end = 0x00DF
    small_let_end = 0x00FF
    remap_big_let = 0x0410
    alph_len = big_let_end - big_let_start + 1
    alph_shift = remap_big_let - big_let_start

    def __init__(self, app_path):
        self.app_path = app_path
        self.font_path = os.path.join(self.app_path, 'fonts', 'C:/Windows/Fonts/times.ttf')
        print( self.font_path)

    def registry_font(self):
        with dpg.font_registry():
            with dpg.font(self.font_path, size=16) as font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range(0x0391, 0x03C9)
                dpg.add_font_range(0x2070, 0x209F)

                if sys.platform == 'win32':
                    self._remap_chars()
                dpg.bind_font(font)

    def _remap_chars(self):
        biglet = self.remap_big_let
        for i1 in range(self.big_let_start, self.big_let_end + 1):
            dpg.add_char_remap(i1, biglet)
            dpg.add_char_remap(i1 + self.alph_len, biglet + self.alph_len)
            biglet += 1

        dpg.add_char_remap(0x00A8, 0x0401)
        dpg.add_char_remap(0x00B8, 0x0451)

    def decode_string(self, instr: str):
        if sys.platform == 'win32':
            outstr = []
            for i in range(len(instr)):
                char_byte = ord(instr[i])
                if char_byte in range(self.big_let_start, self.small_let_end + 1):
                    char = chr(ord(instr[i]) + self.alph_shift)
                    outstr.append(char)
                elif char_byte == 0x00A8:
                    outstr.append(chr(0x0401))
                elif char_byte == 0x00B8:
                    outstr.append(chr(0x0451))
                else:
                    outstr.append(instr[i])

            return ''.join(outstr)
        else:
            return instr
