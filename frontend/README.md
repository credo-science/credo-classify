# CREDO-Classification PWA frontend

## Run in development environment

### Requirements

Installed `node` v12 or never.

### Run development version

```shell script
$ npm install
$ npm run start
```

And open in browser [http://localhost:3000/](http://localhost:3000/)

**Warning!** The backend is proxying from [http://localhost:8000/](http://localhost:8000/).
The configuration of proxy is in `package.json` in `"proxy"` field.

### Update translation files

```shell script
$ npm run i18n
```

Extracts new messages IDs and add append to `./src/translations/locale_en.ts`. You should fill its in english language.



### Build production version

```shell script
$ npm run build
```

The output files you found in `./build` directory.

## Translate to another languages

Files with translated messages are stored in `./src/translations` as `locale_XX.ts` pattern where `XX` is 2-letters or `xx-XX` pattern language code.
Language code should be compatible with `navigator.language` JavaScript browser's variable because it is checked as default language.
If `xx-XX` pattern translation is not provided then app try to cut code to `xx` and load translation.
If translation is not provided too then app load `en` translation.

### How to translate

Copy `./src/translations/locale_en.ts`. Translate all messages i quote on right of colon and send translated file to us.

We must add file with your translations and add your language to supported languages list in app. 
