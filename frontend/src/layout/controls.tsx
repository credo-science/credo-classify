import React from "react";

export type OnSetValue<T> = (name: keyof T, value: number | null) => void;

interface CheckButtonProps<T> {
  classBem: string;
  name: keyof T;
  value: number | null;
  myValue: number;
  uncheckable?: boolean;
  onSetValue: OnSetValue<T>;
  children: React.ReactNode;
}

export class CheckButton<T> extends React.PureComponent<CheckButtonProps<T>> {
  render() {
    const { classBem, value, myValue, children } = this.props;
    return (
      <button className={`btn btn__${classBem}${myValue === value ? "--checked" : ""}`} onClick={this.handleSetValue}>
        {children}
      </button>
    );
  }

  handleSetValue = () => {
    const { name, value, myValue, uncheckable, onSetValue } = this.props;

    if (uncheckable) {
      onSetValue(name, value === myValue ? null : myValue);
    } else if (value !== myValue) {
      onSetValue(name, myValue);
    }
  };
}
