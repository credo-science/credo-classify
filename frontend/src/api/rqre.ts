import { User } from "./entities";

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
  user: User;
}
