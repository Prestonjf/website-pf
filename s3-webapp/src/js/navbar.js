import React from 'react';
import { withRouter } from 'react-router';
import { Navbar, Nav, Form, FormControl } from 'react-bootstrap';
import {Link} from "react-router-dom";
import logo from '../img/preston192x192.png';
import { SocialIcon } from 'react-social-icons';

class AppNavbar extends React.Component {
  
  constructor(props) {
    super();
    this.state = {searchValue: '', expanded: false};
    this.handleSearchChange = this.handleSearchChange.bind(this);
    this.setExpanded = this.setExpanded.bind(this);
  }

  render() {
    const expanded = this.state.expanded;

    return (
      <div>
      <Navbar bg="dark" variant="dark" expand="lg" className="main-navbar" expanded={expanded}>
        <Navbar.Brand >
        <Link to="/" className="main-link-style">
        <img alt="prestonfraziernetlogo" src={logo} height="30" wdith="30"/>&nbsp;prestonfrazier.net
        </Link>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" onClick={() => this.setExpanded(expanded ? false : "expanded")}  className="ml-auto" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Form inline onSubmit={this.submitSearchForm.bind(this)} >
              <FormControl type="text" placeholder="Search..." size="sm" value={this.state.searchValue} onChange={this.handleSearchChange} />
            </Form>
            <Nav.Item className="nav-link">
              <Link className="main-link-style" to="/tags" onClick={() => this.setExpanded(false)}><b>Tags</b></Link>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <Link className="main-link-style" to="/post/portfolio" onClick={() => this.setExpanded(false)}><b>Portfolio</b></Link>
            </Nav.Item>
            <Nav.Item className="nav-link">
              <Link className="main-link-style"  to="/post/about" onClick={() => this.setExpanded(false)}><b>About</b></Link>
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

      <Navbar className="secondary-navbar">
        <Nav className="mx-auto">
          <div className="main-link-style-dark">#BlackLivesMatter</div>
        </Nav>
      </Navbar>
    </div>
    );
  }

  handleSearchChange(e) {
    this.setState({searchValue: e.target.value});
  }

  setExpanded(value) {
    this.setState({expanded: value});
  } 

  submitSearchForm(e) {
    const value = encodeURIComponent(this.state.searchValue);
    this.setState({searchValue: "", expanded: false});
    this.props.history.push("/search?d=" + Date.now() + "&q=" + value);
    e.preventDefault();
  }

  componentDidMount() {

  }

}


export default withRouter(AppNavbar);
