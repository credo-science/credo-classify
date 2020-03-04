import React, { useState, useEffect, useRef, useContext, useCallback } from "react";
import { FormikHelpers } from "formik/dist/types";
import axios, { AxiosError, AxiosResponse, Canceler, Method } from "axios";
import { ErrorResponse } from "./rqre";
import { AppContext } from "../context/AppContext";
import { useI18n } from "../utils";
import { I18n } from "../utils/i18n";
import { PrimitiveType } from "intl-messageformat";

export interface ApiOptions<Re = any> {
  method?: Method;
  data?: Re;
  canceler?: React.MutableRefObject<Canceler | null>;
}

const defaultApiOptions: ApiOptions = { method: "GET" };

export class ApiError extends Error {
  fields: object;
  values?: Record<string, PrimitiveType>;
  i18n: boolean;

  constructor(message: string, fields: object, i18n: boolean = false, values?: Record<string, PrimitiveType>) {
    super(message);
    this.fields = fields;
    this.values = values;
    this.i18n = i18n;
  }

  getMessage = (i18n: I18n) => {
    return this.i18n ? i18n(this.message, this.values) : this.message;
  };
}

export async function api<Rq, Re>(endpoint: string, token: string | null, options?: ApiOptions<Re>): Promise<Re | undefined> {
  const { method, data, canceler } = { ...defaultApiOptions, ...(options || {}) };
  const isGet = method!.toLowerCase() === "get";

  canceler?.current?.();
  const _ = (a: string) => a; // for catching by extract_i18n_messages.js

  try {
    const result: AxiosResponse<Re> = await axios({
      method,
      url: endpoint,
      params: isGet ? data : null,
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
    if (axios.isCancel(error)) {
      if (canceler) {
        canceler.current = null;
      }
    } else {
      const { response } = error as AxiosError<ErrorResponse>;
      if (response) {
        if (response.data) {
          if (response.data.non_field_errors) {
            throw new ApiError(response.data.non_field_errors.join("\n"), response.data);
          } else {
            throw new ApiError(_("msg.conn.e.cli"), response.data, true, { fields: Object.keys(response.data).length });
          }
        } else {
          let err = "";
          if (response.status === 401) {
            err = _("msg.conn.e.401");
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

  async function onSubmit(values: Rq, formikHelpers: FormikHelpers<Rq>) {
    if (canceler.current != null) {
      canceler.current();
    }

    try {
      const result: AxiosResponse<Re> = await axios({
        method,
        url: endpoint,
        data: values,
        headers: token ? { Authorization: `Token ${token}` } : null,
        cancelToken: new axios.CancelToken(c => {
          canceler.current = c;
        })
      });

      setData(result.data);
      formikHelpers.setSubmitting(false);

      formikHelpers.setStatus({ status: "success", message: _("msg.conn.s") } as FormikStatus);
      onSuccess?.(values, result.data);
    } catch (error) {
      if (!axios.isCancel(error)) {
        formikHelpers.setSubmitting(false);

        const { response } = error as AxiosError<ErrorResponse>;
        if (response) {
          if (response.data) {
            if (response.data.non_field_errors) {
              formikHelpers.setStatus({ status: "danger", message: response.data.non_field_errors.join("\n") } as FormikStatus);
            } else {
              formikHelpers.setStatus({
                status: "danger",
                message: _("msg.conn.e.srv")
              });
            }
          } else {
            formikHelpers.setStatus({
              status: "danger",
              message: _("msg.conn.e.srv")
            });
          }
          onFail?.(values, response.data, formikHelpers);
        } else {
          formikHelpers.setStatus({ status: "danger", message: _("msg.conn.e") });
          onFail?.(values, null, formikHelpers);
        }
      }
    }

    canceler.current = null;
  }

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
  onFail: ((request: Rq, response: Re | ErrorResponse | null) => void) | null = null
): { isLoading: boolean; data: Re | null; onQuery: (values: Rq) => void; errors: Re | ErrorResponse | null } {
  const [isLoading, setLoading] = useState(false);
  const [data, setData] = useState<Re | null>(null);
  const [errors, setErrors] = useState<Re | ErrorResponse | null>(null);
  const canceler = useRef<Canceler | null>(null);
  const _ = useI18n();
  const { token } = useContext(AppContext);

  const onQuery = useCallback(
    async (values: Rq) => {
      if (canceler.current != null) {
        canceler.current();
      }
      setLoading(true);

      const isGet = method.toLowerCase() === "get";
      const cancelToken = new axios.CancelToken(c => {
        canceler.current = c;
      });

      try {
        const result: AxiosResponse<Re> = await axios({
          method,
          url: endpoint,
          params: isGet ? values : null,
          data: isGet ? null : values,
          headers: token ? { Authorization: `Token ${token}` } : null,
          cancelToken
        });
        setLoading(false);
        setData(result.data);
        onSuccess?.(values, result.data);
      } catch (error) {
        if (!axios.isCancel(error)) {
          setLoading(false);

          const { response } = error as AxiosError<ErrorResponse>;
          if (response) {
            if (response.data) {
              setErrors(response.data);
            } else {
              setErrors({
                non_field_errors: [_("msg.conn.e.srv")]
              });
            }
            onFail?.(values, response.data);
          } else {
            setErrors({ non_field_errors: [_("msg.conn.e.srv")] });
            onFail?.(values, null);
          }
        }
      }

      canceler.current = null;
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
): { isLoading: boolean; data: Re | null; errors: Re | ErrorResponse | null; onQuery: (values: Rq) => void } {
  const { isLoading, data, errors, onQuery } = useApi<Rq, Re>("GET", endpoint);
  useEffect(() => {
    onQuery(values);
  }, [endpoint, values, onQuery]);
  return { isLoading, data, errors, onQuery };
}