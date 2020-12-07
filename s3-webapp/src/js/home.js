import React from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
import PostList from './post-list.js';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {date: new Date().getFullYear(), searchValue: ''};
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  render() {

    return (
      <div className="post">
        <div className="post-title">
        <h1>A Tech Blog and Portfolio</h1>
        </div>
        <Container fluid="md">
        <Row>
        <Col>
          <Form onSubmit={this.submitSearchForm.bind(this)} > 
            <Form.Group controlId="postSearchForm">
              <Form.Control type="text" placeholder="Search..." autoComplete="false" value={this.state.searchValue} onChange={this.handleSearchChange} />
            </Form.Group>
          </Form>
        </Col>
        </Row>
        <br />
        <PostList posts={this.state.posts}  />
      </Container>



      </div>
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
    this.fetchPosts().then(response => {
      this.setState({posts: response})
    });
  }

  fetchPosts() {
    const url = process.env.REACT_APP_API_URL+'/search?q=about';
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
        return error;
      }
    );
  }

}


export default Home;
