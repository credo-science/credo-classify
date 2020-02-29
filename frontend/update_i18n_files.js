/**
 * Add new messages from en translation to others of the supported languages.
 *
 * Run:
 * npm run i18n-update
 *
 * Should be run after `npm run i18n-extract` and filled extracted messages in en translation.
 */
const supportedLanguages = ["pl"];

const { getFileName, loadTranslations, saveTranslations, mergeTranslations } = require("./utils/i18n_utils");

const en = loadTranslations(getFileName("en"));

supportedLanguages.forEach(r => {
  const fn = getFileName(r);
  const ot = loadTranslations(fn);
  saveTranslations(fn, mergeTranslations(en, ot));
  console.log(`Updated ${fn} file, please check changes`)
});
