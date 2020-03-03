import { AttributeEntity, DetectionEntity, DeviceEntity, UserEntity } from "./entities";

export interface ErrorResponse {
  non_field_errors: string[];
}

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
