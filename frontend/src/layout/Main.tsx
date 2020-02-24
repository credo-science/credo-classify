import React from "react";
import Menu from "./Menu";
import { HashRouter as Router, Switch, Route } from "react-router-dom";

import Home from "../site/Home";
import Login from "../site/Login";

const Main: React.FC = () => {
  return (
    <Router>
      <Menu />
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/" exact component={Home} />
      </Switch>
    </Router>
  );
};

export default Main;
