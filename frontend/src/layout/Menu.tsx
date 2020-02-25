import React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { FormattedMessage } from "react-intl";

const Menu: React.FC = () => {
  return (
    <Navbar collapseOnSelect expand="lg" bg="light">
      <LinkContainer to="/">
        <Navbar.Brand>CREDO Cosmic-Ray Classification</Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto" />
        <Nav>
          <LinkContainer to="/login">
            <Nav.Link>
              <FormattedMessage id="menu.sign_in" defaultMessage="Sign in" />
            </Nav.Link>
          </LinkContainer>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Menu;
