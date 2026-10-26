// Guldbilletterne. Koderne står ikke her, kun et fingeraftryk af dem, så ingen kan finde dem i kildekoden.
const PRIZES = {
  '01057777bb7f63c71e9eb518998c347602cecfc088677898de5096fd8c7ad159': ['En flaske champagne', 'Tag billetten med, så venter flasken på dig i baren.'],
  'c10bc9f7439f4b17e574fcc7631f17848272aa978828c7281456bdd68bf1b731': ['Gin og tonic', 'En flaske gin, tonic og agurk. Tag billetten med, så får du det hele.'],
  'd5a2988e047cf88c4431f3eba9626eac08d2db72f5f899fc534f7418017ce083': ['Rom og ginger beer', 'En flaske rom, ginger beer og lime. Tag billetten med, så får du det hele.'],
};

// Guldbillet
const codeForm = document.getElementById('kode-form');
const codeOut = document.getElementById('kode-svar');
codeForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  let code = codeForm.kode.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
  if (!code.startsWith('GULD')) code = 'GULD' + code;
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('st27:' + code));
  const hash = [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
  const prize = PRIZES[hash];
  codeOut.classList.toggle('ja', !!prize);
  codeOut.innerHTML = prize
    ? `<strong>Du har vundet. ${prize[0]}.</strong><p>${prize[1]}</p>`
    : '<p>Den kode kender vi ikke. Tjek bogstaverne på billetten, og prøv igen.</p>';
});

// Store ord fylder hele bredden på én linje
const fit = (el, box) => {
  el.style.fontSize = '';
  const w = box.clientWidth, s = el.scrollWidth;
  if (s > 0) el.style.fontSize = (parseFloat(getComputedStyle(el).fontSize) * w / s) * 0.995 + 'px';
};
const wm = document.querySelector('.wordmark');
const fitAll = () => {
  const foot = wm.parentElement, cs = getComputedStyle(foot);
  const inner = { clientWidth: foot.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) };
  fit(wm, inner);
};
document.fonts.ready.then(fitAll);
addEventListener('resize', fitAll);

// Stille billeder for dem, der har bedt om mindre bevægelse
if (matchMedia('(prefers-reduced-motion: reduce)').matches) document.querySelectorAll('video').forEach((v) => { v.removeAttribute('autoplay'); v.pause(); });

// Indgange: overskrift, så tekst, så billede
const groups = [
  ['.intro-text > *', '.intro-photo', '.intro-note'],
  ['.side-l', '.giant', '.bars > details', '.side-r'],
  ['.guld-photo', '.guld-body > *'],
  ['.rsvp-top > *', '.bigword'],
  ['.faq h2', '.faq-photo', '.qs details'],
  ['.foot-cols > div'],
];
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  groups.forEach((sels) => {
    let i = 0;
    sels.forEach((sel) => document.querySelectorAll(sel).forEach((el) => {
      el.classList.add('rv'); el.style.setProperty('--d', Math.min(i++ * 75, 600) + 'ms'); io.observe(el);
    }));
  });
}
