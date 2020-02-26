import React, { useCallback, useContext } from "react";
import { AppContext } from "../../context/AppContext";
import { Button, Card, Container } from "react-bootstrap";
import { FormattedMessage } from "react-intl";

const containerStyle = { maxWidth: 540, marginTop: 60 };

const UserPage: React.FC = () => {
  const { toggleLoginState, user } = useContext(AppContext);

  const doLogout = useCallback(() => toggleLoginState(null, null, false), [toggleLoginState]);

  return (
    <Container style={containerStyle}>
      <Card>
        <Card.Body>
          <Card.Title className="text-center">{`${user?.first_name} ${user?.last_name} (${user?.username})`}</Card.Title>
          <Card.Subtitle className="mb-2 text-muted text-center">
            <FormattedMessage id="user.scores" defaultMessage="Your scores:" /> {user?.score}
          </Card.Subtitle>
          <Button variant="primary" onClick={doLogout} block>
            <FormattedMessage id="user.logoutButton" defaultMessage="Logout" />
          </Button>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default UserPage;
