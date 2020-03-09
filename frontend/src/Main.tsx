import React, { PropsWithChildren } from "react";
import Menu from "./layout/Menu";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { IntlProvider } from "react-intl";

import { AppContextType, AppContext, defaultAppContext } from "./context/AppContext";
import { UserEntity } from "./api/entities";

import { ForgotPage, RegisterPage, UserPage } from "./site/user";
import { ClassifyPage } from "./site/classify";
import { HomePage } from "./site";
import { Messages, getI18nMessages } from "./utils/i18n";

interface MainState extends AppContextType {
  messages: Messages;
}

export class Main extends React.PureComponent<PropsWithChildren<{}>, MainState> {
  toggleLanguage = (language: string) => {
    localStorage.setItem("language", language);
    this.setState(() => ({ language: language, messages: getI18nMessages(language) }));
  };

  toggleLoginState = (token: string | null, user: UserEntity | null, remember: boolean) => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    if (token !== null && remember) {
      localStorage.setItem("token", token);
      localStorage.setItem("user", JSON.stringify(user));
    }
    this.setState(() => ({ token: token, user: user }));
  };

  updateUser = (user: UserEntity) => {
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
      toggleLogout: () => this.toggleLoginState(null, null, false),
      updateUser: this.updateUser,
      messages: getI18nMessages(defaultAppContext.language)
    };
  }

  render() {
    const { language, messages, token } = this.state;

    const classify = <Route key="classify" path="/classify" component={ClassifyPage} />;

    return (
      <AppContext.Provider value={this.state}>
        <IntlProvider locale={language} messages={messages}>
          <Router>
            <Menu />
            <Switch>
              <Route path="/user" component={UserPage} />
              <Route path="/forgot" component={ForgotPage} />
              <Route path="/register" component={RegisterPage} />
              {token ? [classify] : null}
              <Route path="/" component={HomePage} />
            </Switch>
          </Router>
        </IntlProvider>
      </AppContext.Provider>
    );
  }
}

export default Main;
