import React, { useContext, useMemo } from "react";
import { Container, Card, Form, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";
import { FormattedMessage, useIntl } from "react-intl";
import { useFormikApi } from "../api/apiHooks";
import { AppContext } from "../context/AppContext";
import { LoginRequest, LoginResponse } from "../api/rqre";
import { FormStatusAlert } from "../layout/forms";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: LoginRequest = { username: "", password: "", remember: false };

const Login: React.FC = () => {
  const { toggleLoginState } = useContext(AppContext);
  const { formatMessage: f } = useIntl();
  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(f({ id: "login.loginFieldValidation", defaultMessage: "Login is required" })),
        password: yup.string().required(f({ id: "login.passwordFieldValidation", defaultMessage: "Password is required" })),
        remember: yup.boolean()
      }),
    [f]
  );
  const { onSubmit } = useFormikApi<LoginRequest, LoginResponse>("POST", "/api-token-auth/", (re, rq) => toggleLoginState(rq.token, rq.user, re.remember));

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, touched, errors, getFieldProps, status, isValid, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Link to="/register" className="float-right btn btn-outline-primary">
                <FormattedMessage id="login.registerButton" defaultMessage="Sign up" />
              </Link>
              <Card.Title className="mb-4 mt-1">
                <FormattedMessage id="login.title" defaultMessage="Sign in" />
              </Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
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
                  <Button variant="primary" type="submit" block disabled={!isValid || isSubmitting}>
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
