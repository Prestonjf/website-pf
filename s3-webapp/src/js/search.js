import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Spinner from 'react-bootstrap/Spinner';
import {Helmet} from "react-helmet";
import PostList from './post-list.js';

class Search extends React.Component {

  constructor(props) {
    super();
    this.state = {searchValue: getSearchValue(), results: ''};
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  render() {

    let loader = <Spinner animation="border" variant="dark" />;
    if (this.state.results && this.state.results.posts) {
      loader = "";
    }

    return (
      <Container fluid="md">
      <div className="post">
      <Helmet>
            <title>Search - PrestonFrazier.net</title>
        </Helmet>
      <Row>
      <Col sm={12} md={12} >
        <div className="post-title">
          Post Search Results
          <br />
          <h5>Search: {this.state.searchValue}</h5>
          <hr />
          {loader}
        </div>
      </Col>
      </Row>
      <PostList posts={this.state.results.posts}  />
      </div>
      </Container>
    );
  }

  componentDidMount() {
    const searchValue = getSearchValue();
    this.fetchPosts(searchValue).then(response => {
      this.setState({searchValue: searchValue, results: response})
    });

  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const search = this.props.location.search;
    if ((search !== prevProps.location.search)) {
      const searchValue = getSearchValue();
      this.fetchPosts(searchValue).then(response => {
        this.setState({searchValue: searchValue, results: response})
      });
    }
  }

  fetchPosts(search) {
    const url = process.env.REACT_APP_API_URL+'/posts/search?q='+encodeURIComponent(search);
    return fetch(url, {
      method: 'get', 
      headers: new Headers({
        'X-API-Key': process.env.REACT_APP_API_KEY
      })
    })
    .then(res => res.json())
    .then(
      (result) => {
        return result;
      },
      (error) => {
        console.error(error);
        return error;
      }
    );
  }

}

function getSearchValue() {
  const queryString = window.location.search;
  const param = new URLSearchParams(queryString).get('q');
  if (param) {
    return decodeURIComponent(param);
  }
  return '';
}

export default Search;
