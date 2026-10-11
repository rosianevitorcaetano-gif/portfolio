// ITIL 4 path: trace one recurring incident through the four modules.
// Selecting a journey step lights up the stage it belongs to; hovering a stage
// points at the journey steps that happen inside it.
const flow = document.querySelector('[data-itil-flow]');
const journey = document.querySelector('[data-journey]');

if (flow && journey) {
  const stages = [...flow.querySelectorAll('.stage[data-module]')];
  const steps = [...journey.querySelectorAll('.journey-step')];
  const playBtn = journey.querySelector('[data-journey-play]');
  const resetBtn = journey.querySelector('[data-journey-reset]');
  const status = journey.querySelector('[data-journey-status]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const moduleNames = {
    cds: 'Create, Deliver and Support',
    msf: 'Monitor, Support and Fulfil',
    pic: 'Plan, Implement and Control',
    dpi: 'Direct, Plan and Improve',
  };
  const last = steps.length - 1;
  let current = -1;
  let timer = null;

  const modulesOf = (step) => [step.dataset.module, step.dataset.also].filter(Boolean);

  function show(index) {
    current = index;
    const step = steps[index];
    const lit = modulesOf(step);
    steps.forEach((s, i) => {
      s.classList.toggle('is-active', i === index);
      s.classList.toggle('is-done', i < index);
      s.setAttribute('aria-pressed', String(i === index));
    });
    flow.classList.add('is-tracing');
    stages.forEach((stage) => stage.classList.toggle('is-lit', lit.includes(stage.dataset.module)));
    const practice = step.querySelector('.jstep-practice').textContent.trim();
    status.textContent = `Step ${index + 1} of ${steps.length}: ${practice} (${moduleNames[step.dataset.module]})`;
  }

  function playLabel() {
    if (current >= last) return 'Trace again';
    if (current >= 0) return reduceMotion.matches ? 'Next step' : 'Continue';
    return 'Trace the path';
  }

  function stop() {
    clearInterval(timer);
    timer = null;
    playBtn.textContent = playLabel();
  }

  function reset() {
    stop();
    current = -1;
    steps.forEach((s) => {
      s.classList.remove('is-active', 'is-done');
      s.setAttribute('aria-pressed', 'false');
    });
    flow.classList.remove('is-tracing');
    stages.forEach((stage) => stage.classList.remove('is-lit'));
    status.textContent = '';
    playBtn.textContent = playLabel();
  }

  playBtn.addEventListener('click', () => {
    if (timer) {
      stop();
      return;
    }
    if (current >= last) current = -1;
    show(current + 1);

    // Without motion, each click moves one step instead of auto-playing.
    if (reduceMotion.matches || current >= last) {
      playBtn.textContent = playLabel();
      return;
    }
    playBtn.textContent = 'Pause';
    timer = setInterval(() => {
      show(current + 1);
      if (current >= last) stop();
    }, 1800);
  });

  resetBtn.addEventListener('click', reset);

  steps.forEach((step, i) => {
    step.addEventListener('click', () => {
      stop();
      show(i);
      playBtn.textContent = playLabel();
    });
  });

  stages.forEach((stage) => {
    const related = steps.filter((s) => modulesOf(s).includes(stage.dataset.module));
    stage.addEventListener('mouseenter', () => related.forEach((s) => s.classList.add('is-related')));
    stage.addEventListener('mouseleave', () => related.forEach((s) => s.classList.remove('is-related')));
  });
}
