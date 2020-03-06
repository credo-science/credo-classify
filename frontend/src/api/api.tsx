import React, { useState, useEffect, useRef, useContext, useCallback } from "react";
import { FormikHelpers } from "formik/dist/types";
import axios, { AxiosError, AxiosResponse, Canceler, Method } from "axios";
import { ErrorResponse } from "./rqre";
import { AppContext } from "../context/AppContext";
import { useI18n } from "../utils";
import { I18n } from "../utils/i18n";
import { PrimitiveType } from "intl-messageformat";

/**
 * Optional options for api() async method
 */
export interface ApiOptions<Pr = any, Rq = any> {
  /** HTTP method, default: GET */
  method?: Method;

  /** Params added to URL after "?" (@see: axios) */
  params?: Pr;

  /** Data uploaded as JSON to server (@see: axios). Ignored when method="GET" */
  data?: Rq;

  /** Used for cancellation. If canceler.current is not null then do cancel. (@see: axios and React.createRef) */
  canceler?: React.MutableRefObject<Canceler | null>;

  /** Execute when HTTP 401 error was received: is no logged or token was void */
  onNoLogged?: () => void;
}

const defaultApiOptions: ApiOptions = { method: "GET" };

/**
 * Throw when API occur an error.
 */
export class ApiError extends Error {
  /** Form fields server-side validation errors. */
  fields: object;

  /** Values injected to translated error message. Ignored when @field i18n is false. @see: react-intl and FormatMessage method */
  values?: Record<string, PrimitiveType>;

  /** When true then Error.message contains ID of translated message, otherwise contains other message from server */
  i18n: boolean;

  constructor(message: string, fields: object, i18n: boolean = false, values?: Record<string, PrimitiveType>) {
    super(message);
    this.fields = fields;
    this.values = values;
    this.i18n = i18n;
  }

  /**
   * Return Exception.message translated by i18n() or not according to this.i18n value.
   * @param i18n message translator
   */
  getMessage = (i18n: I18n) => {
    return this.i18n ? i18n(this.message, this.values) : this.message;
  };
}

/**
 * Wrapper to axios. Support:
 * 1. Run canceler is set.
 * 2. Add authorization token header if set.
 * 3. Return null when canceled instead throw exception.
 * 4. Wrap server error (connection, token void, forbidden, not found, server-side form fields validation and other server error messages) to @see ApiError
 * @param endpoint URL to connection
 * @param token authorization token
 * @param options others no required options @see ApiOptions
 */
export async function api<Pr, Rq, Re>(endpoint: string, token: string | null, options?: ApiOptions<Pr, Rq>): Promise<Re | undefined> {
  const { method, params, data, canceler, onNoLogged } = { ...defaultApiOptions, ...(options || {}) };
  const isGet = method!.toLowerCase() === "get";

  canceler?.current?.();
  const _ = (a: string) => a; // for catching by extract_i18n_messages.js

  try {
    const result: AxiosResponse<Re> = await axios({
      method,
      url: endpoint,
      params: params,
      data: isGet ? null : data,
      headers: token ? { Authorization: `Token ${token}` } : null,
      cancelToken:
        canceler &&
        new axios.CancelToken(c => {
          canceler.current = c;
        })
    });

    return result.data;
  } catch (error) {
    if (!axios.isCancel(error)) {
      const { response } = error as AxiosError<ErrorResponse>;
      if (response) {
        if (response.data) {
          if (response.data.non_field_errors) {
            throw new ApiError(response.data.non_field_errors.join("\n"), response.data);
          } else {
            throw new ApiError(_("msg.conn.e.cli"), response.data, true, { fields: Object.keys(response.data).length });
          }
        } else {
          let err;
          if (response.status === 401) {
            err = _("msg.conn.e.401");
            onNoLogged?.();
          } else if (response.status === 403) {
            err = _("msg.conn.e.403");
          } else if (response.status === 404) {
            err = _("msg.conn.e.404");
          } else {
            err = _("msg.conn.e.srv");
          }
          throw new ApiError(err, {}, true);
        }
      } else {
        throw new ApiError(_("msg.conn.e"), {}, true);
      }
    }
  } finally {
    if (canceler) {
      canceler.current = null;
    }
  }
}

export interface FormikStatus {
  status?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
  message?: string;
}

export function useFormikApi<Rq, Re>(
  method: Method,
  endpoint: string,
  onSuccess: ((request: Rq, response: Re) => void) | null = null,
  onFail: ((request: Rq, response: Re | ErrorResponse | null, formikHelpers: FormikHelpers<Rq>) => void) | null = null
): { data: Re | null; onSubmit: (values: Rq, formikHelpers: FormikHelpers<Rq>) => void } {
  const [data, setData] = useState<Re | null>(null);
  const canceler = useRef<Canceler | null>(null);
  const _ = useI18n();
  const { token } = useContext(AppContext);

  const onSubmit = useCallback(
    async (values: Rq, formikHelpers: FormikHelpers<Rq>) => {
      try {
        const result = await api<any, Rq, Re>(endpoint, token, { method, canceler, data: values });
        if (result != null) {
          setData(result);
          formikHelpers.setSubmitting(false);
          formikHelpers.setStatus({ status: "success", message: _("msg.conn.s") } as FormikStatus);
          onSuccess?.(values, result);
        }
      } catch (ApiError) {
        formikHelpers.setSubmitting(false);
        formikHelpers.setStatus({ status: "danger", message: ApiError.getMessage(_) } as FormikStatus);
        formikHelpers.setErrors(ApiError.fields);
        onFail?.(values, ApiError, formikHelpers);
      }
    },
    [_, method, onFail, onSuccess, token]
  );

  useEffect(() => {
    return () => {
      if (canceler.current != null) {
        canceler.current();
        canceler.current = null;
      }
    };
  }, [endpoint, method]);

  return { data, onSubmit };
}

export function useApi<Rq, Re>(
  method: Method,
  endpoint: string,
  onSuccess: ((request: Rq, response: Re) => void) | null = null,
  onFail: ((request: Rq, response: Re | ApiError | null) => void) | null = null
): { isLoading: boolean; data: Re | null; onQuery: (values: Rq) => void; errors: Re | ApiError | null } {
  const [isLoading, setLoading] = useState(false);
  const [data, setData] = useState<Re | null>(null);
  const [errors, setErrors] = useState<Re | ApiError | null>(null);
  const canceler = useRef<Canceler | null>(null);
  const _ = useI18n();
  const { token } = useContext(AppContext);

  const onQuery = useCallback(
    async (values: Rq) => {
      try {
        const result = await api<any, Rq, Re>(endpoint, token, { method, canceler, data: values });
        if (result != null) {
          setData(result);
          setLoading(false);
          onSuccess?.(values, result);
        }
      } catch (ApiError) {
        setLoading(false);
        setErrors(ApiError);
        onFail?.(values, ApiError);
      }
    },
    [method, endpoint, token, onSuccess, onFail, _]
  );

  useEffect(() => {
    return () => {
      if (canceler.current != null) {
        canceler.current();
        canceler.current = null;
      }
    };
  }, [endpoint, method]);

  return { isLoading, data, onQuery, errors };
}

export function useGet<Rq, Re>(
  endpoint: string,
  values?: any
): { isLoading: boolean; data: Re | null; errors: Re | ApiError | null; onQuery: (values: Rq) => void } {
  const { isLoading, data, errors, onQuery } = useApi<Rq, Re>("GET", endpoint);
  useEffect(() => {
    onQuery(values);
  }, [endpoint, values, onQuery]);
  return { isLoading, data, errors, onQuery };
}
