import React, { useMemo } from "react";
import { Container, Card, Form } from "react-bootstrap";
import * as yup from "yup";
import { Formik } from "formik";
import { FormattedMessage, useIntl } from "react-intl";
import { useFormikApi } from "../../api/apiHooks";
import { ErrorResponse, ForgotRequest } from "../../api/rqre";
import { FormStatusAlert, VField, VSubmitButton } from "../../layout/forms";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: ForgotRequest = { username: "", email: "" };

const Forgot: React.FC = () => {
  const { formatMessage: f } = useIntl();
  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(f({ id: "login.loginFieldValidation", defaultMessage: "Login is required" })),
        email: yup
          .string()
          .email()
          .required(f({ id: "login.passwordFieldValidation", defaultMessage: "Password is required" }))
      }),
    [f]
  );
  const { onSubmit } = useFormikApi<ForgotRequest, ErrorResponse>("POST", "/api/forgot/");

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, status, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Card.Title className="mb-4 mt-1">
                <FormattedMessage id="forgot.title" defaultMessage="Reset password" />
              </Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
              {status?.status !== "success" && (
                <Form noValidate onSubmit={handleSubmit}>
                  <VField labelId="login.loginFieldLabel" labelDm="Your login" placeholder="login" type="text" name="username" />

                  <VField labelId="forgot.emailFieldLabel" labelDm="Your e-mail" placeholder="email" type="email" name="email" />

                  <VSubmitButton labelId="forgot.submitButton" labelDm="Send e-mail with reset password URL" />
                </Form>
              )}
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default Forgot;
