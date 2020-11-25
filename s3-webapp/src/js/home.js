import React from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';

class Home extends React.Component {
  constructor(props) {
    super();
    this.state = {date: new Date().getFullYear(), searchValue: ''};
    this.handleSearchChange = this.handleSearchChange.bind(this);
  }

  render() {

    return (
      <div className="post">
        <div className="post-title">
        <h1>A Tech Blog and Portfolio</h1>
        </div>
        <Container fluid="md">
        <Row>

        </Row>
        <Row>
        <Col sm={0} md={1}></Col>
        <Col sm={12} md={10}>
          <Form onSubmit={this.submitSearchForm.bind(this)} > 
            <Form.Group controlId="postSearchForm">
              <Form.Control type="text" placeholder="Search" autoComplete="false" value={this.state.searchValue} onChange={this.handleSearchChange} />
            </Form.Group>
          </Form>
        </Col>
        </Row>
        
        <Row>
        <Col md={1}></Col>
        <Col md={10}>

          </Col>
        </Row>


        <Row>
        <Col sm={0} md={1}></Col>
        <Col sm={12} md={10}>
          <div className="post">
          <div className="post-body">
            <p>Thank you for visting prestonfrazier.net! The site is currently under construction, but it will soon be a blog site for
            my personal interests, projects, and portfolio. Topics will include technology, programming, music, gaming, and other related content.
            Posts will be tagged and searchable.
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            <br />
            </p>
          </div>
        </div>
        </Col>
        </Row>
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

  }

  componentWillUnmount() {

  }

}


export default Home;
