// Alle drinks står her ét sted. Drinkssiden, plakaten og det lille kort henter dem herfra,
// så en ændring her slår igennem overalt. Kør PDF'erne igen bagefter.
window.BAREN = {
  signatur: [
    { navn: 'Sam', glas: 'highball', ind: 'Mørk rom, ginger beer og lime på masser af is', om: 'Krydret, stærk og lidt farlig.' },
    { navn: 'Tristan', glas: 'ballon', ind: 'Gin, tonic, agurk og en skive citron', om: 'Frisk, klar og går lige i blodet.' },
    { navn: 'Huen', glas: 'coupe', ind: 'Bobler, hyldeblomst og citron', om: 'Til skålen, når huen kommer på.' }
  ],
  grupper: [
    { navn: 'Drinks', glas: 'tumbler', liste: [
      ['Vodka og Red Bull', 'Til dansegulvet'],
      ['Vodka og lemon', 'Klassikeren'],
      ['Rom og cola', 'Med lime'],
      ['Gin og hyldeblomst', 'Med danskvand']
    ] },
    { navn: 'Bobler og øl', glas: 'flute', liste: [
      ['Bobler', 'Til skålen'],
      ['Kold øl', 'Hele natten'],
      ['Shots', 'Når DJ\'en siger til']
    ] },
    { navn: 'Uden alkohol', glas: 'highball', liste: [
      ['Lille Sam', 'Ginger beer, lime og mynte'],
      ['Hyldeblomst og danskvand', 'Med citron'],
      ['Sodavand', 'Cola, lemon og danskvand'],
      ['Vand', 'Drik et glas ind imellem']
    ] }
  ],
  // Glas tegnet med én streg, i samme guld som resten
  glas: {
    highball: '<path d="M14 6h20l-2 36H16z"/><path d="M15 16h18"/><path d="M28 2l-6 20"/>',
    ballon: '<path d="M10 6h28c0 16-6 22-14 22S10 22 10 6z"/><path d="M24 28v14M16 42h16"/><path d="M12 13h24"/>',
    coupe: '<path d="M6 10h36c-2 8-9 12-18 12S8 18 6 10z"/><path d="M24 22v20M16 42h16"/>',
    tumbler: '<path d="M10 14h28l-3 28H13z"/><path d="M16 22h8v8h-8z"/>',
    flute: '<path d="M18 4h12l-1 20c0 4-2 6-5 6s-5-2-5-6z"/><path d="M24 30v12M17 42h14"/><path d="M22 12v2M26 16v2M23 20v1"/>'
  }
};

// Tegner et glas som en lille SVG
window.BAREN.svg = (navn) =>
  '<svg class="glas" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round">' +
  window.BAREN.glas[navn] + '</svg>';
