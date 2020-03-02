import React, { useContext } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import "flag-icon-css/css/flag-icon.css";

import { AppContext } from "../context/AppContext";
import { useI18n } from "../utils";

const Menu: React.FC = () => {
  const { toggleLanguage, user } = useContext(AppContext);
  const _ = useI18n();

  return (
    <Navbar collapseOnSelect expand="lg" bg="light">
      <LinkContainer to="/">
        <Navbar.Brand>CREDO Cosmic-Ray Classification</Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto" />
        <Nav>
          <LinkContainer to="/user">
            <Nav.Link>{user ? user.username : _("menu.sign_in")}</Nav.Link>
          </LinkContainer>
          <div>
            <span className="flag-icon flag-icon-gb mr-1" title="English language" onClick={() => toggleLanguage("en")} />
            <span className="flag-icon flag-icon-pl" title="Język polski" onClick={() => toggleLanguage("pl")} />
          </div>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Menu;
