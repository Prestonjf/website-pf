import React from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';

class Home extends React.Component {

  constructor(props) {
    super(props);
    this.state = {date: new Date().getFullYear()};
  }

  render() {
    const style = {
      "textAlign":"left"
    };

    return (
      <div className="home">
        <h1>A Tech Blog and Portfolio</h1>
        <p><i>by Preston Frazier</i></p>
        <Container fluid="md">
        <Row>

        </Row>
        <Row>
        <Col md={1}></Col>
        <Col md={10}>
          <Form>
            <Form.Group controlId="formBasicEmail">
              <Form.Control type="email" placeholder="Search for a post" />
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
        <Col md={1}></Col>
        <Col md={10} style={style}>
          <p>Thank you for visting prestonfrazier.net! The site is currently under construction, but it will soon be a blog site for
          my personal interests, projects, and portfolio. Topics will include technology, programming, music, gaming, and other related content.
          Posts will be tagged and searchable.

          </p>
        </Col>
        </Row>
      </Container>



      </div>
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

}


export default Home;
