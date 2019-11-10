import React from 'react';

import AppNavbar from './common/navbar.js';
import AppFooter from './common/footer.js';
import AppSideBar from './common/sidebar.js';

import '../css/app.css';

class App extends React.Component {

    render() {
      return (
        <div id="wrap" className="wrap">
        <div className="app">
        <AppNavbar />
        <div id="sidebarContainer">
            <main id="content" className="content">
            <h1>We’ll be back soon!</h1>
            <br /><br />
            <p>Sorry for the inconvenience but we’re performing a site redesign at the moment.
            We’ll be back online ASAP!
            </p>
              <br />
            </main>
            <br />
          </div>
        </div>
        <AppFooter />
        </div>
      );
    }

    componentDidMount() {

    }
}

export default App;
