import React from 'react';


class Tags extends React.Component {

  constructor(props) {
    super();
  }

  render() {

    return (
      <div className="post">
        <div className="post-title">
          Tags Coming Soon!
        </div>
      </div>
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

  fetchPosts(path) {
    const url = process.env.REACT_APP_API_URL+path;
    return fetch(url, {
      method: 'get', 
      headers: new Headers({
        'X-API-Key': process.env.REACT_APP_API_KEY
      })
    })
    .then(res => res.json())
    .then(
      (result) => {
        //console.debug(result)
        return result;
      },
      (error) => {
        //console.error(error);
        return error;
      }
    );
  }

}


export default Tags;
