/**
 * Extract new _("???") and _('???') expressions from source code and append to ./src/translations/locale_en.ts.
 *
 * Run:
 * npm run i18n-extract
 */
const fs = require("fs");
const glob = require("glob");
const { getFileName, loadTranslations, saveTranslations, mergeTranslations } = require("./utils/i18n_utils");
const pattern = "src/**/*.@(tsx|ts|js|jsx)";

let found = [];

function searchAndAppend(contents, found, pattern) {
  const res = contents.match(pattern);
  if (res) {
    return found.concat(res);
  }
  return found;
}

const files = glob(pattern, { sync: true });
files.forEach(f => {
  const contents = fs.readFileSync(f).toString();

  found = searchAndAppend(contents, found, /_\("[^)]+"/g);
  found = searchAndAppend(contents, found, /_\('[^)]+'/g);
});

let extracted = {};

found.forEach(r => {
  const id = r.substr(3, r.length - 4);
  extracted[id] = `!untranslated! ${id}`;
});

const fn = getFileName("en");
const data = loadTranslations(fn);
const toSave = mergeTranslations(extracted, data);
saveTranslations(fn, toSave);
console.log(`Updated ${fn} file, please check changes`);
