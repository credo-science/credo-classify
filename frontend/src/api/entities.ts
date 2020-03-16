interface Entity {
  id: number;
}

export interface UserEntity extends Entity {
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  score: number;
  is_staff: boolean;
  is_active: boolean;
  is_superuser: boolean;

  user_id: number;
  team_id: number;
  team_name: string;
}

export interface AttributeEntity extends Entity {
  name: string;
  description: string;
  active: boolean;
  kind: string;
  author: number;
}

export interface DeviceEntity extends Entity {
  device_id: string;
  device_type: string;
  device_model: string;
  system_version: string;
  user: number;
}

export interface DetectionEntity extends Entity {
  device: number;
  image: string;
  timestamp: number;
  time_received: number;
  source: string;
  provider: string;
  metadata: string;
  user: number;
  team: number;

  mime: string;
  width: number;
  height: number;
  frame_content: string;
}
