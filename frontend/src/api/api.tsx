import React, { useState, useEffect, useRef, useContext, useCallback } from "react";
import { FormikErrors } from "formik/dist/types";
import axios, { AxiosError, AxiosResponse, Canceler, Method } from "axios";
import { ErrorResponse } from "./rqre";
import { AppContext, AppContextType } from "../context/AppContext";
import { I18n } from "../utils/i18n";
import { PrimitiveType } from "intl-messageformat";

/**
 * Non required options for api() async method.
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 */
export interface ApiOptions<Rq = any, Pr = any> {
  /** Authorization token */
  token?: string | null;

  /** HTTP method, default: GET */
  method?: Method;

  /** Data uploaded as JSON to server (see: [[axios]]). Ignored when `method="GET"` */
  data?: Rq;

  /** Params added to URL after "?" (see: [[axios]]) */
  params?: Pr;

  /** Used for cancellation. If canceler.current is not null then do cancel. (see: [[axios]] and [[React.createRef]]) */
  canceler?: React.MutableRefObject<Canceler | null>;

  /** Execute when `HTTP 401` error was received: is no logged or authorization token was void */
  onNoLogged?: () => void;
}

const defaultApiOptions: ApiOptions = { method: "GET" };

/**
 * Throw when API occur an error.
 */
export class ApiError<Rq = any> extends Error {
  /** Original [[axios]] error object */
  error: AxiosError<ErrorResponse>;

  /** Form fields server-side validation errors. */
  fields: FormikErrors<Rq>;

  /** Values injected to translated error message. Ignored when `i18n` is false. @see: react-intl and FormatMessage method */
  values?: Record<string, PrimitiveType>;

  /** When true then Error.message contains ID of translated message, otherwise contains other message from server */
  i18n: boolean;

