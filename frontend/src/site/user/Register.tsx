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

const Register: React.FC = () => {
  const { formatMessage: f } = useIntl();
  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(f({ id: "login.loginFieldValidation", defaultMessage: "Login is required" })),
        email: yup
          .string()
          .email()
          .required(f({ id: "forgot.emailFieldValidation", defaultMessage: "E-mail is required" })),
        first_name: yup.string(),
        last_name: yup.string(),
        password: yup
          .string()
          .required(f({ id: "login.passwordFieldValidation", defaultMessage: "Password is required" }))
          .matches(
            /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/,
            f({
              id: "register.passwordComplexityValidation",
              defaultMessage: "Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and one special case Character"
            })
          ),
        passwordConfirmation: yup
          .string()
          .oneOf([yup.ref("password")], f({ id: "register.passwordConfirmationFieldValidation", defaultMessage: "Passwords must match" }))
          .required(f({ id: "register.passwordConfirmationFieldValidation", defaultMessage: "Passwords must match" }))
      }),
    [f]
  );
  const { onSubmit } = useFormikApi<ForgotRequest, ErrorResponse>("POST", "/api/register/");

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, status, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Card.Title className="mb-4 mt-1">
                <FormattedMessage id="register.title" defaultMessage="Register" />
              </Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
              {status?.status !== "success" && (
                <Form noValidate onSubmit={handleSubmit}>
                  <VField labelId="login.loginFieldLabel" labelDm="Your login" placeholder="login" type="text" name="username" />

                  <VField labelId="forgot.emailFieldLabel" labelDm="Your e-mail" placeholder="email" type="email" name="email" />

                  <VField labelId="register.firstNameFieldLabel" labelDm="Your first name" type="text" name="first_name" />
                  <VField labelId="register.lastNameFieldLabel" labelDm="Your last name" type="text" name="last_name" />

                  <VField labelId="login.passwordFieldLabel" labelDm="Your password" placeholder="******" type="password" name="password" />
                  <VField labelId="register.passwordConfirmationFieldLabel" labelDm="Confirm password" type="password" name="passwordConfirmation" />

                  <VSubmitButton labelId="register.submitButton" labelDm="Register" />
                </Form>
              )}
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default Register;
