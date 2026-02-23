# framebuf2: micropython framebuffer extensions
# (c) 2022-2023 Peter Lumb (peter-l5)
# MIT License - https://github.com/peter-l5/framebuf2

import framebuf

MONO_VLSB = framebuf.MONO_VLSB
MONO_HLSB = framebuf.MONO_HLSB
MONO_HMSB = framebuf.MONO_HMSB
RGB565 = framebuf.RGB565
GS2_HMSB = framebuf.GS2_HMSB
GS4_HMSB = framebuf.GS4_HMSB
GS8 = framebuf.GS8


class FrameBuffer(framebuf.FrameBuffer):
    def large_text(self, s, x, y, m, c=1, r=0, t=None):
        """
        Large text drawing using standard 8x8 font.
        s: text string
        x, y: coordinates
        m: size multiple (2 = 16x16, 3 = 24x24, etc.)
        c: color (default 1)
        r: rotation 0/90/180/270 degrees
        t: character rotation
        """
        def _reverse(s):
            return s[::-1]

        colour = c
        smallbuffer = bytearray(8)
        letter = framebuf.FrameBuffer(smallbuffer, 8, 8, framebuf.MONO_HMSB)
        r = r % 360 // 90
        dx = 8 * m if r in (0, 2) else 0
        dy = 8 * m if r in (1, 3) else 0
        if r in (2, 3):
            s = _reverse(s)
        t = r if t is None else t % 360 // 90
        a, b, c, d = 1, 0, 0, 1
        for i in range(0, t):
            a, b, c, d = c, d, -a, -b
        x0 = 0 if a + c > 0 else 7
        y0 = 0 if b + d > 0 else 7
        for character in s:
            letter.fill(0)
            letter.text(character, 0, 0, 1)
            for i in range(0, 8):
                for j in range(0, 8):
                    if letter.pixel(i, j) == 1:
                        p = x0 + a * i + c * j
                        q = y0 + b * i + d * j
                        if m == 1:
                            self.pixel(x + p, y + q, colour)
                        else:
                            self.fill_rect(x + p * m, y + q * m, m, m, colour)
            x += dx
            y += dy
