import React from "react";
import { Jumbotron } from "react-bootstrap";
import { useI18n } from "../utils";

const HomePage: React.FC = () => {
  const _ = useI18n();

  return (
    <Jumbotron>
      <h1 className="display-4">{_("home.title")}</h1>
      <p className="lead">{_("home.lead")}</p>
      <hr className="my-4" />
      <p>{_("home.description")}</p>
      <a className="btn btn-primary btn-lg" href="https://credo.science/" role="button" target="_blank" rel="noopener noreferrer">
        {_("home.website")}
      </a>
    </Jumbotron>
  );
};

export default HomePage;
