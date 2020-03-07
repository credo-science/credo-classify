import React, { useContext, useMemo } from "react";
import { Container, Card, Form } from "react-bootstrap";
import { Link } from "react-router-dom";
import * as yup from "yup";
import { Formik } from "formik";
import { AppContext } from "../../context/AppContext";
import { LoginRequest, LoginResponse } from "../../api/rqre";
import { FormStatusAlert, VCheck, VField, VSubmitButton } from "../../layout/forms";
import { useI18n } from "../../utils";
import { useFormikApi } from "../../api/formik";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: LoginRequest = { username: "", password: "", remember: false };

const LoginPage: React.FC = () => {
  const { toggleLoginState } = useContext(AppContext);
  const _ = useI18n();

  const req = _("msg.inv.req");
  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(req),
        password: yup.string().required(req),
        remember: yup.boolean()
      }),
    [req]
  );
  const [onSubmit] = useFormikApi<LoginResponse, LoginRequest>("/api-token-auth/", (re, rq) => toggleLoginState(re.token, re.user, !!rq?.remember));

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, status, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Link to="/register" className="float-right btn btn-outline-primary">
                {_("user_login.register")}
              </Link>
              <Card.Title className="mb-4 mt-1">{_("user_login.title")}</Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
              <Form noValidate onSubmit={handleSubmit}>
                <VField label={_("user.login")} placeholder="login" type="text" name="username" />

                <VField
                  head={
                    <Link to="/forgot" className="float-right">
                      {_("user_login.forgot")}
                    </Link>
                  }
                  label={_("user.password")}
                  placeholder="******"
                  type="password"
                  name="password"
                />

                <VCheck name="remember" label={_("user_login.remember")} />

                <VSubmitButton label={_("user_login.submit")} />
              </Form>
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default LoginPage;
