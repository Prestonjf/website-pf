import React from 'react';
import BurgerMenu from 'react-burger-menu';


class AppSideBar extends React.Component {

  constructor (props) {
    super(props);
    this.state = {
      currentMenu: 'push',
      side: 'left'
    };
  }

  render () {
    var styles = {
      bmBurgerButton: {
        position: 'fixed',
        width: '36px',
        height: '30px',
        left: '36px',
        top: '36px',
        marginTop: '30px'
      },
      bmBurgerBars: {
        background: '#373a47'
      },
      bmBurgerBarsHover: {
        background: '#a90000'
      },
      bmCrossButton: {
        height: '24px',
        width: '24px'
      },
      bmCross: {
        background: '#bdc3c7'
      },
      bmMenuWrap: {
        position: 'fixed',
        height: '100%',
        width: 'auto'
      },
      bmMenu: {
        background: '#f7f7f7',
        padding: '2.5em 1.5em 0',
        fontSize: '1.15em'
      },
      bmMorphShape: {
        fill: '#373a47'
      },
      bmItemList: {
        color: '#b8b7ad',
        padding: '0.8em'
      },
      bmItem: {
        display: 'inline-block'
      },
      bmOverlay: {
        background: 'rgba(0, 0, 0, 0.3)'
      }
    }
    // NOTE: You also need to provide styles, see https://github.com/negomi/react-burger-menu#styling
    const Menu = BurgerMenu["push"];

    return (
      <Menu pageWrapId= "content" outerContainerId="sidebarContainer" styles={ styles } isOpen={ true } noOverlay disableOverlayClick>
        <a id="home" className="menu-item" href="#">Home</a>
        <a id="about" className="menu-item" href="#">About</a>
        <a id="contact" className="menu-item" href="#">Contact</a>
      </Menu>
    );
  }

}


export default AppSideBar;
