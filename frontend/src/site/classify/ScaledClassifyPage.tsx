import React, { useCallback } from "react";
import { AppContext, AppContextType } from "../../context/AppContext";
import { Alert, Button, Card, Container } from "react-bootstrap";
import { apiClient, ApiOptions } from "../../api/api";
import { withI18n, WithI18nProps } from "../../utils/i18n";
import { AttributeEntity, DetectionEntity, DeviceEntity, UserEntity } from "../../api/entities";
import { Classes, CommonClassifyProps, formatScopeInfo } from "./commons";

const HardcodedAttributes = [
  { name: "spot", title: "classify.attr.spot" },
  { name: "track", title: "classify.attr.track" },
  { name: "worm", title: "classify.attr.worm" },
  { name: "multi", title: "classify.attr.multi" },
  { name: "artifact", title: "classify.attr.artifact" },
  { name: "amazing", title: "classify.attr.amazing" }
];
const SCORES = [1, 2, 3, 4, 5];

export type OnSetClass = (attribute: string, value: number | null) => void;

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
  classes: Classes;
}

interface ClassifyButtonProps {
  attribute: string;
  value: number | null;
  myValue: number;
  onSetClass: OnSetClass;
}

export const ClassifyButton: React.FC<ClassifyButtonProps> = ({ attribute, value, myValue, onSetClass }) => {
  const handleStClass = useCallback(() => {
    onSetClass(attribute, value === myValue ? null : myValue);
  }, [attribute, myValue, onSetClass, value]);

  return (
    <button className={`btn btn__classify__${myValue}${myValue === value ? "--checked" : ""}`} onClick={handleStClass}>
      {myValue}
    </button>
  );
};

interface ClassifyPageState {
  loading: boolean;
  detection?: Detection;
  error: string | null;
  classes: Classes;
}

class ScaledClassifyPage extends React.Component<WithI18nProps & CommonClassifyProps, ClassifyPageState, AppContextType> {
  static contextType = AppContext;

  state: ClassifyPageState = { loading: true, error: null, classes: {} };
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
    const { detection, loading, classes } = this.state;

    const attributes = HardcodedAttributes;
    const filled = this.getFilledCount();
    const fullFilled = filled === attributes.length;

    return (
      <>
        <Card.Subtitle className="mb-2 mt-2 text-muted text-center">{formatScopeInfo(_, this.props)}</Card.Subtitle>
        <div className="text-center div__img">
          <img src={`data:image/png;base64,${detection!.frame_content}`} className="img__hit" alt={_("classify.common.img.alt")} />
        </div>
        <Card.Subtitle className="mb-2 mt-2 text-muted text-center">{`ID: ${detection!.id}, ${_("classify.common.subtitle")}`}</Card.Subtitle>
        <div className="div__attributes">
          <table className="table__attributes">
            <tbody>{attributes.map(o => this.renderScoreRow(o.name, o.title, classes[o.name]))}</tbody>
          </table>
        </div>
        <div className="text-center mt-4 mb-4">
          <Button variant={fullFilled ? "success" : filled ? "warning" : "secondary"} disabled={loading} onClick={this.onSubmit}>
            {filled ? _("classify.common.submit") : _("classify.common.next")}
          </Button>
        </div>
      </>
    );
  }

  renderScoreRow(name: string, title: string, value: number | null) {
    const { _ } = this.props;

    return (
      <tr key={name}>
        <th className="text-right">{_(title)}:</th>
        {SCORES.map(o => (
          <td key={`${name}_${o}`}>
            <ClassifyButton attribute={name} value={value} myValue={o} onSetClass={this.onSetClass} />
          </td>
        ))}
      </tr>
    );
  }

  loadRandomDetection = async (submit: boolean) => {
    try {
      const params: ClassifyParams = { user: this.props.user_id, team: this.props.team_id };

      this.setState(() => ({ loading: true }));
      const options: ApiOptions<SubmitClassifyRequest> = submit
        ? { method: "POST", data: { id: this.state.detection!.id, classes: this.state.classes }, params }
        : { params };
      const detection = await apiClient<GetRandomDetectionResponse, SubmitClassifyRequest>("api/classify/scaled/", this.context, options);
      this.setState(() => ({ loading: false, detection: detection!.data.detection, error: null, classes: {} }));
      this.context.updateUser(detection!.data.user);
    } catch (ApiError) {
      this.setState(() => ({ loading: false, error: ApiError.getMessage(this.props._) }));
    }
  };

  onSetClass: OnSetClass = (attribute, value) => {
    this.setState(old => ({ classes: { ...old.classes, [attribute]: value } }));
  };

  onSubmit = () => {
    if (!this.state.loading) {
      const filled = this.getFilledCount();
      this.loadRandomDetection(filled > 0).then();
    }
  };

  componentDidMount(): void {
    this.loadRandomDetection(false).then();
  }

  getFilledCount = () => {
    const { classes } = this.state;
    return Object.keys(classes).reduce((sum, key) => sum + (classes[key] ? 1 : 0), 0);
  };
}

export default withI18n(ScaledClassifyPage);
