export interface UserEntity {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  score: number;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean;
}
