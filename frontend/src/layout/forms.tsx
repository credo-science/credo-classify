import React, { useMemo } from "react";
import { FormikStatus } from "../api/apiHooks";
import { Alert, Button, Form } from "react-bootstrap";
import { FormattedMessage } from "react-intl";
import { useFormikContext } from "formik";
import { uniqueId } from "lodash";

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

function useHtmlId(controlId: string | undefined = undefined) {
  return useMemo(() => controlId || `field_${uniqueId()}`, [controlId]);
}

interface VFieldProps {
  controlId?: string;
  labelId?: string;
  labelDm?: string;
  placeholder?: string;
  type?: string;
  name: string;
  head?: React.ReactNode;
}

export const VField: React.FC<VFieldProps> = ({ controlId, labelId, labelDm, placeholder, type, name }) => {
  const { getFieldProps, getFieldMeta } = useFormikContext();
  const meta = getFieldMeta(name);
  const cid = useHtmlId(controlId);

  return (
    <Form.Group controlId={cid}>
      <Form.Label>
        <FormattedMessage id={labelId} defaultMessage={labelDm} />
      </Form.Label>
      <Form.Control
        placeholder={placeholder}
        type={type || "text"}
        name={name}
        isValid={meta.touched && !meta.error}
        isInvalid={!!meta.error}
        {...getFieldProps(name)}
      />
      <Form.Control.Feedback type="invalid">{meta.error}</Form.Control.Feedback>
    </Form.Group>
  );
};

interface VCheckProps {
  controlId?: string;
  labelId?: string;
  labelDm?: string;
  name: string;
}

export const VCheck: React.FC<VFieldProps> = ({ controlId, labelId, labelDm, name }) => {
  const { getFieldProps } = useFormikContext();
  const cid = useHtmlId(controlId);

  return (
    <Form.Group controlId={cid}>
      <Form.Check type="checkbox" label={<FormattedMessage id={labelId} defaultMessage={labelDm} />} name={name} {...getFieldProps(name)} />
    </Form.Group>
  );
};

interface VSubmitButtonProps {
  labelId?: string;
  labelDm?: string;
}

export const VSubmitButton: React.FC<VSubmitButtonProps> = ({ labelId, labelDm }) => {
  const { isValid, isSubmitting } = useFormikContext();

  return (
    <Form.Group>
      <Button variant="primary" type="submit" block disabled={!isValid || isSubmitting}>
        <FormattedMessage id={labelId} defaultMessage={labelDm} />
      </Button>
    </Form.Group>
  );
};
