import React, { useCallback, useContext } from "react";
import { AppContext, AppContextType } from "../../context/AppContext";
import { Button, Card, Container } from "react-bootstrap";
import { api, ApiError, useApi, useGet } from "../../api/api";
import { useI18n } from "../../utils";
import { GetRandomDetectionResponse } from "../../api/rqre";
import { withI18n, WithI18nProps } from "../../utils/i18n";

interface ClassifyFrameProps {
  data: GetRandomDetectionResponse;
}

const ClassifyFrame: React.FC<ClassifyFrameProps> = ({ data }) => {
  return (
    <>
      <Card.Title className="text-center"></Card.Title>
      <img src={data.detections[0].image} />
      <Card.Subtitle className="mb-2 text-muted text-center"></Card.Subtitle>
    </>
  );
};

const Loading: React.FC = () => {
  return <></>;
};

interface ClassifyPageState {
  loading: boolean;
  detection?: GetRandomDetectionResponse;
  error: string | null;
}

class ClassifyPage extends React.Component<WithI18nProps, ClassifyPageState, AppContextType> {
  static contextType = AppContext;

  state: ClassifyPageState = { loading: true, error: null };
  context!: AppContextType;

  render() {
    const { detection } = this.state;

    return (
      <Container className="mt-4">
        <Card>
          <Card.Body>{detection ? <ClassifyFrame data={detection} /> : "pending..."}</Card.Body>
        </Card>
      </Container>
    );
  }

  loadRandomDetection = async () => {
    try {
      const detection = await api<void, GetRandomDetectionResponse>("/api/classify/random/", this.context.token);
      this.setState(() => ({ loading: false, detection: detection, error: null }));
    } catch (ApiError) {
      this.setState(() => ({ loading: false, error: ApiError.getMessage(this.props._) }));
    }
  };

  componentDidMount(): void {
    this.loadRandomDetection().then();
  }
}

export default withI18n(ClassifyPage);
