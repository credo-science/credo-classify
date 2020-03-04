import React, { useMemo } from "react";
import { Container, Card, Form } from "react-bootstrap";
import * as yup from "yup";
import { Formik } from "formik";
import { useFormikApi } from "../../api/api";
import { ErrorResponse, ForgotRequest } from "../../api/rqre";
import { FormStatusAlert, VField, VSubmitButton } from "../../layout/forms";
import { useI18n } from "../../utils";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: ForgotRequest = { username: "", email: "" };

const RegisterPage: React.FC = () => {
  const _ = useI18n();

  const inv = _("msg.inv");
  const req = _("msg.inv.req");
  const pass = _("user.password.inv");
  const confPass = _("user.confirm_password.inv");

  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(req),
        email: yup
          .string()
          .email(inv)
          .required(req),
        first_name: yup.string(),
        last_name: yup.string(),
        password: yup
          .string()
          .required(req)
          .matches(/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/, pass),
        passwordConfirmation: yup
          .string()
          .oneOf([yup.ref("password")], confPass)
          .required(req)
      }),
    [inv, req, pass, confPass]
  );
  const { onSubmit } = useFormikApi<ForgotRequest, ErrorResponse>("POST", "/api/register/");

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, status, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Card.Title className="mb-4 mt-1">{_("user_register.title")}</Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
              {status?.status !== "success" && (
                <Form noValidate onSubmit={handleSubmit}>
                  <VField label={_("user.login")} placeholder="login" type="text" name="username" />

                  <VField label={_("user.email")} placeholder="e-mail" type="email" name="email" />

                  <VField label={_("user.firstname")} type="text" name="first_name" />
                  <VField label={_("user.lastname")} type="text" name="last_name" />

                  <VField label={_("user.password")} placeholder="******" type="password" name="password" />
                  <VField label={_("user.confirm_password")} type="password" name="passwordConfirmation" />

                  <VSubmitButton label={_("user_register.submit")} />
                </Form>
              )}
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default RegisterPage;
