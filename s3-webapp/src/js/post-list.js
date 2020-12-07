import React from 'react';
import {Link} from "react-router-dom";
import { Row, Col } from 'react-bootstrap';

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
                <Col md="auto">
                <img src={post.primary_image_path} alt={index} height={100} width={100} />
                </Col>
                <Col md="auto">
                <Link className="main-link-style-dark" to={post.post_url}>{post.post_name}</Link>
                <br />
                <div className="small">{post.author_name} | {formatTimeStamp(post.post_created_date)}</div>
                <div className="small">{post.post_summary}</div>
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

function formatTimeStamp(str) {
    let time = '';
    var options = {year: 'numeric', month: 'long', day: 'numeric' };
    if (str) {
      time = new Date(str);
      return time.toLocaleTimeString('en-US', options)
    }
    return time;
  }

export default PostList
