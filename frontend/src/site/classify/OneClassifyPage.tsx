import React, { useCallback } from "react";
import { AppContext, AppContextType } from "../../context/AppContext";
import { Alert, Button, Card, Col, Container, Row } from "react-bootstrap";
import { apiClient, ApiOptions } from "../../api/api";
import { withI18n, WithI18nProps } from "../../utils/i18n";
import { AttributeEntity, DetectionEntity, DeviceEntity, UserEntity } from "../../api/entities";
import { CommonClassifyProps, formatScopeInfo } from "./commons";

type OnSetClass = (value: number) => void;

export interface Detection extends Omit<DetectionEntity, "device"> {
  device: DeviceEntity;
  attributes: AttributeEntity[];
}

export interface GetRandomDetectionResponse {
  user: UserEntity;
  detection: Detection;
}

export interface ClassifyParams {
  user?: number;
  team?: number;
}

export interface SubmitClassifyRequest {
  id: number;
  attribute: string;
  value: number;
}

interface ClassifyButtonProps {
  myValue: number;
  onSetClass: OnSetClass;
  children: React.ReactNode;
  loading: boolean;
}

export const ClassifyOneButton: React.FC<ClassifyButtonProps> = ({ myValue, onSetClass, children, loading }) => {
  const handleStClass = useCallback(() => {
    onSetClass(myValue);
  }, [onSetClass, myValue]);

  return (
    <button className={`btn btn-success btn__classify__one__${myValue} : ""}`} disabled={loading} onClick={handleStClass}>
      {children}
    </button>
  );
};

interface ClassifyPageState {
  loading: boolean;
  detection?: Detection;
  error: string | null;
}

class OneClassifyPage extends React.Component<WithI18nProps & CommonClassifyProps, ClassifyPageState, AppContextType> {
  static contextType = AppContext;

  state: ClassifyPageState = { loading: true, error: null };
  context!: AppContextType;

  render() {
    const { _ } = this.props;
    const { detection, loading, error } = this.state;

    return (
      <Container className="mt-4">
        {detection && this.renderDetection()}
        {loading && <Alert variant="info">{_(detection ? "classify.common.msg.p" : "classify.common.msg.loading")}</Alert>}
        {error && <Alert variant="danger">{_("classify.common.msg.e")}</Alert>}
      </Container>
    );
  }

  renderDetection() {
    const { _ } = this.props;
    const { detection, loading } = this.state;

    return (
      <>
        <Card.Subtitle className="mb-2 mt-2 text-muted text-center">{formatScopeInfo(_, this.props)}</Card.Subtitle>
        <div className="text-center div__img">
          <img src={`data:image/png;base64,${detection!.frame_content}`} className="img__hit" alt={_("classify.common.img.alt")} />
        </div>
        <Card.Subtitle className="mb-2 mt-2 text-muted text-center">{`ID: ${detection!.id}, ${_("classify.common.subtitle")}`}</Card.Subtitle>

        <Row>
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={1} loading={loading}>
              {_("classify.attr.spot")}
            </ClassifyOneButton>
          </Col>
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={3} loading={loading}>
              {_("classify.attr.track")}
            </ClassifyOneButton>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={2} loading={loading}>
              {_("classify.attr.worm")}
            </ClassifyOneButton>
          </Col>
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={6} loading={loading}>
              {_("classify.attr.amazing")}
            </ClassifyOneButton>
          </Col>
        </Row>

        <Row className="mt-4">
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={5} loading={loading}>
              {_("classify.attr.multi")}
            </ClassifyOneButton>
          </Col>
          <Col xs={6} className="text-center">
            <ClassifyOneButton onSetClass={this.onSetClass} myValue={4} loading={loading}>
              {_("classify.attr.artifact")}
            </ClassifyOneButton>
          </Col>
        </Row>

        <div className="text-center mt-4 mb-4">
          <Button variant="secondary" disabled={loading} onClick={this.onSubmit}>
            {_("classify.common.next")}
          </Button>
        </div>
      </>
    );
  }

  loadRandomDetection = async (value: number | null) => {
    try {
      const params: ClassifyParams = { user: this.props.user_id, team: this.props.team_id };

      this.setState(() => ({ loading: true }));
      const options: ApiOptions<SubmitClassifyRequest> = value
        ? { method: "POST", data: { id: this.state.detection!.id, attribute: "class", value }, params }
        : { params };
      const detection = await apiClient<GetRandomDetectionResponse, SubmitClassifyRequest>("api/classify/one/", this.context, options);
      this.setState(() => ({ loading: false, detection: detection!.data.detection, error: null, classes: {} }));
      this.context.updateUser(detection!.data.user);
    } catch (ApiError) {
      this.setState(() => ({ loading: false, error: ApiError.getMessage(this.props._) }));
    }
  };

  onSetClass: OnSetClass = value => {
    if (!this.state.loading) {
      this.loadRandomDetection(value).then();
    }
  };

  onSubmit = () => {
    if (!this.state.loading) {
      this.loadRandomDetection(null).then();
    }
  };

  componentDidMount(): void {
    this.loadRandomDetection(null).then();
  }
}

export default withI18n(OneClassifyPage);
