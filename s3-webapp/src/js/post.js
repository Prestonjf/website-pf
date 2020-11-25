import React from 'react';
import yaml from 'js-yaml';
import { Container, Row, Col } from 'react-bootstrap';

class Post extends React.Component {
  constructor(props) {
    super();
    this.state = {post: null};
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  render() {
    if (this.state.post && this.state.post.url && JSON.stringify(this.state.post.url).length > 0) {
      const post = this.state.post;
      const updatedDate = getUpdatedTime(post.createdDate, post.updatedDate);
      return (
        <Container fluid="md">
        <Row>
        <Col sm={0} md={1}></Col>
        <Col sm={12} md={10} >
        <div className="post">
          <div className="post-title">
            {post.name}
            <br />
            {post.primaryImageFile.length > 0 && <img alt="primary-post-img" src={post.primaryImageFile} />}
            <br /><br />
          </div>
    
          <div className="post-body">
            <div className="small">
            By: {post.author.name} | {formatTimeStamp(post.createdDate)}
            {updatedDate && <span><br />Updated: {formatTimeStamp(post.updatedDate)}</span>}
            </div>
            <br />
            <div dangerouslySetInnerHTML={{ __html: post.html }} />
            <br />
          </div>
        </div>
        </Col>
        </Row>
        </Container>
      );
    } else if (this.state.post) {
      // post not found
      return (<div><h1 className="main-link-style-dark">404</h1>
      <h6>Oops! We couldn't find that resource.</h6></div>);
    } else {
      // loading
      return (<div></div>);
    }
  }


  
  componentDidMount() {
    const path = this.props.location.pathname;
    if (path && path.startsWith("/post/"))
      this.fetchPosts(path).then(response => {
        this.setState({post: response});
      });
    else {
      this.setState({post: {}});
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const path = this.props.location.pathname;
    if ((path !== prevProps.location.pathname) && path.startsWith("/post/")) {
      this.setState({post: {}});
      this.fetchPosts(this.props.location.pathname).then(response => {
        this.setState({post: response});
      });
    }
  }

  fetchPosts(path) {
    try {
      const page = path.split("/post/");
      return fetch(process.env.REACT_APP_WEB_URL + '/posts/' + page[1] + '/config.yml')
      .then(res => res.text(),
        (error) => {
          // console.log(error);
          return null;
        })
      .then((result) => {
          if (result) {
            const doc = yaml.load(result);
            if (doc.s3Path)
              return doc;
            } 
          return null;
        })
        .then(function(data) {
          if (data) {
            return fetch(process.env.REACT_APP_WEB_URL + '/posts/' + page[1] + '/post.html')
            .then(res => res.text())
            .then((result) => {
              data.html = result;
              return data;
            })
          }
          else {
            return {};
          }
        });
    } catch (err) {
      return {};
    }
  }



}

function getUpdatedTime(date1, date2) {
  if (date1 !== date2) {
    return date2;
  } else {
    return null;
  }
}

function formatTimeStamp(str) {
  let time = '';
  var options = {year: 'numeric', month: 'long', day: 'numeric' };
  if (str) {
    time = new Date(str);
    return time.toLocaleTimeString('en-US', options)
  }
  return time;
}

export default Post;
