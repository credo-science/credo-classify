import { FormikHelpers } from "formik/dist/types";
import { Method } from "axios";
import { useCallback } from "react";
import { useI18n } from "../utils";
import { OnFail, OnSuccess, useApiClient } from "./api";

/**
 * Message with bootstrap's color.
 */
export interface FormikStatus {
  status?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
  message?: string;
}

/** See [[FormikConfig<Values>.onSubmit]] */
export type FormikOnSubmit<Values> = (values: Values, formikHelpers: FormikHelpers<Values>) => void | Promise<any>;

/**
 * Return array[2] from [[useFormikApi]].
 *
 * [0]: {FormikOnSubmit<Rq>} function provided to onSubmit in Formik, launch [[apiClient]] with provided form values and use [[formikHelpers]] to set [[Formik]] status.
 * [1]: {Rq | null} data from server will be available when onSubmit done with success
 * @typeparam Re type of response JSON object
 * @typeparam Rq request data type passed as JSON
 */
type UseFormikApiHook<Re = any, Rq = any> = [FormikOnSubmit<Rq>, Re | null];

/**
 * Wrapper over [[apiClient]]. Support:
 * 1. Provide [[onSubmit]] method for [[Formik]].
 * 2. Use [[formikHelpers.setSubmitting]] for set submitting pending/done status
 * 3. Use [[formikHelpers.setStatus]] for set current form status, see [[FormikStatus]]
 * 4. Use [[formikHelpers.setErrors]] for set server-side validation errors for form fields.
 * @param endpoint URL for HTTP request
 * @param onSuccess run after form submit with success
 * @param method HTTP method, default 'POST'
 * @param onFail optional, run after error occurs
 * @param params optional, params after '?' in URL (experimental)
 * @return the [[UseFormikApiHook]] array
 */
export function useFormikApi<Re = any, Rq = any, Pr = any>(
  endpoint: string,
  onSuccess?: OnSuccess<Re, Rq, Pr, FormikHelpers<Rq>>,
  method: Method = "POST",
  onFail?: OnFail<Re, Rq, Pr, FormikHelpers<Rq>>,
  params?: Pr // move to this for make onQuery compatible with Formik
): UseFormikApiHook<Re, Rq> {
  //const onFailWrapped = useCallback((error: ApiError<Rq>, request?: Rq) => )
  const _ = useI18n();

  const onFormikSuccess: OnSuccess<Re, Rq, Pr, FormikHelpers<Rq>> = useCallback(
    (response, request, params, userObject) => {
      userObject!.setSubmitting(false);
      userObject!.setStatus({ status: "success", message: _("msg.conn.s") } as FormikStatus);
      onSuccess?.(response, request, params, userObject);
    },
    [_, onSuccess]
  );

  const onFormikFail: OnFail<Re, Rq, Pr, FormikHelpers<Rq>> = useCallback(
    (error, request, params, userObject) => {
      userObject!.setSubmitting(false);
      userObject!.setStatus({ status: "danger", message: error.getMessage(_) } as FormikStatus);
      userObject!.setErrors(error.fields);
      onFail?.(error, request, params, userObject);
    },
    [_, onFail]
  );

  const [onQuery, , data] = useApiClient<Re, Rq, Pr, FormikHelpers<Rq>>(endpoint, onFormikSuccess, method, onFormikFail);

  const onSubmit: FormikOnSubmit<Rq> = useCallback(
    (values, formikHelpers) => {
      onQuery(values, undefined, formikHelpers);
    },
    [onQuery]
  );

  return [onSubmit, data];
}
