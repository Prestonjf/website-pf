import React from 'react';
import {Link} from "react-router-dom";
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
      <div className="app-footer" id='app-footer'>
        <Link style={linkStyle} to="/"><b>Home</b></Link>&nbsp;&nbsp;
        <Link style={linkStyle} to="/post"><b>About</b></Link>&nbsp;&nbsp;
        <Link style={linkStyle} to="/tags"><b>Tags</b></Link>&nbsp;&nbsp;
        <SocialIcon url="https://github.com/Prestonjf" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;&nbsp;
        <SocialIcon url="https://www.linkedin.com/in/preston-frazier/" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;&nbsp;
        <SocialIcon url="/rss.xml" network="rss" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
        <br />
        <Link className="small" style={linkStyle} to="/cookies">Cookie Policy</Link>&nbsp;&nbsp;
        <Link className="small" style={linkStyle} to="/sitemap.xml" target="_blank">Sitemap</Link>&nbsp;&nbsp;
        <br />
        <span className="small credit copyright">Copyright &#169; {this.state.date}&nbsp;
        | <Link style={linkStyle}  to="/">prestonfrazier.net</Link></span>&nbsp;
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
