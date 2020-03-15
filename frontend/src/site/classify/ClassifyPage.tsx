import React, { useCallback } from "react";
import { AppContext, AppContextType } from "../../context/AppContext";
import { Alert, Button, Card, Container } from "react-bootstrap";
import { apiClient, ApiOptions } from "../../api/api";
import { withI18n, WithI18nProps } from "../../utils/i18n";
import { AttributeEntity, DetectionEntity, DeviceEntity, UserEntity } from "../../api/entities";

const HardcodedAttributes = [
  { name: "spot", title: "classify.attr.spot" },
  { name: "track", title: "classify.attr.track" },
  { name: "worm", title: "classify.attr.worm" },
  { name: "artifact", title: "classify.attr.artifact" }
];
const SCORES = [1, 2, 3, 4, 5];

export type OnSetClass = (attribute: string, value: number | null) => void;
export type Classes = { [attrib: string]: number | null };

export interface Detection extends Omit<DetectionEntity, "device"> {
  device: DeviceEntity;
  attributes: AttributeEntity[];
}

export interface GetRandomDetectionResponse {
  user: UserEntity;
  detection: Detection;
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

class ClassifyPage extends React.Component<WithI18nProps, ClassifyPageState, AppContextType> {
  static contextType = AppContext;

  state: ClassifyPageState = { loading: true, error: null, classes: {} };
  context!: AppContextType;

  render() {
    const { _ } = this.props;
    const { detection, loading, error } = this.state;

    return (
      <Container className="mt-4">
        {detection && this.renderDetection()}
        {loading && <Alert variant="info">{_(detection ? "classify.msg.p" : "classify.msg.loading")}</Alert>}
        {error && <Alert variant="danger">{_("classify.msg.e")}</Alert>}
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
        <div className="text-center div__img">
          <img src={`data:image/png;base64,${detection!.frame_content}`} className="img__hit" alt={_("classify.img.alt")} />
        </div>
        <Card.Subtitle className="mb-2 mt-2 text-muted text-center">{`ID: ${detection!.id}, ${_("classify.subtitle")}`}</Card.Subtitle>
        <div className="div__attributes">
          <table className="table__attributes">
            <tbody>{attributes.map(o => this.renderScoreRow(o.name, o.title, classes[o.name]))}</tbody>
          </table>
        </div>
        <div className="text-center mt-4 mb-4">
          <Button variant={fullFilled ? "success" : filled ? "warning" : "secondary"} disabled={loading} onClick={this.onSubmit}>
            {filled ? _("classify.submit") : _("classify.next")}
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
      this.setState(() => ({ loading: true }));
      const options: ApiOptions<SubmitClassifyRequest> = submit ? { method: "POST", data: { id: this.state.detection!.id, classes: this.state.classes } } : {};
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
    const filled = this.getFilledCount();
    this.loadRandomDetection(filled > 0).then();
  };

  componentDidMount(): void {
    this.loadRandomDetection(false).then();
  }

  getFilledCount = () => {
    const { classes } = this.state;
    return Object.keys(classes).reduce((sum, key) => sum + (classes[key] ? 1 : 0), 0);
  };
}

export default withI18n(ClassifyPage);
