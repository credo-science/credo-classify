import { useState, useEffect, useRef } from "react";
import { FormikHelpers } from "formik/dist/types";
import axios, { AxiosError, AxiosResponse, Canceler, Method } from "axios";
import { ErrorResponse } from "./rqre";
import { useIntl } from "react-intl";

export interface FormikStatus {
  status?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
  message?: string;
}

export function useFormikApi<Rq, Re>(
  method: Method,
  endpoint: string,
  onSuccess: ((request: Rq, response: Re) => void) | null = null,
  onFail: ((request: Rq, response: Re | ErrorResponse | null, formikHelpers: FormikHelpers<Rq>) => void) | null = null
): { isLoading: boolean; data: Re | null; onSubmit: (values: Rq, formikHelpers: FormikHelpers<Rq>) => void } {
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState<Re | null>(null);
  const canceler = useRef<Canceler | null>(null);
  const { formatMessage: f } = useIntl();

  async function onSubmit(values: Rq, formikHelpers: FormikHelpers<Rq>) {
    setIsLoading(true);
    if (canceler.current != null) {
      canceler.current();
    }

    try {
      const result: AxiosResponse<Re> = await axios({
        method,
        url: endpoint,
        data: values,
        cancelToken: new axios.CancelToken(c => {
          canceler.current = c;
        })
      });

      setIsLoading(false);
      setData(result.data);
      formikHelpers.setSubmitting(false);

      formikHelpers.setStatus({ status: "success", message: f({ id: "message.success", defaultMessage: "Success" }) } as FormikStatus);
      onSuccess?.(values, result.data);
    } catch (error) {
      setIsLoading(false);
      formikHelpers.setSubmitting(false);

      const { response } = error as AxiosError<ErrorResponse>;
      if (response) {
        if (response.data) {
          if (response.data.non_field_errors) {
            formikHelpers.setStatus({ status: "danger", message: response.data.non_field_errors.join("\n") } as FormikStatus);
          } else {
            formikHelpers.setStatus({
              status: "danger",
              message: f({ id: "message.error.server_error", defaultMessage: "Server error, please contact with admin" })
            });
          }
        } else {
          formikHelpers.setStatus({
            status: "danger",
            message: f({ id: "message.error.server_error", defaultMessage: "Server error, please contact with admin" })
          });
        }
        onFail?.(values, response.data, formikHelpers);
      } else {
        formikHelpers.setStatus({ status: "danger", message: f({ id: "message.error.no_connection", defaultMessage: "No connection with server" }) });
        onFail?.(values, null, formikHelpers);
      }
    }

    canceler.current = null;
  }

  useEffect(() => {
    return () => {
      if (canceler.current != null) {
        canceler.current();
      }
    };
  }, [endpoint, method]);

  return { isLoading, data, onSubmit };
}
