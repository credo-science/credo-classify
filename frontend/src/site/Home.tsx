import React from "react";
import { Jumbotron } from "react-bootstrap";
import { FormattedMessage } from "react-intl";

const Home: React.FC = () => {
  return (
    <Jumbotron>
      <h1 className="display-4">
        <FormattedMessage id="home.title" defaultMessage="Welcome!" />
      </h1>
      <p className="lead">
        <FormattedMessage id="home.lead" defaultMessage="Classify cosmic-ray hits images and earn points :)" />
      </p>
      <hr className="my-4" />
      <p>
        <FormattedMessage id="home.description" defaultMessage="Help scientists organize a huge set of cosmic ray image data from CCD/CMOS cameras." />
      </p>
      <a className="btn btn-primary btn-lg" href="https://credo.science/" role="button" target="_blank" rel="noopener noreferrer">
        <FormattedMessage id="home.button" defaultMessage="CREDO Website" />
      </a>
    </Jumbotron>
  );
};

export default Home;
