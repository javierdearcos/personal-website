/**
 * Internationalisation.
 *
 * `translations` holds every translatable string keyed by a dotted id.
 * Markup carries those ids via `data-i18n`; `applyLang()` rewrites the
 * matching elements' innerHTML. Card components also emit `data-i18n`
 * attributes, so `applyLang()` must run *after* they render.
 */
const translations = {
  es: {
    'skip': 'Saltar al contenido',
    'nav.about': 'Sobre mí',
    'nav.now': 'Ahora',
    'nav.talks': 'Charlas',
    'nav.collab': 'Colaboraciones',
    'nav.posts': 'Posts',
    'nav.projects': 'Proyectos',
    'nav.connect': 'Contacto',
    'hero.eyebrow': 'Engineering Manager',
    'hero.role': 'Servant Leader · Team Builder · Continuous Delivery Advocate',
    'hero.desc': 'Apasionado por construir <strong>equipos de alto rendimiento</strong> donde las personas pueden dar lo mejor de sí. Creo que el gran software es primero un problema de personas, y luego técnico.',
    'hero.cta1': 'Hablemos',
    'hero.cta2': 'Leer el blog ↗',
    'section.about.label': 'Áreas de enfoque',
    'section.about.title': 'Lo que me importa',
    'focus.servant.title': 'Servant Leadership',
    'focus.servant.desc': 'Eliminar bloqueos, crear el entorno correcto y habilitar a los equipos para que prosperen.',
    'focus.safety.title': 'Seguridad Psicológica',
    'focus.safety.desc': 'La cultura de equipo sana como base de todo lo demás. Sin miedo, con confianza.',
    'focus.cd.title': 'Entrega Continua',
    'focus.cd.desc': 'Flujo rápido, seguro y sostenible desde la idea hasta producción.',
    'focus.sharing.title': 'Aprender y Compartir',
    'focus.sharing.desc': 'Escribo y hablo sobre cultura de ingeniería, entrega y liderazgo.',
    'section.now.label': 'En este momento',
    'section.now.title': 'Actualmente',
    'now.1': 'Trabajando como <strong>Engineering Manager</strong>',
    'now.2': 'Estudiando un <strong>Grado en Psicología</strong> — porque la causa raíz de la mayoría de los problemas técnicos son las personas',
    'now.3': 'Participando en eventos como <strong>speaker y colaborador</strong> en podcasts para seguir aprendiendo y compartiendo',
    'now.4': 'Escribiendo sobre ingeniería, liderazgo y carrera en <a href="https://javierdearcos.com" target="_blank" rel="noopener">javierdearcos.com</a>',
    'now.5': 'Explorando: <strong>Kotlin · GIS · Equipos efectivos · IA</strong>',
    'section.talks.label': 'Conferencias y meetups',
    'section.talks.title': 'Charlas',
    'section.collab.label': 'Podcasts y entrevistas',
    'section.collab.title': 'Colaboraciones',
    'section.posts.label': 'Artículos destacados',
    'section.posts.title': 'Posts',
    'posts.more': 'Más artículos en',
    'section.projects.label': 'Código y comunidad',
    'section.projects.title': 'Proyectos',
    'project.rviewer': 'Diseñé y creé retos técnicos a distintos niveles para la plataforma Rviewer, usada por empresas para evaluar candidatos de ingeniería.',
    'project.teach': 'Enseñé fundamentos de desarrollo web a personas en riesgo de exclusión social que querían entrar en el sector tech.',
    'project.liferay': 'Contribuí a las APIs principales, tooling y el framework Objects como líder del equipo Headless API.',
    'project.oda': 'Lideré la implementación del agente IoT open-source para integrar dispositivos con la plataforma OpenGate IoT.',
    'project.ar': 'Librería de Realidad Aumentada para Android basada en ARToolKit. Proyecto Fin de Grado, distinguido con matrícula de honor.',
    'section.tech.label': 'Stack y herramientas',
    'section.tech.title': 'Tecnologías',
    'section.connect.label': 'Redes y contacto',
    'section.connect.title': 'Conectemos',
    'link.slides': 'Slides',
    'link.video': 'Video',
    'footer': '© 2026 Javier de Arcos · Hecho con HTML, CSS y ganas',
  },
  en: {
    'skip': 'Skip to content',
    'nav.about': 'About',
    'nav.now': 'Now',
    'nav.talks': 'Talks',
    'nav.collab': 'Collaborations',
    'nav.posts': 'Posts',
    'nav.projects': 'Projects',
    'nav.connect': 'Connect',
    'hero.eyebrow': 'Engineering Manager',
    'hero.role': 'Servant Leader · Team Builder · Continuous Delivery Advocate',
    'hero.desc': 'Passionate about building <strong>high-performance teams</strong> where people can do their best work. I believe great software is first a people problem, then a technical one.',
    'hero.cta1': "Let's talk",
    'hero.cta2': 'Read the blog ↗',
    'section.about.label': 'Focus areas',
    'section.about.title': 'What I care about',
    'focus.servant.title': 'Servant Leadership',
    'focus.servant.desc': 'Removing blockers, creating the right environment, and enabling teams to thrive.',
    'focus.safety.title': 'Psychological Safety',
    'focus.safety.desc': 'Healthy team culture as the foundation of everything else. No fear, full trust.',
    'focus.cd.title': 'Continuous Delivery',
    'focus.cd.desc': 'Fast, safe, and sustainable flow from idea to production.',
    'focus.sharing.title': 'Learn & Share',
    'focus.sharing.desc': 'I write and speak about engineering culture, delivery, and leadership.',
    'section.now.label': 'Right now',
    'section.now.title': 'Currently',
    'now.1': 'Working as <strong>Engineering Manager</strong>',
    'now.2': 'Studying a <strong>Psychology degree</strong> — because the root cause of most technical problems is people',
    'now.3': 'Participating in events as <strong>speaker and collaborator</strong> on podcasts to keep learning and sharing',
    'now.4': 'Writing about engineering, leadership and career at <a href="https://javierdearcos.com" target="_blank" rel="noopener">javierdearcos.com</a>',
    'now.5': 'Exploring: <strong>Kotlin · GIS · Building effective teams · AI</strong>',
    'section.talks.label': 'Conferences & meetups',
    'section.talks.title': 'Talks',
    'section.collab.label': 'Podcasts & interviews',
    'section.collab.title': 'Collaborations',
    'section.posts.label': 'Featured articles',
    'section.posts.title': 'Posts',
    'posts.more': 'More posts at',
    'section.projects.label': 'Code & community',
    'section.projects.title': 'Projects',
    'project.rviewer': 'Designed and created technical coding challenges at different skill levels for the Rviewer platform, used by companies to assess engineering candidates.',
    'project.teach': 'Taught web development fundamentals to people at risk of social exclusion wanting to enter the tech industry.',
    'project.liferay': 'Contributed to the main APIs, API tooling and the Objects framework as the Headless API team lead.',
    'project.oda': 'Led the implementation of the open-source IoT agent designed to integrate devices with the OpenGate IoT Platform.',
    'project.ar': 'Augmented Reality library for Android based on ARToolKit. Final Degree Project, awarded with the highest distinction.',
    'section.tech.label': 'Stack & tools',
    'section.tech.title': 'Technologies',
    'section.connect.label': 'Networks & contact',
    'section.connect.title': "Let's connect",
    'link.slides': 'Slides',
    'link.video': 'Video',
    'footer': '© 2026 Javier de Arcos · Built with HTML, CSS and passion',
  },
};

let currentLang = 'es';

/** Translate every `[data-i18n]` element into `lang`. */
export function applyLang(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  const t = translations[lang];
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.dataset.i18n;
    if (t[key] !== undefined) el.innerHTML = t[key];
  });
  const toggle = document.getElementById('langToggle');
  if (toggle) {
    toggle.textContent = lang === 'es' ? 'EN' : 'ES';
    toggle.setAttribute('aria-label', lang === 'es' ? 'Switch to English' : 'Cambiar a Español');
  }
}

/** Wire the nav language button to flip between ES and EN. */
export function initLangToggle() {
  const toggle = document.getElementById('langToggle');
  if (!toggle) return;
  toggle.addEventListener('click', () => {
    applyLang(currentLang === 'es' ? 'en' : 'es');
  });
}
