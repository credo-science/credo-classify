import React, { useMemo } from "react";
import { Container, Card, Form } from "react-bootstrap";
import * as yup from "yup";
import { Formik } from "formik";
import { useFormikApi } from "../../api/apiHooks";
import { ErrorResponse, ForgotRequest } from "../../api/rqre";
import { FormStatusAlert, VField, VSubmitButton } from "../../layout/forms";
import { useI18n } from "../../utils";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const initialValues: ForgotRequest = { username: "", email: "" };

const ForgotPage: React.FC = () => {
  const _ = useI18n();

  const inv = _("msg.inv");
  const req = _("msg.inv.req");
  const schema = useMemo(
    () =>
      yup.object({
        username: yup.string().required(req),
        email: yup
          .string()
          .email(inv)
          .required(req)
      }),
    [inv, req]
  );
  const { onSubmit } = useFormikApi<ForgotRequest, ErrorResponse>("POST", "/api/forgot/");

  return (
    <Formik validationSchema={schema} onSubmit={onSubmit} initialValues={initialValues}>
      {({ handleSubmit, status, isSubmitting }) => (
        <Container style={containerStyle}>
          <Card>
            <Card.Body>
              <Card.Title className="mb-4 mt-1">{_("user_forgot.title")}</Card.Title>
              <FormStatusAlert status={status} isSubmitting={isSubmitting} />
              {status?.status !== "success" && (
                <Form noValidate onSubmit={handleSubmit}>
                  <VField label={_("user.login")} placeholder="login" type="text" name="username" />

                  <VField label={_("user.email")} placeholder="email" type="email" name="email" />

                  <VSubmitButton label={_("user_forgot.submit")} />
                </Form>
              )}
            </Card.Body>
          </Card>
        </Container>
      )}
    </Formik>
  );
};

export default ForgotPage;
