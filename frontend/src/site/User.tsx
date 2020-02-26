import React, { useContext } from "react";
import { AppContext } from "../context/AppContext";
import UserPage from "./user/UserPage";
import LoginPage from "./user/LoginPage";

const User: React.FC = () => {
  const { token } = useContext(AppContext);

  if (token) {
    return <UserPage />;
  } else {
    return <LoginPage />;
  }
};

export default User;
