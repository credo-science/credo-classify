import React from "react";
import { User } from "../api/entities";

export interface AppContextType {
  language: string;
  token: string | null;
  user: User | null;
  toggleLanguage: (language: string) => void;
  toggleLoginState: (token: string | null, user: User | null) => void;
  updateUser: (user: User) => void;
}

function getDefaultContext(): AppContextType {
  const user = localStorage.getItem("user");
  return {
    language: localStorage.getItem("language") || navigator.language,
    token: localStorage.getItem("token"),
    user: user ? JSON.parse(user) : null,
    toggleLanguage: () => {},
    toggleLoginState: () => {},
    updateUser: () => {}
  };
}

export const defaultAppContext = getDefaultContext();

export const AppContext = React.createContext<AppContextType>(defaultAppContext);
