/**
 * Featured blog posts shown in the "Posts" grid on the home page.
 * These link to the migrated posts under /blog/. The full archive
 * lives at /blog/.
 *
 * `tag`, `title` and `desc` are `{ es, en }` pairs so the cards follow the
 * global language toggle (see js/components/entry-card.js). The full post
 * bodies are translated separately under blog-src/<slug>/en.html.
 */
export const posts = [
  {
    icon: '🌳',
    tag: { es: 'Personal', en: 'Personal' },
    year: '2025',
    title: { es: 'Tree shaking para la vida real', en: 'Tree shaking for real life' },
    url: '/blog/tree-shaking/',
    desc: {
      es: 'Sobre foco, prioridades y eliminar lo innecesario.',
      en: 'On focus, priorities, and removing the unnecessary.',
    },
  },
  {
    icon: '🦑',
    tag: { es: 'Carrera', en: 'Career' },
    year: '2025',
    title: { es: 'El Juego del Calamar', en: 'Squid Game' },
    url: '/blog/squid-game/',
    desc: {
      es: 'Sobre el burnout y los juegos que no elegimos jugar.',
      en: "On burnout and the games we don't choose to play.",
    },
  },
  {
    icon: '⚔️',
    tag: { es: 'Liderazgo', en: 'Leadership' },
    year: '2025',
    title: { es: 'Conmigo o contra mí', en: 'With me or against me' },
    url: '/blog/with-me-or-against-me/',
    desc: {
      es: 'Sobre liderazgo tóxico y la alternativa de la que casi nunca hablamos.',
      en: 'On toxic leadership and the alternative we rarely talk about.',
    },
  },
];
