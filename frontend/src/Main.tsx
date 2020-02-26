import React, { PropsWithChildren } from "react";
import Menu from "./layout/Menu";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { IntlProvider } from "react-intl";

import Home from "./site/Home";
import Login from "./site/Login";
import { AppContextType, AppContext, defaultAppContext } from "./context/AppContext";
import { User } from "./api/entities";

import en from "./translations/locale_en";
import pl from "./translations/locale_pl";
import { MessageFormatElement } from "intl-messageformat-parser";

type Messages = Record<string, string> | Record<string, MessageFormatElement[]>;
const messages: { [lang: string]: Messages } = { en, pl };

export class Main extends React.PureComponent<PropsWithChildren<{}>, AppContextType> {
  toggleLanguage = (language: string) => {
    localStorage.setItem("language", language);
    this.setState(() => ({ language: language }));
  };

  toggleLoginState = (token: string | null, user: User | null, remember: boolean) => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    if (token !== null && remember) {
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
    }
    this.setState(() => ({ token: token, user: user }));
  };

  updateUser = (user: User) => {
    if (localStorage.getItem("token")) {
      localStorage.setItem("user", JSON.stringify(user));
    }
    this.setState(() => ({ user: user }));
  };

  constructor(props: {}) {
    super(props);
    this.state = {
      ...defaultAppContext,
      toggleLanguage: this.toggleLanguage,
      toggleLoginState: this.toggleLoginState,
      updateUser: this.updateUser
    };
  }

  render() {
    const { language } = this.state;
    const subLang = language.substr(0, 2);
    const msg = messages[language] || messages[subLang] || en;

    return (
      <AppContext.Provider value={this.state}>
        <IntlProvider locale={language} messages={msg}>
          <Router>
            <Menu />
            <Switch>
              <Route path="/login" component={Login} />
              <Route path="/" exact component={Home} />
            </Switch>
          </Router>
        </IntlProvider>
      </AppContext.Provider>
    );
  }
}

export default Main;
