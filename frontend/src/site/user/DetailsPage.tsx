import React, { useCallback, useContext } from "react";
import { AppContext } from "../../context/AppContext";
import { Button, Card, Container } from "react-bootstrap";
import { useApiClient } from "../../api/api";
import { useI18n } from "../../utils";
import { Link } from "react-router-dom";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const DetailsPage: React.FC = () => {
  const { toggleLoginState, user } = useContext(AppContext);
  const _ = useI18n();
  const toggleLogout = useCallback(() => {
    toggleLoginState(null, null, false);
  }, [toggleLoginState]);
  const [onQuery, isLoading] = useApiClient("/api/logout/", toggleLogout);
  const doLogout = useCallback(() => {
    onQuery({});
  }, [onQuery]);

  return (
    <Container style={containerStyle}>
      <Card>
        <Card.Body>
          <Card.Title className="text-center">{user?.username}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted text-center">{`${_("user.scores")} ${user?.score}`}</Card.Subtitle>
          <Link to="/classify" className="btn btn-block btn-success">
            {_("user.classify")}
          </Link>
          <Button variant="primary" onClick={doLogout} block disabled={isLoading}>
            {_("user.logout")}
          </Button>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default DetailsPage;

// <Card.Title className="text-center">{`${user?.first_name} ${user?.last_name} (${user?.username})`}</Card.Title>
