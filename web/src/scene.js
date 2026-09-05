import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

const clamp = THREE.MathUtils.clamp;

export class CausalWorldScene {
  constructor(canvas) {
    this.canvas = canvas;
    this.reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.pointer = new THREE.Vector2(0, 0);
    this.scroll = 0;
    this.mode = 'factual';
    this.modeMix = 0;
    this.clock = new THREE.Clock();
    this.time = 0;

    this.scene = new THREE.Scene();
    this.scene.fog = new THREE.FogExp2(0x050814, 0.055);

    this.camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    this.camera.position.set(0, 1.4, 12.2);

    this.renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.8));
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.15;

    this.composer = new EffectComposer(this.renderer);
    this.composer.addPass(new RenderPass(this.scene, this.camera));
    this.bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.72, 0.7, 0.18);
    this.composer.addPass(this.bloom);

    this.root = new THREE.Group();
    this.scene.add(this.root);

    this.createLights();
    this.createStarfield();
    this.createGrid();
    this.createLatentCore();
    this.createCollisionSystem();
    this.createTrajectories();

    this.onPointerMove = this.onPointerMove.bind(this);
    this.onResize = this.onResize.bind(this);
    this.onScroll = this.onScroll.bind(this);
    this.animate = this.animate.bind(this);

    window.addEventListener('pointermove', this.onPointerMove, { passive: true });
    window.addEventListener('resize', this.onResize);
    window.addEventListener('scroll', this.onScroll, { passive: true });

    this.onResize();
    this.animate();
  }

  createLights() {
    this.scene.add(new THREE.HemisphereLight(0x6edfff, 0x080815, 0.55));
    const key = new THREE.PointLight(0x69e8ff, 35, 20, 2);
    key.position.set(4, 5, 7);
    this.scene.add(key);
    const rim = new THREE.PointLight(0x8f7bff, 30, 18, 2);
    rim.position.set(-5, 1, 4);
    this.scene.add(rim);
    const mint = new THREE.PointLight(0x84ffd6, 18, 15, 2);
    mint.position.set(0, -4, 3);
    this.scene.add(mint);
  }

  createStarfield() {
    const count = 900;
    const positions = new Float32Array(count * 3);
    const sizes = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      const r = 13 + Math.random() * 28;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(THREE.MathUtils.randFloatSpread(2));
      positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = r * Math.cos(phi);
      sizes[i] = 0.5 + Math.random() * 1.5;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    const mat = new THREE.PointsMaterial({ color: 0x8bbaff, size: 0.035, transparent: true, opacity: 0.55, sizeAttenuation: true });
    this.stars = new THREE.Points(geo, mat);
    this.scene.add(this.stars);
  }

  createGrid() {
    const grid = new THREE.GridHelper(28, 34, 0x183253, 0x10243d);
    grid.material.opacity = 0.24;
    grid.material.transparent = true;
    grid.position.y = -2.9;
    grid.rotation.z = 0.02;
    this.scene.add(grid);

    const planeMat = new THREE.MeshPhysicalMaterial({
      color: 0x06101f,
      roughness: 0.35,
      metalness: 0.25,
      transparent: true,
      opacity: 0.28,
      clearcoat: 1,
      clearcoatRoughness: 0.18,
      side: THREE.DoubleSide,
    });
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(24, 15), planeMat);
    plane.rotation.x = -Math.PI / 2;
    plane.position.y = -2.94;
    this.scene.add(plane);
  }

  createLatentCore() {
    this.coreGroup = new THREE.Group();
    this.coreGroup.position.set(0.2, 0.6, -0.5);
    this.root.add(this.coreGroup);

    const inner = new THREE.Mesh(
      new THREE.IcosahedronGeometry(1.05, 5),
      new THREE.MeshPhysicalMaterial({
        color: 0x72eeff,
        emissive: 0x174a66,
        emissiveIntensity: 1.7,
        metalness: 0.1,
        roughness: 0.12,
        transparent: true,
        opacity: 0.46,
        transmission: 0.4,
        thickness: 0.8,
      }),
    );
    this.coreInner = inner;
    this.coreGroup.add(inner);

    const wire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(1.28, 2),
      new THREE.MeshBasicMaterial({ color: 0x9eefff, wireframe: true, transparent: true, opacity: 0.22 }),
    );
    this.coreWire = wire;
    this.coreGroup.add(wire);

    this.rings = [];
    const ringColors = [0x69e8ff, 0x8f7bff, 0x84ffd6];
    for (let i = 0; i < 3; i++) {
      const ring = new THREE.Mesh(
        new THREE.TorusGeometry(1.75 + i * 0.24, 0.012, 12, 180),
        new THREE.MeshBasicMaterial({ color: ringColors[i], transparent: true, opacity: 0.33 - i * 0.055 }),
      );
      ring.rotation.set(0.65 + i * 0.4, 0.15 + i * 0.8, i * 0.52);
      this.coreGroup.add(ring);
      this.rings.push(ring);
    }

    const nodeGeo = new THREE.SphereGeometry(0.055, 12, 12);
    const nodeMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    this.nodes = new THREE.Group();
    for (let i = 0; i < 14; i++) {
      const n = new THREE.Mesh(nodeGeo, nodeMat.clone());
      const a = i / 14 * Math.PI * 2;
      const r = 1.7 + (i % 3) * 0.16;
      n.position.set(Math.cos(a) * r, Math.sin(a * 1.7) * 0.65, Math.sin(a) * r * 0.55);
      n.material.color.set(i % 2 ? 0x69e8ff : 0x8f7bff);
      this.nodes.add(n);
    }
    this.coreGroup.add(this.nodes);
  }

  createCollisionSystem() {
    this.collisionGroup = new THREE.Group();
    this.collisionGroup.position.set(0, -1.6, 0.7);
    this.root.add(this.collisionGroup);

    const ballGeo = new THREE.SphereGeometry(0.38, 48, 48);
    this.ballAMat = new THREE.MeshPhysicalMaterial({ color: 0x8ff5ff, emissive: 0x0b6680, emissiveIntensity: 0.85, metalness: 0.18, roughness: 0.16, clearcoat: 1 });
    this.ballBMat = new THREE.MeshPhysicalMaterial({ color: 0xa38fff, emissive: 0x382b8c, emissiveIntensity: 0.85, metalness: 0.18, roughness: 0.16, clearcoat: 1 });
    this.ballA = new THREE.Mesh(ballGeo, this.ballAMat);
    this.ballB = new THREE.Mesh(ballGeo, this.ballBMat);
    this.ballA.position.x = -3.5;
    this.ballB.position.x = 1.35;
    this.collisionGroup.add(this.ballA, this.ballB);

    const track = new THREE.Mesh(
      new THREE.BoxGeometry(9.5, 0.06, 0.78),
      new THREE.MeshPhysicalMaterial({ color: 0x0d2440, emissive: 0x071222, emissiveIntensity: 0.25, roughness: 0.3, metalness: 0.35, transparent: true, opacity: 0.65 }),
    );
    track.position.y = -0.46;
    this.collisionGroup.add(track);

    const tickMat = new THREE.MeshBasicMaterial({ color: 0x346286, transparent: true, opacity: 0.38 });
    for (let i = -9; i <= 9; i++) {
      const tick = new THREE.Mesh(new THREE.BoxGeometry(0.012, 0.02, 0.5), tickMat);
      tick.position.set(i * 0.5, -0.42, 0);
      this.collisionGroup.add(tick);
    }
  }

  createTrajectories() {
    const makeCurve = (color, y, bend) => {
      const pts = [];
      for (let i = 0; i < 70; i++) {
        const t = i / 69;
        pts.push(new THREE.Vector3(-4 + t * 8, y + Math.sin(t * Math.PI) * bend, -0.6 - t * 0.35));
      }
      const curve = new THREE.CatmullRomCurve3(pts);
      const geo = new THREE.TubeGeometry(curve, 90, 0.012, 6, false);
      const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.16 });
      return new THREE.Mesh(geo, mat);
    };
    this.trajA = makeCurve(0x69e8ff, -1.58, 0.34);
    this.trajB = makeCurve(0x8f7bff, -1.74, -0.28);
    this.root.add(this.trajA, this.trajB);
  }

  setMode(mode) {
    this.mode = mode;
  }

  onPointerMove(e) {
    this.pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
    this.pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;
  }

  onScroll() {
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    this.scroll = window.scrollY / max;
  }

  onResize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h, false);
    this.composer.setSize(w, h);
  }

  updateCollision(t) {
    this.modeMix += ((this.mode === 'counterfactual' ? 1 : 0) - this.modeMix) * 0.055;
    const cycle = (t * 0.18) % 1;
    const reset = cycle < 0.04;
    const collisionT = 0.48;
    const massFactor = THREE.MathUtils.lerp(1.0, 2.4, this.modeMix);
    const incomingSpeed = 6.2;

    let ax, bx;
    if (cycle < collisionT) {
      ax = -3.55 + (cycle / collisionT) * 4.45;
      bx = 1.35;
    } else {
      const u = (cycle - collisionT) / (1 - collisionT);
      const postA = (1 - massFactor) / (1 + massFactor);
      const postB = 2 / (1 + massFactor);
      ax = 0.90 + postA * u * incomingSpeed * 0.62;
      bx = 1.35 + postB * u * incomingSpeed * 0.62;
    }
    if (reset) {
      ax = -3.55;
      bx = 1.35;
    }
    this.ballA.position.x = ax;
    this.ballB.position.x = bx;
    this.ballA.rotation.z -= 0.035;
    this.ballB.rotation.z += 0.021 * (1.2 - this.modeMix * 0.35);

    const counterColor = new THREE.Color(0xf16dff);
    const factualColor = new THREE.Color(0x8f7bff);
    this.ballBMat.color.copy(factualColor).lerp(counterColor, this.modeMix * 0.55);
    this.ballBMat.emissive.copy(new THREE.Color(0x382b8c).lerp(new THREE.Color(0x6b1f79), this.modeMix));
    this.coreInner.material.color.copy(new THREE.Color(0x72eeff).lerp(new THREE.Color(0xb98bff), this.modeMix));
    this.coreInner.material.emissive.copy(new THREE.Color(0x174a66).lerp(new THREE.Color(0x4d226a), this.modeMix));
  }

  animate() {
    const dt = Math.min(this.clock.getDelta(), 0.05);
    this.time += dt;
    const t = this.time;

    if (!this.reducedMotion) {
      this.coreGroup.rotation.y = t * 0.17 + this.pointer.x * 0.12;
      this.coreGroup.rotation.x = Math.sin(t * 0.33) * 0.08 - this.pointer.y * 0.07;
      this.coreInner.rotation.y -= dt * 0.18;
      this.coreWire.rotation.x += dt * 0.12;
      this.rings.forEach((ring, i) => {
        ring.rotation.z += dt * (0.12 + i * 0.035) * (i % 2 ? -1 : 1);
        ring.rotation.y += dt * 0.035;
      });
      this.nodes.rotation.y -= dt * 0.08;
      this.stars.rotation.y += dt * 0.004;
      this.stars.rotation.x = Math.sin(t * 0.08) * 0.025;
    }

    this.updateCollision(t);

    const scrollTilt = this.scroll;
    const targetX = this.pointer.x * 0.25 + Math.sin(scrollTilt * Math.PI) * 0.28;
    const targetY = 1.35 + this.pointer.y * 0.12 - scrollTilt * 0.48;
    this.camera.position.x += (targetX - this.camera.position.x) * 0.035;
    this.camera.position.y += (targetY - this.camera.position.y) * 0.035;
    this.camera.lookAt(0, -0.15, 0);
    this.root.position.y = scrollTilt * 0.42;
    this.root.rotation.z = -this.pointer.x * 0.012;

    this.trajA.material.opacity = 0.11 + Math.sin(t * 1.1) * 0.025;
    this.trajB.material.opacity = 0.11 + Math.cos(t * 1.2) * 0.025 + this.modeMix * 0.08;
    this.bloom.strength = 0.64 + this.modeMix * 0.16;

    this.composer.render();
    requestAnimationFrame(this.animate);
  }
}
