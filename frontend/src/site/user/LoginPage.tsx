import React, { useContext, useMemo } from "react";
import { Container, Card, Form } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";
import { FormattedMessage, useIntl } from "react-intl";
import { useFormikApi } from "../../api/apiHooks";
import { AppContext } from "../../context/AppContext";
import { LoginRequest, LoginResponse } from "../../api/rqre";
import { FormStatusAlert, VCheck, VField, VSubmitButton } from "../../layout/forms";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: LoginRequest = { username: "", password: "", remember: false };

const LoginPage: React.FC = () => {
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
      {({ handleSubmit, status, isSubmitting }) => (
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
                <VField labelId="login.loginFieldLabel" labelDm="Your login" placeholder="login" type="text" name="username" />

                <VField
                  head={
                    <Link to="/forgot" className="float-right">
                      <FormattedMessage id="login.forgotLink" defaultMessage="Forgot?" />
                    </Link>
                  }
                  labelId="login.passwordFieldLabel"
                  labelDm="Your password"
                  placeholder="******"
                  type="password"
                  name="password"
                />

                <VCheck name="remember" labelId="login.rememberCheckbox" labelDm="Save password" />

                <VSubmitButton labelId="login.submitButton" labelDm="Login" />
              </Form>
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default LoginPage;
