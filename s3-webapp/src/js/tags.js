import React from 'react';
import {Link} from "react-router-dom";
import { Container, Row, Col, Badge } from 'react-bootstrap';
import PostList from './post-list.js';

class Tags extends React.Component {

  constructor(props) {
    super();
    this.fetchTags = this.fetchTags.bind(this);
    this.fetchTagsPosts = this.fetchTagsPosts.bind(this);
    this.state = { tags: {}, tag: getSearchTag() }
  }

  render() {
    const marginBottom = {'marginBottom': '10px'};

    return (
      <div className="post">
        <div className="post-title">
          Tags
          {this.state.posts && <span><br/><h5>Tag: {this.state.tag}</h5><hr /></span>}
        </div>
        <br />
        
        <div className="post-body">
        <Container fluid="md">
        {this.state.posts && <PostList posts={this.state.posts}  />} 


        <Row className="justify-content-md-center">
        {this.state.tags && Object.entries(this.state.tags).map(([key, value]) =>{
            return (
              <Col sm="auto" key={key} className="d-flex justify-content-center" style={marginBottom}>
                <Badge pill className="secondary-link-style-background">
                <Link className="secondary-link-style" to={'/tags?tag=' + key + '&d=' + Date.now() }>{key}</Link>
                  &nbsp;&nbsp;<Badge variant="light">{value}</Badge>
                </Badge>
              </Col>
              );
        })}
        </Row>
        </Container>
        </div>
      </div>
    );
  }

  componentDidMount() {
    if (this.state.tag) {
      this.fetchTagsPosts(this.state.tag).then(response => {
        this.setState({posts: response})
      });
    }
    else {
      this.fetchTags().then(response => {
        this.setState({tags: response})
      });
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const search = this.props.location.search;
    if ((search !== prevProps.location.search)) {
      const searchTag = getSearchTag();
      if (searchTag) {
        this.fetchTagsPosts(searchTag).then(response => {
          this.setState({posts: response, tag: searchTag, tags: []})
        });
      }
      else {
        this.fetchTags().then(response => {
          this.setState({posts: null, tags: response})
        });
      }
    }
  }

  fetchTags() {
    const url = process.env.REACT_APP_API_URL+'/posts/tags';
    return fetch(url, {
      method: 'get', 
      headers: new Headers({
        'X-API-Key': process.env.REACT_APP_API_KEY
      })
    })
    .then(res => res.json())
    .then(
      (result) => {
        return result.tags;
      },
      (error) => {
        console.error(error);
        return [];
      }
    );
  }

  fetchTagsPosts(tag) {
    const url = process.env.REACT_APP_API_URL+'/posts/tags/' + tag;
    return fetch(url, {
      method: 'get', 
      headers: new Headers({
        'X-API-Key': process.env.REACT_APP_API_KEY
      })
    })
    .then(res => res.json())
    .then(
      (result) => {
        return result.posts;
      },
      (error) => {
        console.error(error);
        return [];
      }
    );
  }

}

function getSearchTag() {
  const queryString = window.location.search;
  const param = new URLSearchParams(queryString).get('tag');
  if (param) {
    return decodeURIComponent(param);
  }
  return null;
}

export default Tags;
