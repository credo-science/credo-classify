const fs = require("fs");

/**
 * Get path of file with translated messages.
 * @param lang language as xx or xx-XX format
 * @return {string} local path (based on project root directory) to locale_{lang}.ts file
 */
function getFileName(lang) {
  return `./src/translations/locale_${lang}.ts`;
}

/**
 * Load translation messages to dictionary object.
 * @param fn path to file with translated messages
 * @return id:message pair as dictionary object
 */
function loadTranslations(fn) {
  return fs.existsSync(fn)
    ? JSON.parse(
        fs
          .readFileSync(fn)
          .toString()
          .replace("export default ", "")
          .replace(";", "")
      )
    : {};
}

/**
 * Merge two translations.
 * @param orig original dictionary
 * @param changed dictionary with new or updated translations
 */
function mergeTranslations(orig, changed) {
  return { ...orig, ...changed };
}

/**
 * Save dictionary object with translated messages in file.
 * @param fn path to file with translated messages
 * @param translations dictionary object with translated messages
 */
function saveTranslations(fn, translations) {
  fs.writeFileSync(fn, `export default ${JSON.stringify(translations, Object.keys(translations).sort(), 2)};\n`);
}

module.exports = { getFileName, loadTranslations, mergeTranslations, saveTranslations };
