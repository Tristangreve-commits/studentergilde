# Laver teksturerne til det slidte skattekort-look: ridser, støv, folder, pletter og slidte kanter.
# Kør: python3 tools/slid.py   (skriver img/slid-lys-*.svg og img/slid-mork-*.svg)
import random, math, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
W, H = 1000, 1000

def scratches(rnd, n):
    out = []
    for _ in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        length = rnd.uniform(40, 420)
        ang = rnd.gauss(math.radians(rnd.choice([90, 90, 90, 20, 160])), .25)
        pts = []
        for k in range(5):
            t = k / 4
            pts.append((x + math.cos(ang) * length * t + rnd.gauss(0, 3), y + math.sin(ang) * length * t + rnd.gauss(0, 3)))
        d = 'M%.1f %.1f ' % pts[0] + ' '.join('L%.1f %.1f' % p for p in pts[1:])
        out.append('<path d="%s" stroke="#fff" stroke-opacity="%.2f" stroke-width="%.2f" fill="none" stroke-linecap="round"/>'
                   % (d, rnd.uniform(.08, .32), rnd.uniform(.4, 1.4)))
    return out

def specks(rnd, n, color, lo, hi):
    return ['<circle cx="%.1f" cy="%.1f" r="%.2f" fill="%s" fill-opacity="%.2f"/>'
            % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(.4, 2.2), color, rnd.uniform(lo, hi)) for _ in range(n)]

def fold(x1, y1, x2, y2, light):
    # en fold er en lys kant og en mørk skygge lige ved siden af
    if light:
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#fff" stroke-opacity=".16" stroke-width="2.2"/>' % (x1, y1, x2, y2)
    dx, dy = (3, 0) if x1 == x2 else (0, 3)
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#000" stroke-opacity=".4" stroke-width="4"/>' % (x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            + '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#000" stroke-opacity=".25" stroke-width="16"/>' % (x1 + dx * 3, y1 + dy * 3, x2 + dx * 3, y2 + dy * 3))

def svg(body, defs=''):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="none">%s%s</svg>'
            % (W, H, '<defs>%s</defs>' % defs if defs else '', ''.join(body)))

for name, seed, folds in [('a', 7, [(500, 0, 500, 1000), (0, 500, 1000, 500)]),
                          ('b', 21, [(330, 0, 330, 1000), (0, 640, 1000, 640)])]:
    rnd = random.Random(seed)
    lys = scratches(rnd, 70) + specks(rnd, 260, '#fff', .15, .6) + [fold(*f, True) for f in folds]
    # slidte kanter langs folderne: lyse, flossede pletter
    for (x1, y1, x2, y2) in folds:
        for _ in range(40):
            t = rnd.random()
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            lys.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#fff" fill-opacity="%.2f"/>'
                       % (x + rnd.gauss(0, 3), y + rnd.gauss(0, 3), rnd.uniform(1, 6), rnd.uniform(1, 6), rnd.uniform(.03, .12)))
    open(os.path.join(OUT, 'slid-lys-%s.svg' % name), 'w').write(svg(lys))

    defs = ('<filter id="plet" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".006" numOctaves="4" seed="%d"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 .22  0 0 0 0 .12  0 0 0 0 .03  0 0 0 -2.4 1.25"/></filter>'
            '<radialGradient id="kant" cx="50%%" cy="50%%" r="78%%"><stop offset=".6" stop-color="#000" stop-opacity="0"/>'
            '<stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>' % seed)
    mork = ['<rect width="%d" height="%d" filter="url(#plet)" opacity=".6"/>' % (W, H)]
    # kaffe- og vandpletter: ringe med mørk kant
    for _ in range(3):
        cx, cy, r = rnd.uniform(80, 920), rnd.uniform(80, 920), rnd.uniform(40, 110)
        mork.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#3a2410" fill-opacity=".18" stroke="#2a1608" stroke-opacity=".35" stroke-width="%.1f"/>'
                    % (cx, cy, r, rnd.uniform(1.5, 4)))
    mork += [fold(*f, False) for f in folds]
    mork += specks(rnd, 160, '#000', .3, .8)
    mork.append('<rect width="%d" height="%d" fill="url(#kant)"/>' % (W, H))
    open(os.path.join(OUT, 'slid-mork-%s.svg' % name), 'w').write(svg(mork, defs))
print('ok')
