import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
    // this.state={
    // }
  }
  render() {
    return (
      <div className="center">
        <HomePage />
      </div>
    );
    //or return <HomePage></HomePage>;
    //You should return one element only so always rap them
  }
}
const appDiv = document.getElementById("app");
render(<App />, appDiv);
// render(<App name="Mohammad" />, appDiv);
//name is a props
