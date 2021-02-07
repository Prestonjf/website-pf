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
        <div className="post-body">
        {this.props.posts && this.props.posts.map((post, index) => {
            return (
                <div key={index}>
                <Row>
                <Col sm="">
                <Link className="main-link-style-dark" to={getPostPath(post.id)}>
                  <img src={getPostFileUrl(post.id, post.primaryImageFile)} alt={index} height={90} width={160} className="post-list-img" />
                </Link>
                  <Link className="main-link-style-dark" to={getPostPath(post.id)}>{post.name}</Link>
                  <br />
                  <div className="small">{post.author.name} | {formatTimeStamp(post.createdDate)}</div>
                  <div className="">{post.summary}</div>       
                </Col>
                </Row>
                <br />
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


export default PostList
