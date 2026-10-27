# Laver et mere fotorealistisk mockup af fotovæggen: et rigtigt festlokale sløret i baggrunden,
# Baggrunden er et foto fra Wikimedia Commons: "DZ6 0468 Spacious elegantly lit banquet hall" af PattayaPatrol, CC BY-SA 4.0.
# Mockuppen bygger på det foto, så den deles under samme licens med kredit.
# stof med folder og glans, stativ, rød løber og guldstolper, blitzlys, korn og linsefejl.
# Kør med FaceFusion-miljøets Python, der har opencv og numpy:
#   ~/facefusion-lokal/app/.venv/bin/python tools/mockup.py <baggrundsfoto> <ud.png>
import sys, os
import numpy as np, cv2

HER = os.path.dirname(os.path.abspath(__file__))
BAG, UD = sys.argv[1], sys.argv[2]
W, H = 2400, 1600
rng = np.random.default_rng(7)

def glat_stoej(h, w, skala, seed):
    # blød støj: tilfældige værdier i et groft net, skaleret op og sløret
    r = np.random.default_rng(seed).standard_normal((max(2, h // skala), max(2, w // skala))).astype(np.float32)
    r = cv2.resize(r, (w, h), interpolation=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(r, (0, 0), skala / 2)

def lerp(a, b, t):
    return a * (1 - t) + b * t

# ---------- baggrund: et rigtigt festlokale, sløret som ved stor blænde og gjort aftenmørkt ----------
bag = cv2.imread(BAG).astype(np.float32) / 255
bag = cv2.resize(bag, (W, int(W * bag.shape[0] / bag.shape[1])))
bag = bag[bag.shape[0] - H - 40: bag.shape[0] - 40] if bag.shape[0] > H + 40 else cv2.resize(bag, (W, H))
bag = cv2.GaussianBlur(bag, (0, 0), 22)
lys = np.clip((bag - .72) * 4, 0, 1)                       # lyse punkter bliver til bokeh
bag = bag * .32 + cv2.GaussianBlur(lys, (0, 0), 14) * .55
gra = bag.mean(2, keepdims=True); bag = lerp(gra, bag, .45)       # mindre farve, så den blå skærm ikke stjæler blikket
bag[..., 2] *= 1.08; bag[..., 0] *= .88                     # varmere
img = bag.copy()

# gulvet: mørkt trægulv i perspektiv
GULV = 1180
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
t = np.clip((yy - GULV) / (H - GULV), 0, 1)
gulv = np.dstack([lerp(.07, .13, t) * .8, lerp(.07, .12, t) * .85, lerp(.08, .14, t)])
planker = (np.sin((xx - W / 2) / (1 + t * 3.5) * .09) * .5 + .5) * .03
gulv = gulv + planker[..., None] + glat_stoej(H, W, 8, 3)[..., None] * .012
img = np.where((yy >= GULV)[..., None], gulv, img)
# blød overgang mellem væg og gulv
img = lerp(img, cv2.GaussianBlur(img, (0, 0), 6), np.clip(1 - abs(yy - GULV) / 14, 0, 1)[..., None])

# ---------- banneret med stoffolder ----------
design = cv2.imread(os.path.join(HER, '..', 'print', 'fotovaeg-preview.png')).astype(np.float32) / 255
S = 1200
design = cv2.resize(design, (S, S), interpolation=cv2.INTER_AREA)
by, bx = np.mgrid[0:S, 0:S].astype(np.float32)
# folder fra ophænget i toppen, der fader ud nedad, plus store bløde buler
fold = (np.sin(bx / S * np.pi * 9 + glat_stoej(S, S, 60, 11) * 2) * np.exp(-by / (S * .18)) * 1.0
        + glat_stoej(S, S, 140, 12) * 2.2 + glat_stoej(S, S, 45, 13) * .5)
fold = cv2.GaussianBlur(fold, (0, 0), 6)
dx = cv2.Sobel(fold, cv2.CV_32F, 1, 0, ksize=5) / 40
dy = cv2.Sobel(fold, cv2.CV_32F, 0, 1, ksize=5) / 40
skygge = 1 + (dx * -.7 + dy * -.5) * 1.3                    # lys fra venstre og lidt oppefra
glans = np.clip(dx * -.7 + dy * -.5, 0, None) ** 1.5 * .5     # satinglans på kammene
bane = remap = cv2.remap(design, bx + dx * 7, by + dy * 7, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
bane = bane * skygge[..., None] + glans[..., None] * np.array([.55, .6, .65], np.float32)
# kanterne trækker lidt mørkere, og lommen øverst
bane *= (1 - .35 * np.exp(-bx / 25) - .35 * np.exp(-(S - bx) / 25))[..., None]
bane[:26] *= .55

# placer banneret drejet en anelse i rummet
x0, y0, x1 = 720, 210, 1680
hojre_kort = 26
src = np.float32([[0, 0], [S, 0], [S, S], [0, S]])
dst = np.float32([[x0, y0], [x1, y0 + hojre_kort], [x1, GULV - 30 - hojre_kort * .3], [x0, GULV - 30]])
M = cv2.getPerspectiveTransform(src, dst)
bane_w = cv2.warpPerspective(bane, M, (W, H), flags=cv2.INTER_LINEAR)
maske = cv2.warpPerspective(np.ones((S, S), np.float32), M, (W, H))
# skygge bag banneret på væggen
sk = cv2.GaussianBlur(cv2.warpPerspective(np.ones((S, S), np.float32), cv2.getPerspectiveTransform(src, dst + np.float32([40, 30])), (W, H)), (0, 0), 40)
img *= (1 - sk * .55)[..., None]

# ---------- stativet ----------
def stang(img, xa, ya, xb, yb, bredde, farve_lys=.55, farve_mork=.05):
    lag = np.zeros((H, W), np.float32)
    cv2.line(lag, (int(xa), int(ya)), (int(xb), int(yb)), 1, int(bredde), cv2.LINE_AA)
    # metal: lys stribe midt på, mørk i kanterne
    midt = np.zeros((H, W), np.float32)
    cv2.line(midt, (int(xa - bredde * .15), int(ya)), (int(xb - bredde * .15), int(yb)), 1, max(1, int(bredde * .3)), cv2.LINE_AA)
    farve = farve_mork + cv2.GaussianBlur(midt, (0, 0), 1.2) * (farve_lys - farve_mork)
    return lerp(img, np.dstack([farve] * 3), lag[..., None])

ben_y = GULV + 40
for (xp, top) in [(x0 - 18, y0 - 18), (x1 + 18, y0 + hojre_kort - 18)]:
    # fødderne: tre ben spredt ud på gulvet, med kontaktskygge
    for dxp, dyp in [(-150, 34), (150, 34), (0, 70)]:
        sh = np.zeros((H, W), np.float32)
        cv2.line(sh, (xp, ben_y), (xp + dxp, ben_y + dyp + 8), 1, 18, cv2.LINE_AA)
        img *= (1 - cv2.GaussianBlur(sh, (0, 0), 10) * .6)[..., None]
        img = stang(img, xp, ben_y - 30, xp + dxp, ben_y + dyp, 9, .35)
    img = stang(img, xp, top, xp, ben_y - 20, 15)
    img = stang(img, xp, int(lerp(top, ben_y, .45)), xp, int(lerp(top, ben_y, .45)) + 26, 21, .4)  # samlemuffe

# banneret oven på stængerne, og tværstangen øverst
img = lerp(img, bane_w, maske[..., None])
img = stang(img, x0 - 34, y0 - 12, x1 + 34, y0 + hojre_kort - 12, 14, .6)

# ---------- rød løber i perspektiv ----------
lob = np.zeros((H, W), np.float32)
pts = np.int32([[880, GULV + 6], [1540, GULV + 14], [2030, H], [390, H]])
cv2.fillPoly(lob, [pts], 1, cv2.LINE_AA)
lob = cv2.GaussianBlur(lob, (0, 0), 1.2)
t2 = np.clip((yy - GULV) / (H - GULV), 0, 1)
tekst = glat_stoej(H, W, 2, 21) * .05 + glat_stoej(H, W, 30, 22) * .04
rod = np.dstack([.06 + t2 * .04, .03 + t2 * .02, .32 + t2 * .22]) * (1 + tekst)[..., None]
img = lerp(img, rod, lob[..., None])

# ---------- guldstolper med røde reb ----------
def stolpe(img, cx, fod_y, hoejde, s=1.0):
    r = int(42 * s); bw = int(13 * s)
    sh = np.zeros((H, W), np.float32)
    cv2.ellipse(sh, (cx + int(18 * s), fod_y + int(6 * s)), (int(r * 1.5), int(r * .35)), 0, 0, 360, 1, -1, cv2.LINE_AA)
    img *= (1 - cv2.GaussianBlur(sh, (0, 0), 12 * s) * .75)[..., None]
    lag = np.zeros((H, W), np.float32)
    cv2.ellipse(lag, (cx, fod_y), (r, int(r * .3)), 0, 0, 360, 1, -1, cv2.LINE_AA)
    cv2.rectangle(lag, (cx - bw // 2, fod_y - hoejde), (cx + bw // 2, fod_y), 1, -1, cv2.LINE_AA)
    cv2.circle(lag, (cx, fod_y - hoejde - int(10 * s)), int(14 * s), 1, -1, cv2.LINE_AA)
    lag = cv2.GaussianBlur(lag, (0, 0), .8)
    # guld med lodret glans
    u = np.clip((xx - (cx - r)) / (2 * r), 0, 1)
    g = .25 + .75 * np.exp(-((u - .38) / .12) ** 2) + .15 * np.exp(-((u - .8) / .05) ** 2)
    guld = np.dstack([.18 * g, .5 * g, .78 * g])
    return lerp(img, np.clip(guld, 0, 1), lag[..., None])

def reb(img, a, b, synk, tyk):
    t = np.linspace(0, 1, 120)
    px = lerp(a[0], b[0], t); py = lerp(a[1], b[1], t) + np.sin(t * np.pi) * synk
    p = np.int32(np.c_[px, py])
    sh = np.zeros((H, W), np.float32); cv2.polylines(sh, [p + [10, 60]], False, 1, tyk, cv2.LINE_AA)
    img *= (1 - cv2.GaussianBlur(sh, (0, 0), 14) * .35)[..., None]
    for d, f in [(0, (.04, .03, .32)), (-tyk * .2, (.12, .1, .62)), (-tyk * .3, (.3, .3, .85))]:
        lag = np.zeros((H, W), np.float32)
        cv2.polylines(lag, [np.int32(p + [0, d])], False, 1, max(2, int(tyk * (1 if d == 0 else .35 if f[2] < .8 else .15))), cv2.LINE_AA)
        img = lerp(img, np.dstack([np.full((H, W), c, np.float32) for c in f]), cv2.GaussianBlur(lag, (0, 0), .9)[..., None])
    return img

poster = [(250, 1510, 330, 1.25), (800, 1270, 250, .95), (1640, 1280, 250, .95), (2170, 1520, 330, 1.25)]
img = reb(img, (poster[0][0], poster[0][1] - poster[0][2] - 10), (poster[1][0], poster[1][1] - poster[1][2] - 8), 90, 20)
img = reb(img, (poster[2][0], poster[2][1] - poster[2][2] - 8), (poster[3][0], poster[3][1] - poster[3][2] - 10), 90, 20)
for cx, fy, h, s in sorted(poster, key=lambda p: p[1]):
    img = stolpe(img, cx, fy, h, s)

# ---------- fotolys: blitz, vignet, linsefejl og korn ----------
blitz = np.exp(-(((xx - 1180) / 1300) ** 2 + ((yy - 720) / 900) ** 2))
img = img * (.55 + .75 * blitz)[..., None]
vig = 1 - .55 * (((xx - W / 2) / (W * .62)) ** 2 + ((yy - H / 2) / (H * .62)) ** 2)
img *= np.clip(vig, 0, 1)[..., None]
# en anelse kromatisk forskydning ud mod kanterne
k = ((xx - W / 2) / W) * 2.2
img[..., 2] = cv2.remap(img[..., 2], xx + k, yy, cv2.INTER_LINEAR)
img[..., 0] = cv2.remap(img[..., 0], xx - k, yy, cv2.INTER_LINEAR)
# blødere forgrund, som ved lav dybdeskarphed
bl = cv2.GaussianBlur(img, (0, 0), 3.5)
img = lerp(img, bl, np.clip((yy - 1400) / 200, 0, 1)[..., None])
# filmagtigt korn og en let tone
korn = rng.standard_normal((H, W)).astype(np.float32)
korn = cv2.GaussianBlur(korn, (0, 0), .7) * .035
img = img + korn[..., None] * (.6 + img)
img = np.clip(img, 0, 1) ** .95
img = np.clip(img * 1.08 - .01, 0, 1)
cv2.imwrite(UD, (img * 255).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 6])
print('ok', UD)
