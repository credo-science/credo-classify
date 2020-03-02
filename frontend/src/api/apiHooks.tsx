import { useState, useEffect, useRef, useContext } from "react";
import { FormikHelpers } from "formik/dist/types";
import axios, { AxiosError, AxiosResponse, Canceler, Method } from "axios";
import { ErrorResponse } from "./rqre";
import { AppContext } from "../context/AppContext";
import { useI18n } from "../utils";

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

  async function onQuery(values: Rq) {
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
        params: isGet ? data : null,
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
  }

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

export function useGet<Rq, Re>(endpoint: string, values?: any): { isLoading: boolean; data: Re | null; errors: Re | ErrorResponse | null } {
  const { isLoading, data, errors, onQuery } = useApi<Rq, Re>("GET", endpoint);
  useEffect(() => {
    onQuery(values);
  }, [endpoint, values, onQuery]);
  return { isLoading, data, errors };
}
