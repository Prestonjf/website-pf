import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

class Search extends React.Component {

  constructor(props) {
    super();
    this.state = {searchValue: '', results: ''};
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  render() {

    let results = "";
    if (this.state.results && this.state.results.posts) {
      
      results = this.state.results.posts.length;
    }

    return (
      <Container fluid="md">
      <Row>
      <Col sm={0} md={1}></Col>
      <Col sm={12} md={10} >
      <div className="post">
        <div className="post-title">
          Post Search Results
          <br />
          <h5>Search: {this.state.searchValue}</h5>
        </div>
        <div className="post-body">
          {results}
        </div>
      </div>
      </Col>
      </Row>
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
    const url = process.env.REACT_APP_API_URL+'/search?'+encodeURIComponent(search);
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
