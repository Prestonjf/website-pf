import React from 'react';
import { Navbar, Nav, Form, FormControl } from 'react-bootstrap';
import {Link} from "react-router-dom";
import logo from '../../img/preston192x192.png';
import { SocialIcon } from 'react-social-icons';

class AppNavbar extends React.Component {

  render() {
    const style = {
      "backgroundColor": "#e8e8e8",
      "zIndex": "2000"
    };

    const altNavStyle = {
      "backgroundColor": "#ddffaa",
      "zIndex": "3000",
      "color": "#000000",
      "textAlign": "center"
    };

    const searchBoxStyle = {
      "fontWeight": "bold",
      "color": "#343a40"
    };

    const linkStyle = {
      "textDecoration": "none",
      "color": "#ddffaa"
    };

    return (
      <div>
      <Navbar  bg="dark" variant="dark" expand="lg" style={style}>
        <Navbar.Brand >
        <Link to="/" style={linkStyle}>
        <img alt="prestonlogo" src={logo} height="30" wdith="30"/>&nbsp;prestonfrazier.net
        </Link>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Form inline>
              <FormControl type="text" placeholder="Search" size="sm" style={searchBoxStyle}/>
            </Form>
            <Nav.Item className="nav-link">
              <Link style={linkStyle}  to="/tags"><b>Tags</b></Link>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <Link style={linkStyle}  to="/post"><b>About</b></Link>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <SocialIcon url="https://github.com/Prestonjf" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <SocialIcon url="https://www.linkedin.com/in/preston-frazier/" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <SocialIcon url="/rss.xml" network="rss" style={{ height: 25, width: 25 }} bgColor="#ddffaa" target="_blank"/>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
        <br />
      </Navbar>

      <Navbar style={altNavStyle}>
        <Nav className="mx-auto">
          <div>#BlackLivesMatter</div>
        </Nav>
      </Navbar>
    </div>
    );
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

}


export default AppNavbar;
