# Sam & Tristans studentergilde

Invitationssiden, brevet og guldbilletterne.

- `index.html`, `style.css`, `app.js`: siden, som QR-koden peger på
- `print/brev.pdf`: invitationen, klar til print
- `print/guldbilletter.pdf`: de tre guldbilletter (ligger kun lokalt, se HEMMELIGT.md)
- `apps-script.gs`: koden, der skriver tilmeldinger ind i jeres Google Sheet

## Læg siden op på GitHub Pages

1. Lav et nyt offentligt repo på github.com med navnet `studentergilde`.
2. Skub mappen op (`git push`).
3. På GitHub: Settings, Pages, vælg branch `main` og mappen `/ (root)`, og gem.
4. Efter et minut ligger siden på https://tristangreve-commits.github.io/studentergilde/

Hedder repoet eller brugeren noget andet, så ret `URL_TIL_SIDEN` i `print/brev.html` og lav PDF'en igen, før I printer.

## Tilmeldinger i Google Sheet

1. Lav et nyt Google Sheet, fx "Studentergilde tilmeldinger".
2. Udvidelser, Apps Script. Slet det, der står, og indsæt indholdet af `apps-script.gs`. Gem.
3. Implementer, Ny implementering, type "Webapp". Udfør som: dig selv. Hvem har adgang: Alle. Implementer, og giv lov.
4. Kopiér webapp-adressen (den ender på `/exec`), og sæt den ind i `SHEET_URL` øverst i `app.js`.
5. Skub ændringen op. Nu lander hver tilmelding som en række i arket, og når nogen indløser en guldbillet, kommer der også en række.

## Ret dato, adresse og tekst

Dato, tid og adresse står direkte i `index.html` og `print/brev.html`. Søg efter "15. juli" og "Gyntelsbjerg" og ret alle steder.

## Print

- Brevet er A4, printet dobbeltsidet (vend på den lange kant) og foldet i tre, så det passer i en lang konvolut (C65/DL, 110 x 220 mm). De små streger i kanten viser, hvor der skal foldes.
- Fold den nederste tredjedel op først, og så den øverste ned over. Så vender forsiden med seglet udad.
- Skriv gæstens navn og medlemsnummer på forsiden og navnet efter "Kære" indeni.
- Brevet er mørkt hele vejen ud til kanten. En hjemmeprinter laver en hvid kant og bruger meget sort blæk, så et trykkeri giver det pæneste resultat. Tykt papir (200 til 250 g) føles mest eksklusivt.
- Guldbilletterne ser bedst ud på guld- eller cremefarvet karton.

Billederne er gamle, frie arkivbilleder fra Wikimedia Commons. Krediteringen står nederst på siden.
