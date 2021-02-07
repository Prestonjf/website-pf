import React from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
import yaml from 'js-yaml';
import PostList from './post-list.js';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {date: new Date().getFullYear(), searchValue: ''};
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.fetchFeaturedPosts = this.fetchFeaturedPosts.bind(this);
  }

  render() {

    return (
      <Container fluid="md">
      <div className="post">
        <div className="post-title">
          A Tech Blog and Portfolio
        </div>
        <Row>
        <Col>
          <Form onSubmit={this.submitSearchForm.bind(this)} > 
            <Form.Group controlId="postSearchForm">
              <Form.Control type="text" placeholder="Search..." autoComplete="false" value={this.state.searchValue} onChange={this.handleSearchChange} />
            </Form.Group>
          </Form>
        </Col>
        </Row>

        <PostList posts={this.state.posts}  />
      </div>
      </Container>
    );
  }
  
  handleSearchChange(e) {
    this.setState({searchValue: e.target.value});
  }

  submitSearchForm(e) {
    const value = encodeURIComponent(this.state.searchValue);
    this.setState({searchValue: ""});
    this.props.history.push("/search?q=" + value);
    e.preventDefault();
  }

  componentDidMount() {
    this.fetchFeaturedPosts().then(response => {
      this.setState({posts: response})
    });
  }

  fetchFeaturedPosts() {
    const url = process.env.REACT_APP_WEB_URL+'/featured.yml';
    return fetch(url, {
      method: 'get', 
      cache: "reload"
    })
    .then(res => res.text())
    .then((result) => {
      const featured = yaml.load(result);
      let promises = [];
      featured.featured.forEach(function(p) {
        promises.push(fetchPosts(p));
      });
      const posts = compilePosts(promises);
      return posts;
      },
      (error) => {
        console.error(error);
        return [];
      }
    );
  }

}

async function compilePosts(promises) {
  let posts = [];
  await Promise.all(promises).then((values) => {
    values.forEach(function(value) {
      if (value != null) posts.push(value);
    });
  });
  return posts;
}

async function fetchPosts(path) {
    try {
      const res = await fetch(process.env.REACT_APP_WEB_URL + '/posts/' + path + '/config.yml', { cache: 'reload' });
      const result = await res.text();
      const yml = yaml.load(result);
      if (yml.id) {
        return yml;
      }
      return null;
    } catch (error) {
      console.log(error);
      return null;
    }
}

export default Home;
