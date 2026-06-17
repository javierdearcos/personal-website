/**
 * Professional career timeline (most recent first).
 *
 * Only the non-translatable bits live here: the company name and the number
 * of bullet points. Every translatable string (role, period, summary and each
 * bullet) lives in js/i18n.js under `career.<id>.*` keys, so <career-card>
 * emits matching `data-i18n` placeholders that applyLang() fills in.
 */
export const career = [
  { id: 'technosylva', company: 'Technosylva', bullets: 3 },
  { id: 'celonis',     company: 'Celonis',     bullets: 3 },
  { id: 'huspy',       company: 'Huspy',       bullets: 2 },
  { id: 'liferay',     company: 'Liferay',     bullets: 3 },
  { id: 'amplia',      company: 'Amplía',      bullets: 2 },
  { id: 'gmv',         company: 'GMV',         bullets: 1 },
  { id: 'fcc',         company: 'FCC',         bullets: 1 },
  { id: 'andanta',     company: 'Andanta',     bullets: 2 },
  { id: 'ixion',       company: 'IXION',       bullets: 2 },
  { id: 'upm',         company: 'UPM',         bullets: 0 },
];
