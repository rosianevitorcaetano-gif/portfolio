#!/usr/bin/env python3
"""ITIL Path card illustration, grown-up manga style (waist-up character with a whiteboard).

usage: python3 tools/make_itil_art.py src/assets/itil
Writes cds.svg for card 01. Cards 02-04 use other pictures.
"""
import os
import sys

# line colours per material, thinner than the chibi set
L_SKIN, L_HAIR, L_CLOTH, L_OBJ = "#a5675a", "#1b1210", "#262a4a", "#2b2b38"
SKIN, SKIN_SH = "#f7d7c4", "#e8b39d"
HAIR, HAIR_SH, HAIR_HI = "#2f211d", "#1d1412", "#5e423a"
WHITE, WHITE_SH = "#ffffff", "#e3e8f0"
MOD = {"cds": "#818cf8", "msf": "#22d3ee", "pic": "#fbbf24", "dpi": "#f472b6"}

_clip = 0


def line(d, color, sw, extra=""):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def shape(d, fill, stroke, sw=2, extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extra}/>')


def shaded(d, fill, stroke, sw=2, shadows=(), shade=None, extra_inside=""):
    """Fill, clipped cel shadows (and any extra inner detail), then the outline on top."""
    global _clip
    _clip += 1
    cid = f"c{_clip}"
    s = f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{fill}"/>'
    inner = "".join(f'<path d="{sd}" fill="{shade}"/>' for sd in shadows) + extra_inside
    if inner:
        s += f'<g clip-path="url(#{cid})">{inner}</g>'
    return s + (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" '
                f'stroke-linejoin="round" stroke-linecap="round"/>')


# ----------------------------------------------------------------------------- character
def back_hair(cx=115):
    d = (f"M70 100 C64 52 96 32 116 32 C140 32 170 52 162 104 "
         f"C160 142 174 172 180 206 C186 240 178 270 188 300 L42 300 "
         f"C52 270 44 240 50 206 C56 172 72 142 70 100 Z")
    return shaded(d, HAIR, L_HAIR, 2, ["M132 30 C168 52 170 140 178 200 C184 236 182 268 196 300 L240 300 L240 0 Z"], HAIR_SH)


def neck():
    d = "M107.5 140 L107 181 Q115 186 123 181 L122.5 140 Z"
    return shaded(d, SKIN, L_SKIN, 1.8, ["M100 142 Q115 162 130 142 L130 158 Q115 170 100 158 Z"], SKIN_SH)


def face():
    d = ("M84 94 C84 122 90 138 103 149 C108 153 112 155 115 155 C118 155 122 153 127 149 "
         "C140 138 146 122 146 94 C146 68 132 56 115 56 C98 56 84 68 84 94 Z")
    return shaded(d, SKIN, L_SKIN, 1.8, [
        "M137 94 C144 118 138 140 121 155 L152 160 L152 90 Z",          # right side of the face
        "M80 84 C100 94 124 90 152 84 L152 70 L80 70 Z",                # under the fringe
    ], SKIN_SH)


def eye(cx, outer, cy=110):
    """Almond eye. outer = -1 for the left eye (outer corner on the left), +1 for the right."""
    global _clip
    ox, ix = cx + outer * 11, cx - outer * 10          # outer and inner corners
    white = f"M{ox} {cy + 1.5} Q{cx - outer} {cy - 14} {ix} {cy - 0.5} Q{cx} {cy + 8.5} {ox} {cy + 1.5} Z"
    _clip += 1
    cid = f"c{_clip}"
    s = f'<clipPath id="{cid}"><path d="{white}"/></clipPath><path d="{white}" fill="#fbf8f6"/>'
    s += (f'<g clip-path="url(#{cid})"><circle cx="{cx}" cy="{cy + 0.5}" r="6.9" fill="url(#iris)"/>'
          f'<circle cx="{cx}" cy="{cy + 1}" r="3" fill="#160d09"/>'
          f'<circle cx="{cx - 2.5}" cy="{cy - 2.2}" r="2.2" fill="#ffffff"/>'
          f'<circle cx="{cx + 2.7}" cy="{cy + 3}" r="0.9" fill="#ffffff" opacity="0.85"/>'
          f'<path d="M{ox - 2} {cy - 14} L{ix + 2} {cy - 14} L{ix} {cy - 1.5} Q{cx} {cy - 9} {ox} {cy} Z" fill="#000" opacity="0.1"/></g>')
    s += line(f"M{ox} {cy + 1.5} Q{cx - outer * 1} {cy - 14} {ix} {cy - 0.5}", L_HAIR, 3)        # upper lash line
    s += line(f"M{ox} {cy + 1.5} l{outer * 3.6} -1.2", L_HAIR, 2.2)                              # outer flick
    s += line(f"M{ox - outer * 1.5} {cy + 3.5} Q{cx} {cy + 8} {ix + outer * 3} {cy + 3.5}", "#9b6556", 1)  # lower lash
    s += line(f"M{ox - outer * 1} {cy - 6} Q{cx} {cy - 15.5} {ix + outer * 1.5} {cy - 8}", "#c08a78", 1)   # crease
    return s


