import React from 'react';
import {version} from '../../../package.json';

class AppFooter extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {

    return (
      <div className="app-footer" >
      <span className="small credit copyright">Copyright &#169; {this.state.date} &nbsp;
      <a href="https://prestonfrazier.net" target="_blank" rel="noopener noreferrer">prestonfrazier.net</a></span>
      <br />
      <span className="small">
      Website | {process.REACT_APP_ENVIRONMENT} v{version}
      </span>
      </div>
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

}


export default AppFooter;
