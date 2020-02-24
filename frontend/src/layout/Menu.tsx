import React from "react";
import { Nav, Navbar } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

const Menu: React.FC = () => {
  return (
    <Navbar collapseOnSelect expand="lg" bg="light">
      <LinkContainer to="/">
        <Navbar.Brand>CREDO Cosmic-Ray Classification</Navbar.Brand>
      </LinkContainer>
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="mr-auto"></Nav>
        <Nav>
          <LinkContainer to="/login">
            <Nav.Link>Sign in</Nav.Link>
          </LinkContainer>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Menu;