def features():
    s = eye(100, -1) + eye(130, 1)
    s += line("M87 96 Q98 90.5 110 93.5", "#3a2622", 2.1) + line("M120 93.5 Q132 90.5 143 96", "#3a2622", 2.1)
    s += line("M117 113 L115.6 124.5 Q117 126.5 119.4 125.6", "#c58b78", 1.4)                  # nose
    s += f'<path d="M108.5 138.6 Q115 143.8 121.5 138.6 Q115 140.6 108.5 138.6 Z" fill="#e4877f" opacity="0.85"/>'
    s += line("M107 137.6 Q115 141.2 123 137.6", "#9c4f4f", 1.6)                                 # lips
    s += line("M106.2 137 q-1.3 0.1 -1.9 -0.9 M123.8 137 q1.3 0.1 1.9 -0.9", "#9c4f4f", 1.1)   # smile corners
    s += '<ellipse cx="95" cy="125" rx="7" ry="3.4" fill="#f29f9a" opacity="0.18"/>'
    s += '<ellipse cx="135" cy="125" rx="7" ry="3.4" fill="#f29f9a" opacity="0.18"/>'
    return s


def bangs():
    d = ("M82 98 C78 62 96 42 118 42 C142 42 160 60 152 104 "
         "Q149 94 146 87 Q144 96 141 101 Q138 88 134 80 Q132 88 128 92 "
         "Q124 80 118 71 Q112 66 106 66 Q103 78 98 88 Q95 82 92 78 Q90 88 86 95 Q84 96 82 98 Z")
    s = shaded(d, HAIR, L_HAIR, 2, ["M128 42 C150 50 160 72 152 104 L200 104 L200 30 Z"], HAIR_SH)
    s += line("M92 56 Q106 48 122 48", HAIR_HI, 2.4) + line("M128 50 Q140 54 146 62", HAIR_HI, 2.4)
    s += line("M118 60 Q128 66 134 78 M124 56 Q136 62 142 74", "#4a3530", 1.4)
    return s


def side_locks():
    left = ("M84 96 C78 128 80 160 72 192 C66 214 72 236 62 256 "
            "C76 244 82 220 86 200 C90 176 88 134 88 104 Z")
    right = ("M146 96 C152 128 150 160 158 192 C164 214 158 236 168 256 "
             "C154 244 148 220 144 200 C140 176 142 134 142 104 Z")
    s = shaded(left, HAIR, L_HAIR, 2)
    s += shaded(right, HAIR, L_HAIR, 2, ["M150 100 L172 100 L172 260 L156 260 Z"], HAIR_SH)
    s += line("M86 120 C84 150 80 180 72 214 M144 120 C146 150 150 180 158 214", "#4a3530", 1.3)
    return s


def blazer(base, shadow, lapel):
    s = ""
    # sleeve hanging on the left side (cropped by the frame)
    s += shaded("M60 198 C46 214 44 262 46 300 L68 300 C66 266 68 230 72 210 Z", base, L_CLOTH, 2,
                ["M60 198 C52 214 50 262 52 300 L46 300 L40 200 Z"], shadow)
    body = "M58 198 C64 190 86 182 104 178 L115 232 L126 178 C146 182 166 190 172 198 L178 300 L52 300 Z"
    s += shaded(body, base, L_CLOTH, 2, ["M140 186 C160 194 172 200 172 210 L178 300 L146 300 Z"], shadow)
    s += shape("M104 178 L94 198 L105 203 L115 232 Z", lapel, L_CLOTH, 1.8)
    s += shape("M126 178 L136 198 L125 203 L115 232 Z", lapel, L_CLOTH, 1.8)
    s += f'<circle cx="115" cy="266" r="3" fill="{shadow}" stroke="{L_CLOTH}" stroke-width="1.4"/>'
    return s


def blouse():
    s = shaded("M104 178 L115 232 L126 178 Q115 171 104 178 Z", WHITE, L_CLOTH, 1.6, ["M117 178 L128 178 L117 232 Z"], WHITE_SH)
    s += shape("M104 178 L109 192 L115 184 Z", WHITE, L_CLOTH, 1.4) + shape("M126 178 L121 192 L115 184 Z", WHITE, L_CLOTH, 1.4)
    s += line("M108 185 Q115 194 122 185", "#c9a24a", 1.1) + '<circle cx="115" cy="193.6" r="2" fill="#e0b84f" stroke="#a07c2a" stroke-width="0.8"/>'
    return s


