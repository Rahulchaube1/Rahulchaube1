#!/usr/bin/env python3
"""Original SVG animation for a GitHub profile, generated with the standard library.

A blue car reveals a decorative 53 x 7 neon grid. It is not contribution data.
The SVG contains no scripts or external resources. Reduced-motion users receive
the complete, static board with the car parked at the right-hand side.
"""

from html import escape
from math import cos, sin, radians
from pathlib import Path
from random import Random

WIDTH, HEIGHT = 1080, 360
GRID_X, GRID_Y, PITCH, CELL = 64, 126, 18, 13
GRID_WIDTH, GRID_HEIGHT = 949, 121
CENTER_Y = 186
DURATION = 14
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "contribution-drive.svg"
PARTS: list[str] = []
RNG = Random(241119)


def add(markup):
    PARTS.append(markup)


def rect(x, y, width, height, fill, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    add(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" {extra}/>')


def text(x, y, value, size=12, fill="#9b91ad", **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" {extra}>{escape(value)}</text>')


def car_frames():
    """A horizontal drive, one controlled donut, then a clean exit.

    Full transform keyframes retain compatibility with SVG used as an image.
    The camera is stationary; the car drives through the grid rather than moving it.
    """
    frames = [(0, 89, CENTER_Y, 0), (3, 104, CENTER_Y, -3),
              (12, 224, CENTER_Y+2, 3), (23, 366, CENTER_Y-3, -4),
              (34, 494, CENTER_Y, 0), (37, 530, CENTER_Y-30, 0)]
    for index in range(1, 33):
        angle = -90 + index/32*360
        # A small oversteer angle communicates a drift instead of a rigid orbit.
        yaw = 14*sin(radians(index/32*180))
        frames.append((37+index/32*20, 530+30*cos(radians(angle)),
                       CENTER_Y+30*sin(radians(angle)), angle+90+yaw))
    frames.extend([(61, 571, CENTER_Y, 360), (72, 710, CENTER_Y+3, 356),
                   (85, 875, CENTER_Y-2, 363), (95, 1000, CENTER_Y, 360),
                   (100, 1032, CENTER_Y, 360)])
    return "@keyframes drive{"+"".join(
        f"{t:.3f}%{{transform:translate({x:.2f}px,{y:.2f}px) rotate({a:.2f}deg)}}"
        for t, x, y, a in frames)+"}"


def grid():
    # Dim squares are always present. Their brightness never encodes user data.
    add('<g fill="#241a30" stroke="#34243e" stroke-width=".6">')
    for col in range(53):
        for row in range(7):
            add(f'<use href="#cell" x="{GRID_X+col*PITCH}" y="{GRID_Y+row*PITCH}"/>')
    add('</g>')
    # Purple -> magenta -> coral/honey; irregular intensity makes a rich mosaic.
    palette = ['#7036c2', '#8b3fda', '#a74be8', '#c351e4', '#dc5dcc',
               '#f272b3', '#fc8d9d', '#ffa883', '#ffbf75', '#ffcf7c']
    add('<g class="lit-grid" clip-path="url(#reveal)">')
    for col in range(53):
        for row in range(7):
            density = RNG.random()
            if density < .17:
                color, opacity = '#4b285e', '.68'
            else:
                # Most cells stay violet; warm pixels punctuate high-intensity spots.
                index = int(RNG.triangular(0, len(palette)-.01, 2.1))
                color, opacity = palette[index], f'{RNG.uniform(.74, 1):.2f}'
            x, y = GRID_X+col*PITCH, GRID_Y+row*PITCH
            add(f'<use href="#cell" x="{x}" y="{y}" fill="{color}" opacity="{opacity}"/>')
            if density > .78:
                add(f'<path d="M{x+3} {y+2.5}H{x+10}" stroke="#fff3ff" stroke-opacity=".13"/>')
    add('</g>')


def main():
    PARTS.clear()
    RNG.seed(241119)
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="drive-title drive-desc">')
    add('<title id="drive-title">Commit to the drive — Rahul Chaube</title>')
    add('<desc id="drive-desc">A detailed blue sports car reveals a neon violet, pink and warm orange grid from left to right, with soft tire smoke and a playful drift. This is an original decorative animation, not a visualization of contribution statistics. With reduced motion, the fully colored board and parked car remain still.</desc>')
    add('''<defs>
<rect id="cell" width="13" height="13" rx="2"/>
<clipPath id="canvas"><rect x="1" y="1" width="1078" height="358" rx="15"/></clipPath>
<clipPath id="reveal"><rect class="reveal-mask" x="64" y="119" width="949" height="135"/></clipPath>
<linearGradient id="body-paint" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#a5d5ff"/><stop offset=".23" stop-color="#75b6ff"/><stop offset=".6" stop-color="#4479e8"/><stop offset="1" stop-color="#243e87"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#132442"/><stop offset=".55" stop-color="#203d60"/><stop offset="1" stop-color="#71a3c4"/></linearGradient>
<linearGradient id="beam"><stop stop-color="#c4dfff" stop-opacity=".12"/><stop offset="1" stop-color="#c4dfff" stop-opacity="0"/></linearGradient>
<radialGradient id="board-halo"><stop stop-color="#8746b0" stop-opacity=".09"/><stop offset="1" stop-color="#8746b0" stop-opacity="0"/></radialGradient>
<filter id="soft-smoke" x="-45%" y="-100%" width="200%" height="300%"><feGaussianBlur stdDeviation="3.5"/></filter>
</defs>''')
    add('''<style>
.car{transform:translate(1000px,186px);transform-origin:0 0;transform-box:view-box}
.reveal-mask{transform-origin:64px 0;transform-box:view-box}
.smoke{opacity:0}.skid{opacity:.5}.donut{opacity:.4}
@media(prefers-reduced-motion:no-preference){
 .car{animation:drive 14s linear infinite,car-fade 14s linear infinite}
 .reveal-mask{animation:reveal 14s linear infinite}
 .lit-grid{animation:board-fade 14s linear infinite}
 .skid{animation:board-fade 14s linear infinite}
 .donut{animation:donut-ink 14s linear infinite}
 .smoke{opacity:1;animation:smoke-breathe 1.4s ease-in-out infinite alternate}
}
@keyframes reveal{0%{transform:scaleX(.026)}3%{transform:scaleX(.042)}12%{transform:scaleX(.169)}23%{transform:scaleX(.319)}34%{transform:scaleX(.453)}37%,57%{transform:scaleX(.524)}61%{transform:scaleX(.535)}72%{transform:scaleX(.681)}85%{transform:scaleX(.855)}95%,100%{transform:scaleX(1)}}
@keyframes car-fade{0%{opacity:0}3%,94%{opacity:1}100%{opacity:0}}
@keyframes board-fade{0%{opacity:0}3%,94%{opacity:1}100%{opacity:0}}
@keyframes donut-ink{0%,37%{stroke-dashoffset:240;opacity:0}39%{opacity:.42}57%,94%{stroke-dashoffset:0;opacity:.42}100%{stroke-dashoffset:0;opacity:0}}
@keyframes smoke-breathe{from{opacity:.7;transform:translate(2px,-1px) scale(.94)}to{opacity:1;transform:translate(-5px,1px) scale(1.04)}}
'''+car_frames()+'</style>')
    rect(.5, .5, 1079, 359, '#100d19', rx='15', stroke='#302439')
    add('<g clip-path="url(#canvas)">')
    add('<ellipse cx="520" cy="185" rx="520" ry="150" fill="url(#board-halo)"/>')
    add('<g font-family="ui-monospace,SFMono-Regular,Consolas,Liberation Mono,monospace">')
    text(34, 43, 'COMMIT TO THE DRIVE', 21, '#eee7f4', font_weight='700', letter_spacing='-.7')
    text(1046, 41, '@Rahulchaube1', 12, '#a89ab7', text_anchor='end')
    add('</g>')
    grid()
    # Two understated rubber tracks and a ring are clipped behind the reveal.
    add('<g clip-path="url(#reveal)" fill="none" stroke="#07050c" stroke-linecap="round">')
    add('<g class="skid" stroke-width="4"><path d="M90 179C230 176 355 184 478 178S517 147 530 149M565 179C690 186 840 173 1000 179"/><path d="M90 197C230 194 355 202 478 196S517 165 530 167M565 197C690 204 840 191 1000 197"/></g>')
    add('<g class="donut" stroke-width="5" stroke-dasharray="240" stroke-dashoffset="0"><circle cx="530" cy="186" r="37" transform="rotate(-90 530 186)"/><circle cx="530" cy="186" r="22" transform="rotate(-90 530 186)"/></g>')
    add('</g>')
    add('<g class="car" transform="translate(1000 186)">')
    add('<g transform="scale(1.35)">')
    # Tire smoke follows the rear axle; static users receive a clean parked car.
    add('<g class="smoke" filter="url(#soft-smoke)" fill="#b8b1c5">')
    add('<ellipse cx="-35" cy="-10" rx="14" ry="6" opacity=".24"/><ellipse cx="-35" cy="10" rx="13" ry="6" opacity=".22"/><ellipse cx="-58" cy="-9" rx="22" ry="10" opacity=".13"/><ellipse cx="-62" cy="8" rx="22" ry="10" opacity=".11"/><ellipse cx="-86" cy="1" rx="29" ry="13" opacity=".06"/>')
    add('</g>')
    add('<path d="M29-10 81-25V-5L29-5ZM29 5 81 5V25L29 10Z" fill="url(#beam)"/>')
    rect(-33, -10, 66, 28, '#03020a', rx='10', opacity='.5')
    # Exposed wheels, sidewalls and brake highlights.
    for x in [-24, 16]:
        rect(x, -16, 10, 5, '#050711', rx='1.5')
        rect(x, 11, 10, 5, '#050711', rx='1.5')
        rect(x+2, -15.5, 6, 1, '#7585a6', opacity='.6')
        rect(x+2, 14.5, 6, 1, '#7585a6', opacity='.55')
    add('<path d="M-26-13H17L27-9 32-4V4L27 9 17 13H-26L-31 8V-8Z" fill="url(#body-paint)" stroke="#88b3ff" stroke-width=".9"/>')
    # Roof, windshield, rear glass and hood relief.
    add('<path d="M6-10 15-8 18-5V5L15 8 6 10Z" fill="url(#glass)" stroke="#a4c6e8" stroke-width=".7"/>')
    add('<path d="M8-8 13-7 15-4V4L13 7 12 7 12-3Z" fill="#b8dfff" opacity=".26"/>')
    add('<path d="M-20-9-13-11V11L-20 9-22 5V-5Z" fill="#182b4c" stroke="#7fa4cc" stroke-width=".7"/>')
    rect(-12, -10.5, 17, 21, '#6c9fe9', rx='2', stroke='#aacbff', stroke_width='.7')
    rect(-10, -8.5, 13, 1.5, '#bddbff', rx='.5', opacity='.65')
    rect(-10, 7, 13, 1.2, '#244b93', opacity='.65')
    add('<path d="M19-7H25M19 7H25M22-4H28M22 4H28" stroke="#abcfff" stroke-width=".8" opacity=".55"/>')
    add('<path d="M-25-11H-15M-25 11H-15" stroke="#c6e0ff" stroke-width="1.3" opacity=".75"/>')
    # Rear spoiler and tail lamps.
    rect(-29, -13, 3.5, 26, '#223862', rx='.6', stroke='#9abbef', stroke_width='.6')
    rect(-31, -9, 2.2, 5, '#ff776c', rx='.6')
    rect(-31, 4, 2.2, 5, '#ff776c', rx='.6')
    # Front lamps, grille and small wing mirrors.
    add('<path d="M27-9 30-6V-3H27ZM27 3H30V6L27 9Z" fill="#e7f3ff"/>')
    rect(30, -2, 2, 4, '#17243b', rx='.4')
    rect(8, -15, 5, 2.2, '#8ac5ff', rx='.7')
    rect(8, 12.8, 5, 2.2, '#5d92e2', rx='.7')
    add('</g></g>')
    add('<g font-family="ui-monospace,SFMono-Regular,Consolas,Liberation Mono,monospace">')
    text(34, 327, 'A LITTLE DETOUR BETWEEN COMMITS.', 9, '#71627e', letter_spacing='1.5')
    add('</g></g></svg>')
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text('\n'.join(PARTS)+'\n', encoding='utf-8')
    print(f'{OUTPUT}: {OUTPUT.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
