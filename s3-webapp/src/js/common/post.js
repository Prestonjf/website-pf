import React from 'react';


class Post extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {

    return (
      <div className="post">
        <h1>We’ll be back soon!!</h1>
        <br /><br />
        <p>Sorry for the inconvenience but we’re performing a site redesign at the moment.
        We’ll be back online ASAP!
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


export default Post;
