import React from "react";
import { Jumbotron } from "react-bootstrap";
import { useI18n } from "../utils";
import { Link } from "react-router-dom";

const HomePage: React.FC = () => {
  const _ = useI18n();

  return (
    <Jumbotron>
      <h1 className="display-4">{_("home.title")}</h1>
      <p className="lead">{_("home.lead")}</p>
      <hr className="my-4" />
      <p>{_("home.description")}</p>
      <div className="text-center">
        <Link to="/classify" className="btn btn-lg btn-success mb-4">
          {_("home.classify")}
        </Link>
        <br />
        <a className="btn btn-primary btn-lg" href="https://credo.science/" role="button" target="_blank" rel="noopener noreferrer">
          {_("home.website")}
        </a>
      </div>
    </Jumbotron>
  );
};

export default HomePage;
