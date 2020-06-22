import React from 'react';
import {Route, Switch} from "react-router-dom";
import { Button } from 'react-bootstrap';

import AppNavbar from './common/navbar.js';
import AppFooter from './common/footer.js';
import Post from './common/post.js';
import Home from './common/home.js';
import Tags from './common/tags.js';

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
            <Route path="/cookies" exact= {true} component={Post} />
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
      if (!localStorage.getItem('acceptedCookiePolicyNotice') || localStorage.getItem('acceptedCookiePolicyNotice') === false) {
        return (<div id="cookiePolicyNotification" className="small">
                We use cookies to improve your experience with this site. To find out more,
          please read the full <a href="/cookies" className="cookieLink">Cookie Policy</a>.&nbsp;
          <Button size="sm" style={{ backgroundColor: "#343a40", borderColor: "#343a40"}}  onClick={() => this.acceptCookiePolicy()}>Ok</Button>
          </div>);
      }
      return;
    }

    acceptCookiePolicy() {
      localStorage.setItem('acceptedCookiePolicyNotice', true);
      document.getElementById('cookiePolicyNotification').style.display = 'none';
    }

}


export default App;
