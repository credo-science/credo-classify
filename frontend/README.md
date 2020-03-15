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

**Wraning** if you use custom `CREDO_ENDPOINT` environment variable you should change the `user-interface/classification/`
phrase manually in `./package.json` and `./public/manifest.json` and **after build** in `./build/static/service-worker`.
TODO: apply it by build script.

## Translate to another languages

Files with translated messages are stored in `./src/translations` as `locale_XX.ts` pattern where `XX` is 2-letters or `xx-XX` pattern language code.
Language code should be compatible with `navigator.language` JavaScript browser's variable because it is checked as default language.
If `xx-XX` pattern translation is not provided then app try to cut code to `xx` and load translation.
If translation is not provided too then app load `en` translation.

### How to translate

Copy `./src/translations/locale_en.ts`. Translate all messages i quote on right of colon and send translated file to us.

We must add file with your translations and add your language to supported languages list in app.

## For developers

### Coding conventions

**ESLint** are used. Please run **prettier** before commit to github (CTRL+ALT+SHIFT+P in WebStorm, please check configuration in settings).

#### Components naming and placement in source code tree conventions

* `./src/api` - communication with backend
* `./src/layout` - layout helpers i.e. form fields, buttons and other visual controls
* `./src/context` - global app state, login state, current user state etc.
* `./src/site` - app pages,
  * each site page should be in separated subdirectory with `index.ts` file,
  * the depth of subdirectory should be equivalent to site map,
  * components having whole web page should have `Page` suffix,
  * bigger parts of site page should be divided to smaller components,
  * smaller components used only in one site page should be in the same subdirectory than site page,
  * reusable components (used in various site pages) should be in `/src/layout` or in `/src/{site_map_scope}/commons`
* `./src/translations` - translated messages
* `./src/utils` - other functions

#### Translated messages IDs conventions

There are some domains separated by dot.

For 3+ depth for components or for messages IDs please use abbreviations from https://www.allacronyms.com/ if possible.

##### Messages IDs for components
1. Component name in small letters with include the path to component source code file
(without `./site` or `./layout`) and separate by `_`. Example: `user_login` for `LoginPage` component in `./site/user/LoginPage.tsx`.
Please leave component name if placeholder is common for path scope. Example `user.email` for field used in `ForgotPage` and `RegisterPage`.
2. Placeholder or field in component.
3. Subplaceholder or conditional shown messages like validation errors. Examples:
   * `user_login.password` - label of password field in `LoginPage` component,
   * `user_login.password.help` - help placeholder for `password` field,
   * `user_login.password.inv` - message when value in password is not valid.
   
##### Messages IDs for global used messages
1. `msg` - always please use this in main domain.
2. Scope of message, examples:
   * `conn` - connection with server,
   * `inv` - not valid.
3. Variants, example:
   * `e` - error,
   * `w` - warning,
   * `s` - success,
   * `i` - info,
   * `p` - pending,
   * `req` - required.
