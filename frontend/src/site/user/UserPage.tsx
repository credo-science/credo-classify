import React, { useContext } from "react";
import { AppContext } from "../../context/AppContext";
import DetailsPage from "./DetailsPage";
import LoginPage from "./LoginPage";

const UserPage: React.FC = () => {
  const { token } = useContext(AppContext);

  if (token) {
    return <DetailsPage />;
  } else {
    return <LoginPage />;
  }
};

export default UserPage;
