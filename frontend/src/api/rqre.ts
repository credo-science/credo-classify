import { AttributeEntity, DetectionEntity, DeviceEntity, UserEntity } from "./entities";
import { FormikErrors } from "formik/dist/types";

interface NonFieldErrors {
  non_field_errors: string[];
}

export type ErrorResponse<Rq = any> = NonFieldErrors | FormikErrors<Rq>;

export interface LoginRequest {
  username: string;
  password: string;
  remember: boolean;
}

export interface LoginResponse {
  token: string;
  user: UserEntity;
}

export interface ForgotRequest {
  username: string;
  email: string;
}

interface RandomDetection extends Omit<DetectionEntity, "device"> {
  device: DeviceEntity;
  attributes: AttributeEntity[];
}

export interface GetRandomDetectionResponse {
  detections: RandomDetection[];
}
