# Laver teksturen til det slidte fotokopi-look: svag gennemslagstekst, tynde folder og en plet tonerprikker.
# Kør: python3 tools/kopi.py   (skriver img/kopi-a.svg og img/kopi-b.svg)
import random, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
W, H = 1600, 1000

def tekstblok(rnd, w, h):
    # rækker af små streger, der ligner tekst set gennem papiret
    out, y = [], 6
    while y < h - 4:
        x = rnd.uniform(0, 8)
        end = w - rnd.uniform(0, 30) if rnd.random() > .15 else rnd.uniform(w * .3, w * .8)
        while x < end:
            ww = rnd.uniform(4, 22)
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>' % (x, y, min(ww, end - x), rnd.uniform(2.2, 3.4)))
            x += ww + rnd.uniform(2.5, 5)
        y += rnd.uniform(9.5, 11)
    return ''.join(out)

for name, seed, folds, toner in [('a', 3, [('v', 1060), ('h', 640)], (1340, 380)),
                                 ('b', 17, [('v', 540), ('h', 300)], (260, 760))]:
    rnd = random.Random(seed)
    defs = []
    blok = tekstblok(rnd, 220, 300)
    defs.append('<filter id="slor"><feGaussianBlur stdDeviation=".7"/></filter>')
    # tekstspalterne toner ind og ud i store, bløde felter
    defs.append('<filter id="felt" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".0016" numOctaves="5" seed="%d"/>'
                '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  4 0 0 0 -1.9"/></filter>' % seed)
    defs.append('<mask id="m"><rect width="%d" height="%d" filter="url(#felt)"/></mask>' % (W, H))
    # tonerprikker: fin støj, der kun er tydelig i én plet
    defs.append('<filter id="toner" x="0" y="0" width="100%%" height="100%%"><feTurbulence type="fractalNoise" baseFrequency=".55" numOctaves="2" seed="%d"/>'
                '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  14 0 0 0 -9.2"/></filter>' % seed)
    defs.append('<radialGradient id="plet"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    defs.append('<mask id="tm"><ellipse cx="%d" cy="%d" rx="300" ry="260" fill="url(#plet)"/></mask>' % toner)
    body = []
    # spalter med mellemrum, som i en avis
    for i, x in enumerate(range(140, W - 200, 250)):
        if rnd.random() < .75:
            y0 = rnd.uniform(-40, 120)
            defs.append('<pattern id="t%d" x="%d" y="%.0f" width="230" height="300" patternUnits="userSpaceOnUse"><g fill="#fff">%s</g></pattern>' % (i, x, y0, blok))
            body.append('<g mask="url(#m)"><rect x="%d" y="%.0f" width="220" height="%.0f" fill="url(#t%d)" filter="url(#slor)" opacity="%.2f"/></g>'
                        % (x, y0, rnd.uniform(500, 900), i, rnd.uniform(.35, .7)))
    body.append('<rect width="%d" height="%d" filter="url(#toner)" mask="url(#tm)" opacity=".9"/>' % (W, H))
    for k, p in folds:
        if k == 'v':
            body.append('<path d="M%d 0 L%d %d" stroke="#fff" stroke-opacity=".5" stroke-width="1.6" fill="none"/>' % (p, p + 6, H))
        else:
            body.append('<path d="M0 %d L%d %d" stroke="#fff" stroke-opacity=".4" stroke-width="1.4" fill="none"/>' % (p, W, p - 5))
    for _ in range(40):
        body.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff" fill-opacity="%.2f"/>' % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(.8, 2.4), rnd.uniform(.3, .8)))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice"><defs>%s</defs>%s</svg>'
           % (W, H, ''.join(defs), ''.join(body)))
    open(os.path.join(OUT, 'kopi-%s.svg' % name), 'w').write(svg)
print('ok')