def raised_arm_with_pen(base, shadow, pen_color):
    s = shaded("M166 200 C182 210 192 236 196 262 L178 272 C176 248 168 228 158 214 Z", base, L_CLOTH, 2,
               ["M184 210 C192 230 196 248 196 262 L186 266 Z"], shadow)                       # upper arm
    s += shaded("M182 270 C190 244 198 222 205 206 L222 212 C216 230 208 252 198 276 Z", base, L_CLOTH, 2,
                ["M214 210 L224 212 L200 280 L192 276 Z"], shadow)                               # forearm
    s += shape("M203 206 L222 213 L219 220 L201 213 Z", WHITE, L_CLOTH, 1.5)                     # cuff
    s += line("M219 190 L240 164", L_OBJ, 5.2) + line("M219 190 L240 164", pen_color, 3.4)       # pen
    s += line("M240 164 L243 160", L_OBJ, 2.2)
    s += shaded("M205 205 C202 197 207 189 215 188 L224 190 C229 192 229 199 225 203 L219 209 C214 212 208 210 205 205 Z", SKIN, L_SKIN, 1.6,
                ["M221 196 C226 197 229 194 229 192 L232 210 L216 212 Z"], SKIN_SH)              # hand
    s += line("M213 190 C216 186.5 221 186.5 224 190", L_SKIN, 1.3)                             # thumb over the pen
    s += line("M208.5 197 Q214 195.6 220 197.6 M207.6 202 Q212.6 200.8 218 202.6", L_SKIN, 1.1)  # fingers
    return s


def character_cds():
    ind, ind_sh, ind_lapel = "#4349a8", "#343a8c", "#525ab8"
    s = back_hair() + neck() + blazer(ind, ind_sh, ind_lapel) + blouse()
    s += face() + features() + bangs() + side_locks()
    s += raised_arm_with_pen(ind, ind_sh, MOD["cds"])
    return s


# ----------------------------------------------------------------------------- scenes
def svg(inner, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300" role="img" aria-label="{label}">
  <!-- Original illustration drawn for the ITIL Path cards of Rosiane's portfolio. Free to use. -->
  <defs>
    <linearGradient id="iris" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2b190f"/><stop offset="1" stop-color="#9b6a47"/>
    </linearGradient>
  </defs>
{inner}
</svg>
'''


def board(x, y, w, h):
    s = shape(f"M{x + 8} {y} H{x + w - 8} Q{x + w} {y} {x + w} {y + 8} V{y + h - 8} Q{x + w} {y + h} {x + w - 8} {y + h} "
              f"H{x + 8} Q{x} {y + h} {x} {y + h - 8} V{y + 8} Q{x} {y} {x + 8} {y} Z", "#f8fafc", L_OBJ, 2)
    return s


def scene_cds():
    s = f'<circle cx="112" cy="176" r="118" fill="{MOD["cds"]}" opacity="0.1"/>'
    bx, by, bw, bh = 228, 34, 160, 204
    s += board(bx, by, bw, bh)
    s += line(f"M{bx + 16} {by + 22} h58 M{bx + 16} {by + 33} h36", "#a3adbd", 3.2)
    xs = [bx + 14 + i * 36 for i in range(4)]
    for x, key in zip(xs, ("cds", "msf", "pic", "dpi")):
        s += shape(f"M{x + 5} {by + 58} H{x + 21} Q{x + 26} {by + 58} {x + 26} {by + 63} V{by + 79} Q{x + 26} {by + 84} {x + 21} {by + 84} "
                   f"H{x + 5} Q{x} {by + 84} {x} {by + 79} V{by + 63} Q{x} {by + 58} {x + 5} {by + 58} Z", MOD[key], L_OBJ, 1.8)
    for i, x in enumerate(xs):
        s += (f'<text x="{x + 13}" y="{by + 76}" font-family="Helvetica, Arial, sans-serif" font-size="12" '
              f'font-weight="700" fill="#1f2937" text-anchor="middle">{i + 1}</text>')
    for x in xs[:3]:
        s += line(f"M{x + 28} {by + 71} h6 M{x + 31} {by + 68} l3 3 l-3 3", L_OBJ, 1.8)
    s += line(f"M{xs[3] + 13} {by + 88} V{by + 104} H{xs[0] + 13} V{by + 90} M{xs[0] + 10} {by + 94} L{xs[0] + 13} {by + 89} L{xs[0] + 16} {by + 94}",
              "#4f46e5", 1.8, 'stroke-dasharray="4 4"')
    s += line(f"M{bx + 16} {by + 128} h96 M{bx + 16} {by + 140} h78 M{bx + 16} {by + 152} h88", "#d3d9e3", 3)
    s += (f'<g transform="rotate(5 {bx + 128} {by + 150})"><rect x="{bx + 112}" y="{by + 132}" width="34" height="32" rx="2" '
          f'fill="#fde68a" stroke="{L_OBJ}" stroke-width="1.6"/><path d="M{bx + 118} {by + 143} h20 M{bx + 118} {by + 151} h13" '
          f'stroke="#b45309" stroke-width="2" stroke-linecap="round"/></g>')
    s += character_cds()
    return svg(s, "Manga-style drawing of Rosiane in a blazer, presenting the four steps of the path on a whiteboard")


SCENES = {"cds": scene_cds}


def main():
    out = sys.argv[1]
    names = sys.argv[2:] or list(SCENES)
    os.makedirs(out, exist_ok=True)
    for name in names:
        with open(os.path.join(out, f"{name}.svg"), "w") as f:
            f.write(SCENES[name]())
        print("wrote", name)


if __name__ == "__main__":
    main()
