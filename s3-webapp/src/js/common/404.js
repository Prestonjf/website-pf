import React from 'react';


class NotFound extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {

    return (
      <div className="post">
        <h1>404</h1>
        <br /><br />
        <p>Sorry for the inconvenience, but the page you are looking for cannot be found.
        </p>
        <br />



      </div>
      /**
        Post Title

        Post Author     post share
        Post date       Post Tags
        last updated

        Html post content ....



      **/
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

}


export default NotFound;
