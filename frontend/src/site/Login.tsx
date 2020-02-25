import React from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";
import { FormattedMessage } from "react-intl";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const schema = yup.object({
  username: yup.string().required(),
  password: yup.string().required(),
  remember: yup.boolean()
});

const initialValues = { username: "", password: "", remember: false };

const Login: React.FC = () => {
  return (
    <Formik validationSchema={schema} onSubmit={console.log} initialValues={initialValues}>
      {({ handleSubmit, handleChange, handleBlur, values, touched, isValid, errors, getFieldProps }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Link to="/register" className="float-right btn btn-outline-primary">
                <FormattedMessage id="login.registerButton" defaultMessage="Sign up" />
              </Link>
              <Card.Title className="mb-4 mt-1">
                <FormattedMessage id="login.title" defaultMessage="Sign in" />
              </Card.Title>
              <Form noValidate onSubmit={handleSubmit}>
                <Form.Group controlId="formLogin">
                  <Form.Label>
                    <FormattedMessage id="login.loginFieldLabel" defaultMessage="Your login" />
                  </Form.Label>
                  <Form.Control
                    placeholder="Login"
                    type="text"
                    name="username"
                    isValid={touched.username && !errors.username}
                    isInvalid={!!errors.username}
                    {...getFieldProps("username")}
                  />
                  <Form.Control.Feedback type="invalid">{errors.username}</Form.Control.Feedback>
                </Form.Group>
                <Form.Group controlId="formPassword">
                  <Link to="/forgot" className="float-right">
                    <FormattedMessage id="login.forgotLink" defaultMessage="Forgot?" />
                  </Link>
                  <Form.Label>
                    <FormattedMessage id="login.passwordFieldLabel" defaultMessage="Your password" />
                  </Form.Label>
                  <Form.Control
                    placeholder="******"
                    type="password"
                    name="password"
                    isValid={touched.password && !errors.password}
                    isInvalid={!!errors.password}
                    {...getFieldProps("password")}
                  />
                  <Form.Control.Feedback type="invalid">{errors.password}</Form.Control.Feedback>
                </Form.Group>
                <Form.Group controlId="formRemember">
                  <Form.Check
                    type="checkbox"
                    label={<FormattedMessage id="login.rememberCheckbox" defaultMessage="Save password" />}
                    name="remember"
                    {...getFieldProps("remember")}
                  />
                </Form.Group>
                <Form.Group>
                  <Button variant="primary" type="submit" block>
                    <FormattedMessage id="login.submitButton" defaultMessage="Login" />
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
