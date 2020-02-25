import React from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const schema = yup.object({
  username: yup.string().required(),
  password: yup.string().required()
});

const initialValues = { username: "", password: "" };

const Login: React.FC = () => {
  return (
    <Formik validationSchema={schema} onSubmit={console.log} initialValues={initialValues}>
      {({ handleSubmit, handleChange, handleBlur, values, touched, isValid, errors }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Link to="/register" className="float-right btn btn-outline-primary">
                Sign up
              </Link>
              <Card.Title className="mb-4 mt-1">Sign in</Card.Title>
              <Form noValidate onSubmit={handleSubmit}>
                <Form.Group>
                  <Form.Label>Your login</Form.Label>
                  <Form.Control placeholder="Login" type="text" name="username" value={values.username} />
                  <Form.Control.Feedback type="invalid">{errors.username}</Form.Control.Feedback>
                </Form.Group>
                <Form.Group>
                  <Link to="/forgot" className="float-right">
                    Forgot?
                  </Link>
                  <Form.Label>Your password</Form.Label>
                  <Form.Control placeholder="******" type="password" name="password" value={values.password} />
                  <Form.Control.Feedback type="invalid">{errors.password}</Form.Control.Feedback>
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
      )}
    </Formik>
  );
};

export default Login;
