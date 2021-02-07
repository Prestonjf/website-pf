import React from 'react';
import {Link} from "react-router-dom";
import { Row, Col, Badge} from 'react-bootstrap';
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
                <Col sm="auto">
                <Link className="main-link-style-dark" to={getPostPath(post.id)}>
                  <img src={getPostFileUrl(post.id, post.primaryImageFile)} alt={index} height={100} width={150} className="post-list-img" />
                </Link>
                  <Link className="main-link-style-dark" to={getPostPath(post.id)}>{post.name}</Link>
                  <br />
                  <div className="small">{post.author.name} | {formatTimeStamp(post.createdDate)}</div>
                  <div className="">{post.summary}</div>
                  {post.tags && post.tags.map((tag, index2) => {
                    return (
                      <span key={index2}><Badge pill className="secondary-link-style-background">
                        <Link className="secondary-link-style" to={'/tags?tag=' + tag}>{tag}</Link>
                      </Badge>&nbsp;</span>
                    );
                  })}        
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
