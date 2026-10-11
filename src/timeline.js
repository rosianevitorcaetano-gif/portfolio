// Horizontal timelines: the arrow buttons scroll one card at a time, switch off at
// either end, and hide when everything already fits.
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

document.querySelectorAll('[data-htl-arrows]').forEach((arrows) => {
  const list = document.getElementById(arrows.dataset.htlArrows);
  if (!list) return;
  const [back, forward] = arrows.querySelectorAll('button');

  const step = () => {
    const card = list.querySelector('.htl-item');
    const gap = parseFloat(getComputedStyle(list).columnGap) || 0;
    return card ? card.getBoundingClientRect().width + gap : list.clientWidth * 0.8;
  };

  const update = () => {
    const max = list.scrollWidth - list.clientWidth;
    arrows.hidden = max <= 1;
    back.disabled = list.scrollLeft <= 1;
    forward.disabled = list.scrollLeft >= max - 1;
  };

  const go = (dir) => list.scrollBy({ left: dir * step(), behavior: reduceMotion.matches ? 'auto' : 'smooth' });
  back.addEventListener('click', () => go(-1));
  forward.addEventListener('click', () => go(1));
  list.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);
  update();
});
