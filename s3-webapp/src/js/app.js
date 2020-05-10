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
      console.log(process.env.REACT_APP_API_URL);
      const url = process.env.REACT_APP_API_URL+'/init';
      fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result);
          this.setState({isLoaded: true, items: result.items});
        },
        (error) => {
          this.setState({isLoaded: true, error});
        }
      )
    }
}

export default App;
