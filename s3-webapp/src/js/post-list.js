import React from 'react';
import {Link} from "react-router-dom";
import { Row, Col, Badge} from 'react-bootstrap';
import { formatTimeStamp } from './utils';

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
                <img src={post.primary_image_path} alt={index} height={100} width={100} />
                </Col>
                <Col >
                  <Link className="main-link-style-dark" to={post.post_url}>{post.post_name}</Link>
                  <br />
                  <div className="small">{post.author_name} | {formatTimeStamp(post.post_created_date)}</div>
                  <div className="">{post.post_summary}</div>
                  {post.post_tags && post.post_tags.map((tag, index2) => {
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
