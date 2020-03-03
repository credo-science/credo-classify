import { useIntl } from "react-intl";
import { PrimitiveType } from "intl-messageformat";
import React, { useCallback, ComponentType, FC } from "react";
import en from "../translations/locale_en";
import pl from "../translations/locale_pl";
import { MessageFormatElement } from "intl-messageformat-parser";

export type Messages = Record<string, string> | Record<string, MessageFormatElement[]>;
const messages: { [lang: string]: Messages } = { en, pl };

export type I18n = (id: string, values?: Record<string, PrimitiveType>) => string;

export function useI18n(): I18n {
  const { formatMessage } = useIntl();
  return useCallback((id, values) => formatMessage({ id }, values), [formatMessage]);
}

export function getI18nMessages(language: string): Messages {
  const subLang = language.substr(0, 2);
  const msg = messages[language] || messages[subLang] || en;
  return { ...en, ...msg };
}

type ShadowInjected<T1, T2> = Omit<T1, keyof T2>;

interface HOCProps {
  foo: number;
}

export const withSomething = <T extends HOCProps>(WrappedComponent: React.ComponentType<T>): React.FC<ShadowInjected<T, HOCProps>> => {
  return function WithSomething(props: ShadowInjected<T, HOCProps>) {
    // Do you HOC work here
    return <WrappedComponent foo={1337} {...(props as T)} />;
  };
};

export interface WithI18nProps {
  _: I18n;
}

type WithoutI18nProps<T> = Omit<T, keyof WithI18nProps>;

export function withI18n<T extends WithI18nProps>(WrappedComponent: ComponentType<T>): FC<WithoutI18nProps<T>> {
  return (props: WithoutI18nProps<T>) => {
    const _ = useI18n();
    return <WrappedComponent _={_} {...(props as T)} />;
  };
}
