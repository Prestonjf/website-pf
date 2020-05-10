import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import logo from '../../img/preston192x192.png';

class AppNavbar extends React.Component {

  render() {
    const style = {
      "backgroundColor": "#e8e8e8",
      "zIndex": "2000"
    };

    return (
      <Navbar  bg="dark" variant="dark" expand="lg" style={style}>
        <Navbar.Brand href="#home">
        <img alt="prestonlogo" src={logo} height="30" wdith="30"/>&nbsp;prestonfrazier.net</Navbar.Brand>
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
