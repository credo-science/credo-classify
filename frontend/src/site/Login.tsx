import React from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const Login: React.FC = () => {
  return (
    <Container style={containerStyle}>
      <Card>
        <Card.Body>
          <Link to="/register" className="float-right btn btn-outline-primary">
            Sign up
          </Link>
          <Card.Title className="mb-4 mt-1">Sign in</Card.Title>
          <Form>
            <Form.Group>
              <Form.Label>Your email</Form.Label>
              <Form.Control placeholder="Login" type="text" />
            </Form.Group>
            <Form.Group>
              <Link to="/forgot" className="float-right">
                Forgot?
              </Link>
              <Form.Label>Your password</Form.Label>
              <Form.Control placeholder="******" type="password" />
            </Form.Group>
            <Form.Group>
              <Form.Check type="checkbox" label="Save password" />
            </Form.Group>
            <Form.Group>
              <Button variant="primary" type="submit" block>
                Login
              </Button>
            </Form.Group>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Login;
