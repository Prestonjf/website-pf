import React from 'react';
import {Link} from "react-router-dom";
import { Row, Col } from 'react-bootstrap';
import { formatTimeStamp, getPostFileUrl , getPostPath} from './utils';

class PostList extends React.Component {
  
  constructor(props) {
    super();
  }

  render() {
    return (
        <div className="post-list-body">
        {this.props.posts && this.props.posts.map((post, index) => {
            let thumbnail = getThumbnail(post, index);
            return (
                <div key={index} >
                <div className="post-list-item">
                <Row>
                <Col sm="">
                {thumbnail}
                <Link className="main-link-style-dark" to={getPostPath(post.id)}>{post.name} | </Link>
                <span className="">{post.summary}</span>
                &nbsp;|&nbsp;
                <span className="small">{formatTimeStamp(post.createdDate)}</span>
                </Col>
                </Row>
                </div>
                </div>
                
              );
        })}
        </div>
    );
  }

  componentDidMount() {

  }

  componentDidUpdate(prevProps, prevState, snapshot) {

  }
}

function getThumbnail(post, index) {
  if (post.primaryImageThumbnail) {
    return (
    <Link className="main-link-style-dark" to={getPostPath(post.id)}>
    <img src={getPostFileUrl(post.id, post.primaryImageThumbnail)} alt={index} width={160} className="post-list-img" />
  </Link>);
  }
  return '';
}

export default PostList
