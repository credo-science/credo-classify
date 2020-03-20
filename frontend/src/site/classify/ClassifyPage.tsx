import React from "react";
import { withI18n, WithI18nProps } from "../../utils/i18n";
import { AppContext, AppContextType } from "../../context/AppContext";
import { ButtonGroup, Card, Col, Container, Row } from "react-bootstrap";
import { CheckButton } from "../../layout/controls";
import { Link, Route, Switch } from "react-router-dom";
import ScaledClassifyPage from "./ScaledClassifyPage";
import { CommonClassifyProps } from "./commons";
import OneClassifyPage from "./OneClassifyPage";

interface FormState {
  checked: number;
  user: string;
  team: string;
  own: boolean;
}

interface ClassifyPageState extends FormState {
  loading: boolean;
  error: string | null;
  data?: { user_id: number; team_id: number };
}

class ClassifyPage extends React.Component<WithI18nProps, ClassifyPageState, AppContextType> {
  static contextType = AppContext;

  state: ClassifyPageState = { checked: 3, user: "", team: "", own: true, loading: false, error: null };
  context!: AppContextType;

  render() {
    const { checked } = this.state;
    const classifyProps: CommonClassifyProps = {};
    if (checked === 1) {
      classifyProps.user_id = this.context.user!.user_id;
      classifyProps.user_name = this.context.user!.username;
    } else if (checked === 2) {
      classifyProps.team_id = this.context.user!.team_id;
      classifyProps.team_name = this.context.user!.team_name;
    }

    return (
      <Switch>
        <Route path="/classify/one">
          <OneClassifyPage {...classifyProps} />
        </Route>
        <Route path="/classify/scaled">
          <ScaledClassifyPage {...classifyProps} />
        </Route>
        <Route path="/classify/select">TODO</Route>
        <Route path="/classify">{this.renderDashboard()}</Route>
      </Switch>
    );
  }

  renderDashboard() {
    const { _ } = this.props;
    const { checked } = this.state;

    return (
      <Container className="mt-4">
        <Card.Title className="text-center">{_("classify.scope")}</Card.Title>
        <ButtonGroup toggle className="w-100">
          <CheckButton classBem="classify_user" onSetValue={this.onSetValue} name="checked" value={checked} myValue={1}>
            {_("classify.user")}
          </CheckButton>
          <CheckButton classBem="classify_team" onSetValue={this.onSetValue} name="checked" value={checked} myValue={2}>
            {_("classify.team")}
          </CheckButton>
          <CheckButton classBem="classify_all" onSetValue={this.onSetValue} name="checked" value={checked} myValue={3}>
            {_("classify.all")}
          </CheckButton>
        </ButtonGroup>

        <div className={`div__classify_scope${checked === 3 ? "" : " div__classify_scope--expanded"}`}>
          <Card.Body>
            <Card.Subtitle className="text-center">
              {checked === 1 && `${_("classify.user")}: ${this.context.user!.username}`}
              {checked === 2 && `${_("classify.team")}: ${this.context.user!.team_name}`}
            </Card.Subtitle>
          </Card.Body>
        </div>

        <Card.Title className="text-center mt-4">{_("classify.go")}</Card.Title>
        <Row>
          <Col xs={6}>
            <Link to="/classify/one" className="btn btn-lg btn-block btn-success">
              {_("classify.one")}
            </Link>
          </Col>
          <Col xs={6}>
            <Link to="/classify/scaled" className="btn btn-lg btn-block btn-success">
              {_("classify.scaled")}
            </Link>
          </Col>
        </Row>
        <Row className="mt-4">
          <Col xs={12}>
            <Link to="/classify/select" className="btn btn-lg btn-block btn-secondary">
              {_("classify.select")}
            </Link>
          </Col>
        </Row>
      </Container>
    );
  }

  onSetValue = (name: keyof FormState, value: number | string | boolean | null) => {
    const newState = { [name]: value } as Pick<FormState, keyof FormState>;
    console.log(newState);
    this.setState(() => newState);
  };

  componentDidMount() {}
}

export default withI18n(ClassifyPage);
