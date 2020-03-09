import React, { useContext, useState } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import "flag-icon-css/css/flag-icon.css";

import { AppContext } from "../context/AppContext";
import { useI18n } from "../utils";

const Menu: React.FC = () => {
  const { toggleLanguage, user } = useContext(AppContext);
  const _ = useI18n();
  const [expanded, setExpanded] = useState(false);

  return (
    <Navbar collapseOnSelect expand="sm" bg="light" onToggle={setExpanded} fixed="top">
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <LinkContainer to="/">
        <Navbar.Brand>CREDO Classify</Navbar.Brand>
      </LinkContainer>
      <div className={`navbar-collapse bg-light offcanvas-collapse${expanded ? " open" : ""}`}>
        <Nav className="mr-auto">
          {user && (
            <>
              <LinkContainer to="/classify">
                <Nav.Link>{_("menu.classify")}</Nav.Link>
              </LinkContainer>
            </>
          )}
        </Nav>
        <Nav>
          <LinkContainer to="/user">
            <Nav.Link>{user ? user.username : _("menu.sign_in")}</Nav.Link>
          </LinkContainer>
          <div>
            <span className="flag-icon flag-icon-gb mr-1" title="English language" onClick={() => toggleLanguage("en")} />
            <span className="flag-icon flag-icon-pl" title="Język polski" onClick={() => toggleLanguage("pl")} />
          </div>
        </Nav>
      </div>
    </Navbar>
  );
};

export default Menu;
