import React from "react";
import { FormikStatus } from "../api/apiHooks";
import { Alert } from "react-bootstrap";
import { FormattedMessage } from "react-intl";

export const FormStatusAlert: React.FC<{ status: FormikStatus; isSubmitting: boolean }> = ({ status, isSubmitting }) => {
  if (isSubmitting) {
    return (
      <Alert variant="info">
        <FormattedMessage id="message.pending" defaultMessage="Your values is submitting to server, please wait..." />
      </Alert>
    );
  } else if (status?.status) {
    return <Alert variant={status.status}>{status.message}</Alert>;
  }
  return null;
};
