import React from 'react';

import AppNavbar from './common/navbar.js';
import AppFooter from './common/footer.js';
import Post from './common/post.js';
import Home from './common/home.js';
import Tags from './common/tags.js';

import '../css/app.css';

class App extends React.Component {

    render() {
      return (
        <div id="wrap" className="wrap">
        <div className="app">
        <AppNavbar />
          <main id="content" className="content">
            <Home />
          </main>
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
