import React from 'react';
import {Link} from "react-router-dom";
import {version} from '../../package.json';
import { SocialIcon } from 'react-social-icons';
import CommonModal from './common-modal.js';

class AppFooter extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {

    return (
      <div className="app-footer" id='app-footer'>
        <Link className="main-link-style" to="/"><b>Home</b></Link>&nbsp;&nbsp;
        <Link className="main-link-style" to="/tags"><b>Tags</b></Link>&nbsp;&nbsp;
        <Link className="main-link-style" to="/post/portfolio"><b>Portfolio</b></Link>&nbsp;&nbsp;  
        <Link className="main-link-style" to="/post/about"><b>About</b></Link>&nbsp;&nbsp;       
        <SocialIcon url="https://github.com/Prestonjf" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;&nbsp;
        <SocialIcon url="https://www.linkedin.com/in/preston-frazier/" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;&nbsp;
        <SocialIcon url="/rss.xml" network="rss" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
        <br />
        <Link className="secondary-link-style small" to="/privacypolicy">Privacy Policy</Link>&nbsp;&nbsp;
        <CommonModal type="cookiepreferences" />&nbsp;&nbsp;
        <Link className="secondary-link-style small" to="/sitemap.xml" target="_blank">Sitemap</Link>&nbsp;&nbsp;
        <br />
        <span className="small credit copyright">Copyright &#169; {this.state.date}&nbsp;
        | <Link className="secondary-link-style"  to="/">prestonfrazier.net</Link></span>&nbsp;
        <span className="small">
        | {process.env.REACT_APP_ENV} v{version}
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
