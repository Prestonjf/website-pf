import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

class AppNavbar extends React.Component {

  render() {
    const style = {
      "backgroundColor": "#e8e8e8",
      "zIndex": "2000"
    };

    return (
      <Navbar  bg="dark" variant="dark" expand="lg" style={style}>
        <Navbar.Brand href="#home">PrestonFrazier.net</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto" defaultActiveKey="#about">
            <Nav.Link href="#about">About</Nav.Link>
            <Nav.Link href="#projects">Projects</Nav.Link>
            <Nav.Link href="#tutorials">Tutorials</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

}


export default AppNavbar;