  constructor(message: string, error: AxiosError<ErrorResponse>, fields: FormikErrors<Rq>, i18n: boolean = false, values?: Record<string, PrimitiveType>) {
    super(message);
    this.error = error;
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
 * Wrapper over [[axios]]. Support:
 * 1. Run canceler before if set.
 * 2. Add authorization token header if set.
 * 3. Return undefined when cancel instead throw exception.
 * 4. Wrap server error (connection error, token void, forbidden, not found, server-side form fields validation and other server error messages) to [[ApiError]]
 * @param endpoint URL to connection
 * @param options others no required options @see ApiOptions
 * @typeparam Re type of response JSON object
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 * @return [[Promies]] with [[AxiosReponse]] when success, undefined when cancel or throw [[ApiError]] when error
 */
export async function apiRequest<Re = any, Rq = any, Pr = any>(endpoint: string, options?: ApiOptions<Rq, Pr>): Promise<AxiosResponse<Re> | undefined> {
  const { method, params, data, canceler, onNoLogged, token } = { ...defaultApiOptions, ...(options || {}) };
  const isGet = method!.toLowerCase() === "get";

  canceler?.current?.();
  const _ = (a: string) => a; // for catching by extract_i18n_messages.js

  try {
    return await axios({
      method,
      url: `${credoAppRoot}/${endpoint}`,
      params: params,
      data: isGet ? null : data,
      headers: token ? { Authorization: `Token ${token}` } : null,
      cancelToken:
        canceler &&
        new axios.CancelToken(c => {
          canceler.current = c;
        })
    });
  } catch (error) {
    if (!axios.isCancel(error)) {
      const { response } = error as AxiosError<ErrorResponse>;
      if (response) {
        if (response.data) {
          // FIXME: use default messages for 401, 403 and 404 and override when provided in response
          if (response.status === 401) {
            onNoLogged?.();
          }

          if (response.data.non_field_errors instanceof Array) {
            throw new ApiError<Rq>(response.data.non_field_errors.join("\n"), error, response.data as FormikErrors<Rq>);
          } else {
            throw new ApiError<Rq>(_("msg.conn.e.cli"), error, response.data as FormikErrors<Rq>, true, { fields: Object.keys(response.data).length });
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
          throw new ApiError(err, error, {}, true);
        }
      } else {
        throw new ApiError(_("msg.conn.e"), error, {}, true);
      }
    }
  } finally {
    if (canceler) {
      canceler.current = null;
    }
  }
}

/**
 * Wrapper over [[apiRequest]]. Support:
 * 1/ Use authorization token from `context`.
 * 2/ Use `toggleLogout` from `context` to `onNoLogged`.
 * @param {string} endpoint
 * @param {AppContextType} context
 * @param {ApiOptions<Pr, Rq>} options
 * @typeparam Re type of response JSON object
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 * @return See [[apiRequest]]
 */
export async function apiClient<Re = any, Rq = any, Pr = any>(
  endpoint: string,
  context: AppContextType,
  options?: Omit<ApiOptions<Rq, Pr>, "token" | "onNoLogged">
): Promise<AxiosResponse<Re> | undefined> {
  return apiRequest<Re, Rq, Pr>(endpoint, { ...(options || {}), token: context.token, onNoLogged: context.toggleLogout });
}

/**
 * Launcher for [[apiClient]] with provided form values, query params (optional) and user object (optional).
 * @param values serialized to JSON and send as request data (ignored in 'GET')
 * @param params encoded in URL after '?'
 * @param userObject user's object provided to [[onSuccess]] or [[onFail]]
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 * @typeparam U optional user's object provided to [[onSuccess]] or [[onFail]]
 */
export type OnApiQuery<Rq = any, Pr = any, U = any> = (values: Rq, params?: Pr, userObject?: U) => void;

export type OnSuccess<Re = any, Rq = any, Pr = any, U = any> = (response: Re, request?: Rq, params?: Pr, userObject?: U) => void;
export type OnFail<Re = any, Rq = any, Pr = any, U = any> = (error: ApiError<Rq>, request?: Rq, params?: Pr, userObject?: U) => void;

/**
 * Return array[4] from [[useApiClient]].
 *
 * [0]: launcher for [[apiClient]] with provided form values, query params (optional) and user object (optional)
 * [1]: pending status, will be true when `[0]` run and false when `[0]` done
 * [2]: {Rq | null} data from server will be non null when `[0]` done with success
 * [3]: {ApiError<Rq> | null} error object, will be non null when `[0]` done with fail
 * @typeparam Re type of response JSON object
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 * @typeparam U optional user's object provided to [[onSuccess]] or [[onFail]]
 */
type UseApiClientHook<Re = any, Rq = any, Pr = any, U = any> = [OnApiQuery<Rq, Pr, U>, boolean, Re | null, ApiError<Rq> | null];

/**
 * Hook for hang state of [[apiClient]] in functional components. Supports:
 * 1. Cancel when `endpoint` or `method` was changed or component will unmount.
 * 2. Stores launcher function, pending status, response data and error.
 * @param endpoint URL for HTTP request
 * @param onSuccess callback function run after form submit with success, no run when cancel
 * @param method HTTP method, default 'POST'
 * @param onFail optional callback function, run after error occurs, no run when cancel
 * @typeparam Re type of response JSON object
 * @typeparam Rq request data type passed as JSON
 * @typeparam Pr query params type passed after '?'
 * @typeparam U optional user's object provided to [[onSuccess]] or [[onFail]]
 * @return the [[UseApiHook]] array
 */
export function useApiClient<Re = any, Rq = any, Pr = any, U = any>(
  endpoint: string,
  onSuccess?: OnSuccess<Re, Rq, Pr, U>,
  method: Method = "POST",
  onFail?: OnFail<Re, Rq, Pr, U>
): UseApiClientHook<Re, Rq, Pr> {
  const [isLoading, setLoading] = useState(false);
  const [data, setData] = useState<Re | null>(null);
  const [errors, setErrors] = useState<ApiError | null>(null);
  const canceler = useRef<Canceler | null>(null);
  const context = useContext(AppContext);

  const onQuery = useCallback(
    async (values: Rq, params?: Pr, userObject?: U) => {
      try {
        const result = await apiClient<Re, Rq, Pr>(endpoint, context, { method, canceler, data: values, params });
        if (result != null) {
          setLoading(false);
          if (result) {
            setData(result.data);
            onSuccess?.(result.data, values, params, userObject);
          }
        }
      } catch (ApiError) {
        setLoading(false);
        setErrors(ApiError);
        onFail?.(ApiError, values, params, userObject);
      }
    },
    [endpoint, context, method, onSuccess, onFail]
  );

  useEffect(() => {
    return () => {
      if (canceler.current != null) {
        canceler.current();
        canceler.current = null;
      }
    };
  }, [endpoint, method]);

  return [onQuery, isLoading, data, errors];
}

/**
 * Wrapper for [[useApiClient]] for 'GET' requests. Launch [[OnApiQuery]] after component did mount and after changed `endpoint` or `params`.
 * @param endpoint URL for HTTP request
 * @param params optional URL params
 * @typeparam Re type of response JSON object
 * @typeparam Pr query params type passed after '?'
 * @return the [[UseApiHook]] array
 */
export function useGet<Re = any, Pr = any>(endpoint: string, params?: Pr): UseApiClientHook<Re, void, Pr> {
  const [onQuery, isLoading, data, errors] = useApiClient<Re, void, Pr>(endpoint, undefined, "GET");
  useEffect(() => {
    onQuery(undefined, params);
  }, [endpoint, onQuery, params]);
  return [onQuery, isLoading, data, errors];
}
