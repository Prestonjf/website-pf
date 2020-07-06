import React from 'react';
import {Route, Switch} from "react-router-dom";
import { Button } from 'react-bootstrap';

import AppNavbar from './common/navbar.js';
import AppFooter from './common/footer.js';
import Post from './common/post.js';
import Home from './common/home.js';
import Tags from './common/tags.js';
import CommonPost from './common/common-post.js';

import '../css/app.css';

class App extends React.Component {



    render() {
      let cookiePolicyNotifcation = this.showCookiePolicy();

      return (
        <div id="wrap" className="wrap">
        <div className="app">
        <AppNavbar />
          <main id="content" className="content">
          <Switch>
            <Route path="/" exact= {true} component={Home} />
            <Route path="/tags" exact= {true} component={Tags} />
            <Route path="/post" exact= {true} component={Post} />
            <Route path="/privacypolicy" exact= {true} component={CommonPost} />
            <Route path={["/sitemap"]} component={() => {
               window.location.href = '/sitemap.xml';
               return null;
             }}/>
             <Route path={["/robots"]} component={() => {
                window.location.href = '/robots.txt';
                return null;
              }}/>
            <Route path="/*" component={Post} />
          </Switch>
          </main>
        </div>
        <br />
        <AppFooter />
        {cookiePolicyNotifcation}
        </div>
      );
    }

    componentDidMount() {
      window.addEventListener('resize', this.handleFooterResize);
      this.handleFooterResize();
      this.showCookiePolicy();
    }

    handleFooterResize() {
      document.getElementById("content").style.paddingBottom = document.getElementById('app-footer').clientHeight+'px';
    }

    showCookiePolicy() {
      if (!localStorage.getItem('cookies-policy-notice-accepted') || localStorage.getItem('cookies-policy-notice-accepted') === false) {
        return (
          <div id="cookiePolicyNotification" className="small">
                We use cookies on our website to improve your user experience.
                Click "Accept" if you are ok with this. Please read our&nbsp;
                <a href="/privacypolicy#cookies" className="cookieLink">Privacy Policy</a> for more information.&nbsp;
          <Button size="sm" style={{ backgroundColor: "#343a40", borderColor: "#343a40"}}  onClick={() => this.acceptCookiePolicy('accept')}>Accept</Button>&nbsp;
          <Button size="sm" style={{ backgroundColor: "#343a40", borderColor: "#343a40"}}  onClick={() => this.acceptCookiePolicy('decline')}>Decline</Button>&nbsp;
          </div>
      );
      }
      return;
    }

    acceptCookiePolicy(value) {
      localStorage.setItem('cookies-policy-notice-accepted', true);
      localStorage.setItem('cookie-consent-essential-accepted', true);
      localStorage.setItem('cookie-consent-session-accepted', ((value === 'decline') ? false : true));
      localStorage.setItem('cookie-consent-persistant-accepted', ((value === 'decline') ? false : true));
      document.getElementById('cookiePolicyNotification').style.display = 'none';
    }

}


export default App;
