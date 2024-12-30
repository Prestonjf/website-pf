import React from 'react';
import yaml from 'js-yaml';
import {Link} from "react-router-dom";
import {Helmet} from "react-helmet";
import { Container, Row, Col, Badge} from 'react-bootstrap';

import { formatTimeStamp } from './utils';

class Post extends React.Component {
  constructor(props) {
    super();
    this.state = { post: null };
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  render() {
    if (this.state.post && this.state.post.id && JSON.stringify(this.state.post.id).length > 0) {
      const post = this.state.post;
      const updatedDate = getUpdatedTime(post.createdDate, post.updatedDate);
      // Optional Photo credit
      // <p className="photo-credit">Photo by <a href=""></a> on <a href=""></a></p>
      return (
        <div>
        <div className="post-title">
        {post.primaryImageFile.length > 0 && <img alt="primary-post-img" src={this.state.postFolder + post.primaryImageFile} width="100%" />}
        <br />
        {post.name}
        </div>
        
        <Container fluid="md">
        <Helmet>
            <title>{post.name} - PrestonFrazier.net</title>
        </Helmet>
        <Row>
        <Col sm={0} md={1}></Col>
        <Col sm={12} md={10} >
        <div className="post">
          <div className="post-body">
            <div className="small">
            By: {post.author.name} | {formatTimeStamp(post.createdDate)}
            {updatedDate && <span><br />Updated: {formatTimeStamp(post.updatedDate)}</span>}
            </div>
            <br />
            <div dangerouslySetInnerHTML={{ __html: post.html }} />

            {post.tags && post.tags.map((tag, index) => {
              return (
                <span key={index}><Badge pill className="secondary-link-style-background">
                  <Link className="secondary-link-style" to={'/tags?tag=' + tag}>{tag}</Link>
                </Badge>&nbsp;</span>
              );
            })} 
          </div>
        </div>
        </Col>
        </Row>
        </Container>
        </div>
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
        const postFolder = process.env.REACT_APP_WEB_URL + '/posts/' + response.id + '/';
        this.setState({post: response, postFolder: postFolder});
      });
    else {
      this.setState({post: {}});
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const path = this.props.location.pathname;
    if ((path !== prevProps.location.pathname) && path.startsWith("/post/")) {
      this.setState({post: null});
      this.fetchPosts(this.props.location.pathname).then(response => {
        const postFolder = process.env.REACT_APP_WEB_URL + '/posts/' + response.id + '/';
        this.setState({post: response, postFolder: postFolder});
      });
    }
  }

  fetchPosts(path) {
    try {
      const page = path.split("/post/");
      return fetch(process.env.REACT_APP_WEB_URL + '/posts/' + page[1] + '/config.yml', {cache: 'reload'})
      .then(res => res.text(),
        (error) => {
          // console.log(error);
          return null;
        })
      .then((result) => {
          if (result) {
            const doc = yaml.load(result);
            if (doc.htmlFile)
              return doc;
            } 
          return null;
        })
        .then(function(data) {
          if (data) {
            return fetch(process.env.REACT_APP_WEB_URL + '/posts/' + page[1] + '/' + data.htmlFile, {cache: 'reload'})
            .then(res => res.text())
            .then((result) => {
              data.html = result;
              data.page = page;
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

export default Post;
