import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import {Link} from "react-router-dom";
import logo from '../../img/preston192x192.png';

import '../../css/app.css';

class CommonModal extends React.Component {

  constructor(props){
       super();
       this.state = {
          type : props.type,
          showHide : false
       }
       this.cookiePreferenceOnChange = this.cookiePreferenceOnChange.bind(this);
   }

   handleModalShowHide(e) {
       this.setState({ showHide: !this.state.showHide,
         sessionAccepted :  (localStorage.getItem('cookie-consent-session-accepted') === 'true') ? true : false,
         persistantAccepted :  (localStorage.getItem('cookie-consent-persistant-accepted') === 'true') ? true : false
        });
       if (e) e.preventDefault();
   }

   render() {
     if ('cookiepreferences' === this.state.type) return this.loadCookiePreferencesModal();
     else return null;
   }

   loadCookiePreferencesModal() {
     return(
       <span>
         <Link className="small defaultLinkStyle" to="/" onClick={e => this.handleModalShowHide(e)}>Cookie Preferences</Link>
           <Modal show={this.state.showHide} onHide={() => this.handleModalShowHide()} aria-labelledby="contained-modal-title-vcenter" centered>
               <Modal.Header className="defaultPageStyle" closeButton onClick={() => this.handleModalShowHide()}>
               <Modal.Title><img alt="prestonfraziernetlogo" src={logo} height="30" wdith="30"/> Cookie Preferences</Modal.Title>
               </Modal.Header>
               <Modal.Body>
               <Form>
                 <Form.Check disabled type="switch" checked id="cookie-consent-essential-accepted" label="Essential Cookies" />
                 <Form.Check type="switch" checked={this.state.sessionAccepted} id="cookie-consent-session-accepted" onChange={e => this.cookiePreferenceOnChange(e)} label="Session Cookies"/>
                 <Form.Check type="switch" checked={this.state.persistantAccepted} id="cookie-consent-persistant-accepted" onChange={e => this.cookiePreferenceOnChange(e)} label="Persistant Cookies" />
               </Form>


               </Modal.Body>
               <Modal.Footer>
               <Button size="sm" style={{ backgroundColor: "#343a40", borderColor: "#343a40"}} onClick={() => this.handleModalShowHide()}>
                   OK
               </Button>
               </Modal.Footer>
           </Modal>
           </span>
     )
   }

   cookiePreferenceOnChange(e) {
     localStorage.setItem(e.target.id, e.target.checked);
     this.setState({
       sessionAccepted :  (localStorage.getItem('cookie-consent-session-accepted') === 'true') ? true : false,
       persistantAccepted :  (localStorage.getItem('cookie-consent-persistant-accepted') === 'true') ? true : false
    });
   }

}

export default CommonModal;
