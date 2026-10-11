#!/usr/bin/env python3
"""Project card illustrations: flat, light, one per Featured Project, in the colour of the
ITIL 4 module the project maps to.

usage: python3 tools/make_project_art.py src/assets/projects
"""
import os
import sys

O = "#2b2b38"
F = "Helvetica, Arial, sans-serif"
MOD = {  # (bright, ink, tint) as in src/itil.css
    "cds": ("#818cf8", "#4338ca", "#eef2ff"),
    "msf": ("#22d3ee", "#0e7490", "#ecfeff"),
    "pic": ("#fbbf24", "#b45309", "#fffbeb"),
    "dpi": ("#f472b6", "#be185d", "#fdf2f8"),
}


def rect(x, y, w, h, fill="#ffffff", rx=8, sw=2.2, stroke=O, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def line(d, color=O, sw=2.2, extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def shape(d, fill, sw=2.2, stroke=O):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>'


def text(x, y, s, size=12, color=O, weight=700, anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="{F}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>'


def pill(x, y, w, label, mod):
    bright, ink, tint = MOD[mod]
    return rect(x, y, w, 24, "#ffffff", 12, 1.8, ink) + text(x + w / 2, y + 16, label, 11.5, ink)


def check(cx, cy, r=13, fill="#22c55e"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{O}" stroke-width="2.2"/>'
            + line(f"M{cx - r * 0.42} {cy} L{cx - r * 0.1} {cy + r * 0.32} L{cx + r * 0.45} {cy - r * 0.35}", "#ffffff", 2.6))


def svg(mod, inner, label):
    bright, ink, tint = MOD[mod]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 235" width="400" height="235" role="img" aria-label="{label}">
  <!-- Original illustration for the Featured Projects cards. Free to use. -->
  <defs>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.2" fill="{ink}" opacity="0.12"/>
    </pattern>
  </defs>
  <rect width="400" height="235" fill="{tint}"/>
  <rect width="400" height="235" fill="url(#dots)"/>
  <circle cx="345" cy="30" r="95" fill="{bright}" opacity="0.14"/>
  <circle cx="40" cy="225" r="70" fill="{bright}" opacity="0.12"/>
{inner}
</svg>
'''


def incident():
    m = "msf"; b, ink, _ = MOD[m]
    s = rect(36, 34, 220, 160, rx=10)
    s += line("M36 58 H256")
    s += "".join(f'<circle cx="{x}" cy="46" r="3.5" fill="{c}"/>' for x, c in ((52, "#f87171"), (64, "#fbbf24"), (76, "#4ade80")))
    s += line("M56 176 H238 M56 176 V74", "#cbd5e1", 1.8)
    s += line("M58 160 L82 152 L102 156 L122 132 L138 86 L154 142 L176 146 L198 140 L220 138 L238 136", ink, 3)
    s += f'<circle cx="138" cy="86" r="9" fill="#ef4444" stroke="{O}" stroke-width="2.2"/>' + text(138, 90.5, "!", 12, "#ffffff")
    s += rect(176, 68, 40, 20, "#fee2e2", 10, 1.8) + text(196, 82, "P1", 11.5, "#b91c1c")
    # incident ticket leads to a problem record
    s += rect(278, 52, 92, 50) + text(298, 72, "INC", 12, ink, anchor="start") + line("M298 84 H350 M298 92 H336", "#cbd5e1", 3)
    s += rect(278, 132, 92, 50) + text(298, 152, "PRB", 12, ink, anchor="start") + line("M298 164 H350 M298 172 H330", "#cbd5e1", 3)
    s += line("M324 104 V126 M318 120 L324 127 L330 120", ink, 2.4)
    s += check(366, 182)
    return svg(m, s, "Incident chart with an alert and a ticket escalated to a problem record")


def decommission():
    m = "pic"; b, ink, tint = MOD[m]
    s = rect(48, 38, 160, 176, rx=10) + rect(98, 28, 60, 20, "#cbd5e1", 5)
    for i, label in enumerate(("Legal steps", "Cardholders", "Balances", "Chargebacks")):
        y = 70 + i * 34
        s += rect(66, y, 20, 20, "#ffffff", 4, 2) + line(f"M70 {y + 10} L75 {y + 15} L83 {y + 5}", ink, 2.6)
        s += text(96, y + 15, label, 13, O, 600, "start")
    s += f'<circle cx="300" cy="104" r="52" fill="#ffffff" stroke="{O}" stroke-width="2.6"/>'
    s += f'<circle cx="300" cy="104" r="40" fill="{b}" opacity="0.25"/>'
    s += line("M300 78 V102", ink, 5) + line("M285 88 A22 22 0 1 0 315 88", ink, 5)
    s += pill(246, 172, 108, "Service retired", m)
    return svg(m, s, "Checklist for a controlled service shutdown next to a power switch")


def integration():
    m = "cds"; b, ink, _ = MOD[m]
    nodes = (("Scheme", 34, 34), ("Perso bureau", 34, 166), ("Finance", 270, 34), ("Legal", 270, 166))
    s = ""
    for label, x, y in nodes:
        cx, cy = x + 48, y + 18
        s += line(f"M{cx} {cy} L200 117", ink, 2, 'stroke-dasharray="5 5"')
    for label, x, y in nodes:
        s += rect(x, y, 96, 36, rx=18) + text(x + 48, y + 23, label, 12.5, O, 600)
    s += rect(166, 83, 68, 68, b, 16, 2.6)
    s += line("M184 108 H214 M208 102 L214 108 L208 114", "#ffffff", 3) + line("M216 126 H186 M192 120 L186 126 L192 132", "#ffffff", 3)
    return svg(m, s, "Partners connected through one central integration hub")


def mining_water():
    m = "dpi"; b, ink, _ = MOD[m]
    s = shape("M58 44 C58 44 38 70 38 84 A20 20 0 0 0 78 84 C78 70 58 44 58 44 Z", "#38bdf8")
    s += rect(24, 150, 190, 22, "#cbd5e1", 6)
    s += f'<circle cx="120" cy="130" r="32" fill="#ffffff" stroke="{O}" stroke-width="2.4"/>'
    s += "".join(line(f"M{120 + 24 * c} {130 - 24 * sn} L{120 + 30 * c} {130 - 30 * sn}", O, 1.6)
                 for c, sn in ((-0.87, 0.5), (-0.5, 0.87), (0, 1), (0.5, 0.87), (0.87, 0.5)))
    s += line("M120 130 L136 112", ink, 3) + f'<circle cx="120" cy="130" r="4" fill="{O}"/>'
    s += line("M240 196 H380 M240 196 V70", "#94a3b8", 2)
    for i, (h, c) in enumerate(((110, "#fbcfe8"), (88, "#f9a8d4"), (66, b), (46, "#ec4899"))):
        x = 254 + i * 31
        s += rect(x, 196 - h, 22, h, c, 3, 2)
    s += line("M256 74 L360 140 M348 140 L361 141 L357 128", ink, 3)
    s += pill(250, 32, 120, "Measure, improve", m)
    return svg(m, s, "Water flow meter on a pipe next to a falling consumption chart")


def membrane():
    m = "msf"; b, ink, _ = MOD[m]
    s = rect(40, 112, 230, 64, "#e2e8f0", 6)
    s += "".join(line(f"M{x} 116 V172", "#94a3b8", 2) for x in range(56, 268, 16))
    blobs = ((70, 106, 7), (88, 104, 9), (108, 107, 6), (150, 104, 8), (168, 106, 6), (205, 103, 10), (226, 107, 7), (246, 104, 8))
    s += "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#b45309" opacity="0.75" stroke="{O}" stroke-width="1.6"/>' for x, y, r in blobs)
    s += f'<circle cx="300" cy="96" r="50" fill="#ffffff" fill-opacity="0.75" stroke="{O}" stroke-width="4"/>'
    s += line("M336 132 L372 170", O, 10) + line("M336 132 L372 170", ink, 6)
    s += f'<circle cx="290" cy="90" r="13" fill="#b45309" opacity="0.8" stroke="{O}" stroke-width="1.8"/>'
    s += f'<circle cx="312" cy="104" r="9" fill="#b45309" opacity="0.8" stroke="{O}" stroke-width="1.8"/>'
    s += pill(40, 40, 104, "Root cause", m)
    return svg(m, s, "Magnifying glass over fouling on a membrane surface")


def scale_up():
    m = "pic"; b, ink, _ = MOD[m]
    s = shape("M66 120 H86 V140 L102 176 Q104 184 96 184 H56 Q48 184 50 176 L66 140 Z", "#ffffff")
    s += shape("M56 168 H96 L100 176 Q102 182 96 182 H56 Q50 182 52 176 Z", b, 0)
    s += rect(150, 98, 64, 86, "#ffffff", 10) + rect(166, 84, 32, 16, "#cbd5e1", 4)
    s += rect(152, 140, 60, 42, b, 8, 0)
    s += rect(262, 58, 104, 126, "#ffffff", 16) + rect(264, 116, 100, 66, b, 14, 0)
    s += line("M276 70 V102 M288 70 V96", "#e2e8f0", 4)
    s += line("M114 152 H138 M132 146 L139 152 L132 158", ink, 2.6) + line("M224 142 H250 M244 136 L251 142 L244 148", ink, 2.6)
    s += check(360, 60, 15)
    s += text(76, 208, "Lab", 12, ink) + text(182, 208, "Pilot", 12, ink) + text(314, 208, "Plant", 12, ink)
    return svg(m, s, "Flask, pilot vessel and plant tank showing a validated scale-up")


def gases_support():
    m = "msf"; b, ink, _ = MOD[m]
    s = ""
    for x, c in ((46, "#cbd5e1"), (96, "#94a3b8"), (146, "#cbd5e1")):
        s += rect(x, 72, 40, 130, c, 18) + rect(x + 12, 58, 16, 16, "#475569", 4)
        s += rect(x, 112, 40, 14, "#ffffff", 0, 1.8)
    s += shape("M226 44 H362 Q372 44 372 54 V106 Q372 116 362 116 H262 L244 132 L248 116 H226 Q216 116 216 106 V54 Q216 44 226 44 Z", "#ffffff")
    s += "".join(f'<circle cx="{x}" cy="80" r="5" fill="{ink}"/>' for x in (270, 294, 318))
    s += shape("M250 140 H352 Q362 140 362 150 V186 Q362 196 352 196 H340 L344 210 L326 196 H250 Q240 196 240 186 V150 Q240 140 250 140 Z", b)
    s += check(300, 168, 14)
    return svg(m, s, "Industrial gas cylinders next to support chat bubbles")


ART = {
    "incident_management": incident, "citi_migration": decommission, "payment_integration": integration,
    "mining_water": mining_water, "membrane_fouling": membrane, "vaccine_production": scale_up,
    "industrial_gases": gases_support,
}

if __name__ == "__main__":
    out = sys.argv[1]
    for name, fn in ART.items():
        with open(os.path.join(out, f"{name}.svg"), "w") as f:
            f.write(fn())
        print("wrote", name)
