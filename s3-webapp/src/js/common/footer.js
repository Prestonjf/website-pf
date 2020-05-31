import React from 'react';
import {version} from '../../../package.json';
import { SocialIcon } from 'react-social-icons';

class AppFooter extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {

    const linkStyle = {
      "textDecoration": "none",
      "color": "#ddffaa"
    };

    return (
      <div className="app-footer" >
        <a href="https://prestonfrazier.net?page=home" style={linkStyle}><b>Home</b></a>&nbsp;&nbsp;
        <a href="https://prestonfrazier.net?page=about" style={linkStyle}><b>About</b></a>&nbsp;&nbsp;
        <a href="https://prestonfrazier.net?page=tags" style={linkStyle}><b>Tags</b></a>&nbsp;&nbsp;
        <SocialIcon url="https://github.com/Prestonjf" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;&nbsp;
        <SocialIcon url="https://twitter.com/prestonfrazier" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
        <br />
        <span className="small credit copyright">Copyright &#169; {this.state.date}&nbsp;
        | <a href="https://prestonfrazier.net" style={linkStyle} rel="noopener noreferrer">prestonfrazier.net</a></span>&nbsp;
        <span className="small">
        | {process.REACT_APP_ENVIRONMENT} v{version}
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
