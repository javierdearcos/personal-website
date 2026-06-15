/**
 * Focus areas shown in the "Lo que me importa / What I care about" grid.
 * `titleKey` / `descKey` map to the i18n catalog; `title` / `desc` are the
 * Spanish defaults rendered before (or without) the i18n pass.
 */
export const focusAreas = [
  {
    icon: '🧭',
    titleKey: 'focus.servant.title', title: 'Servant Leadership',
    descKey: 'focus.servant.desc',
    desc: 'Eliminar bloqueos, crear el entorno correcto y habilitar a los equipos para que prosperen.',
  },
  {
    icon: '🤝',
    titleKey: 'focus.safety.title', title: 'Seguridad Psicológica',
    descKey: 'focus.safety.desc',
    desc: 'La cultura de equipo sana como base de todo lo demás. Sin miedo, con confianza.',
  },
  {
    icon: '🚀',
    titleKey: 'focus.cd.title', title: 'Entrega Continua',
    descKey: 'focus.cd.desc',
    desc: 'Flujo rápido, seguro y sostenible desde la idea hasta producción.',
  },
  {
    icon: '📣',
    titleKey: 'focus.sharing.title', title: 'Aprender y Compartir',
    descKey: 'focus.sharing.desc',
    desc: 'Escribo y hablo sobre cultura de ingeniería, entrega y liderazgo.',
  },
];
