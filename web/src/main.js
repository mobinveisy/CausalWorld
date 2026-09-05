import './style.css';
import { CausalWorldScene } from './scene.js';

const canvas = document.querySelector('#webgl');
let scene;
try {
  scene = new CausalWorldScene(canvas);
} catch (error) {
  console.error('Three.js scene failed to initialize:', error);
  document.documentElement.classList.add('no-webgl');
  canvas.style.display = 'none';
}

const modes = document.querySelectorAll('.mode');
const massValue = document.querySelector('#massValue');
const velocityValue = document.querySelector('#velocityValue');
const editValue = document.querySelector('#editValue');
const latentValue = document.querySelector('#latentValue');

const factual = {
  mass: '1.00×',
  velocity: '0.91',
  edit: 'OFF',
  latent: 'z = [0.41, −0.08, 0.77, …]',
};
const counterfactual = {
  mass: '2.40×',
  velocity: '0.53',
  edit: 'ON',
  latent: 'z′ = [0.72, 0.31, −0.19, …]',
};

function setMode(mode) {
  modes.forEach((button) => button.classList.toggle('active', button.dataset.mode === mode));
  const data = mode === 'counterfactual' ? counterfactual : factual;
  massValue.textContent = data.mass;
  velocityValue.textContent = data.velocity;
  editValue.textContent = data.edit;
  latentValue.textContent = data.latent;
  scene?.setMode(mode);
}

modes.forEach((button) => button.addEventListener('click', () => setMode(button.dataset.mode)));

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.13, rootMargin: '0px 0px -8% 0px' });

document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

const cursorGlow = document.querySelector('.cursor-glow');
window.addEventListener('pointermove', (event) => {
  cursorGlow.style.left = `${event.clientX}px`;
  cursorGlow.style.top = `${event.clientY}px`;
}, { passive: true });

window.addEventListener('pointerleave', () => { cursorGlow.style.opacity = '0'; });
window.addEventListener('pointerenter', () => { cursorGlow.style.opacity = ''; });

setMode('factual');
