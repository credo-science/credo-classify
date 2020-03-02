import React, { useMemo } from "react";
import { FormikStatus } from "../api/apiHooks";
import { Alert, Button, Form } from "react-bootstrap";
import { useFormikContext } from "formik";
import { uniqueId } from "lodash";
import { useI18n } from "../utils";

export const FormStatusAlert: React.FC<{ status: FormikStatus; isSubmitting: boolean }> = ({ status, isSubmitting }) => {
  const _ = useI18n();

  if (isSubmitting) {
    return <Alert variant="info">{_("msg.conn.p")}</Alert>;
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
  label?: string;
  placeholder?: string;
  type?: string;
  name: string;
  head?: React.ReactNode;
}

export const VField: React.FC<VFieldProps> = ({ controlId, label, placeholder, type, name, head }) => {
  const { getFieldProps, getFieldMeta } = useFormikContext();
  const meta = getFieldMeta(name);
  const cid = useHtmlId(controlId);

  return (
    <Form.Group controlId={cid}>
      {head}
      <Form.Label>{label}</Form.Label>
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
  label?: string;
  name: string;
}

export const VCheck: React.FC<VCheckProps> = ({ controlId, label, name }) => {
  const { getFieldProps } = useFormikContext();
  const cid = useHtmlId(controlId);

  return (
    <Form.Group controlId={cid}>
      <Form.Check type="checkbox" label={label} name={name} {...getFieldProps(name)} />
    </Form.Group>
  );
};

interface VSubmitButtonProps {
  label?: string;
}

export const VSubmitButton: React.FC<VSubmitButtonProps> = ({ label }) => {
  const { isValid, isSubmitting } = useFormikContext();

  return (
    <Form.Group>
      <Button variant="primary" type="submit" block disabled={!isValid || isSubmitting}>
        {label}
      </Button>
    </Form.Group>
  );
};
