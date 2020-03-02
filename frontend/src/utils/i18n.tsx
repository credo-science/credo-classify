import { useIntl } from "react-intl";
import { PrimitiveType } from "intl-messageformat";
import { useCallback } from "react";
import en from "../translations/locale_en";
import pl from "../translations/locale_pl";
import { MessageFormatElement } from "intl-messageformat-parser";

export type Messages = Record<string, string> | Record<string, MessageFormatElement[]>;
const messages: { [lang: string]: Messages } = { en, pl };

export function useI18n() {
  const { formatMessage } = useIntl();
  return useCallback((id: string, values?: Record<string, PrimitiveType>) => formatMessage({ id }, values), [formatMessage]);
}

export function getI18nMessages(language: string): Messages {
  const subLang = language.substr(0, 2);
  const msg = messages[language] || messages[subLang] || en;
  return { ...en, ...msg };
}
