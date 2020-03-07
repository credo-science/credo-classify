import React from "react";
import { UserEntity } from "../api/entities";

export interface AppContextType {
  language: string;
  token: string | null;
  user: UserEntity | null;
  toggleLanguage: (language: string) => void;
  toggleLoginState: (token: string | null, user: UserEntity | null, remember: boolean) => void;
  toggleLogout: () => void;
  updateUser: (user: UserEntity) => void;
}

function getDefaultContext(): AppContextType {
  const user = localStorage.getItem("user");
  return {
    language: localStorage.getItem("language") || navigator.language,
    token: localStorage.getItem("token"),
    user: user ? JSON.parse(user) : null,
    toggleLanguage: () => {},
    toggleLoginState: () => {},
    updateUser: () => {},
    toggleLogout: () => {}
  };
}

export const defaultAppContext = getDefaultContext();

export const AppContext = React.createContext<AppContextType>(defaultAppContext);
