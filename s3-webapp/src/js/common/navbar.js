import React from 'react';
import { Navbar, Nav, Form, FormControl } from 'react-bootstrap';
import logo from '../../img/preston192x192.png';
import { SocialIcon } from 'react-social-icons';

class AppNavbar extends React.Component {

  render() {
    const style = {
      "backgroundColor": "#e8e8e8",
      "zIndex": "2000"
    };

    return (
      <Navbar  bg="dark" variant="dark" expand="lg" style={style}>
        <Navbar.Brand href="https://prestonfrazier.net">
        <img alt="prestonlogo" src={logo} height="30" wdith="30"/>&nbsp;prestonfrazier.net</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Form inline>
              <FormControl type="text" placeholder="Search" className="mr-sm-2" />
            </Form>
            <Nav.Link href="#tags">Tags</Nav.Link>
            <Nav.Link href="#about">About</Nav.Link>
            <Form inline>
              <SocialIcon url="https://github.com/Prestonjf" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>&nbsp;
              <SocialIcon url="https://twitter.com/prestonfrazier" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
            </Form>
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
