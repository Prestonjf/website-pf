import React from 'react';
import { Container, Row, Col,  } from 'react-bootstrap';


class CommonPost extends React.Component {

  constructor(props) {
    super(props);
    this.state = {content: ''};
    this.getCommonPost = this.getCommonPost.bind(this);
  }

  render() {

    const style = {
      "textAlign":"left"
    };

    return (
      <div className="post">
      <Container>
      <Row>
      <Col sm={0} md={1}></Col>
      <Col sm={12} md={10} style={style}>
        <div id="postContent" dangerouslySetInnerHTML={{__html: this.state.content}} />

      </Col>
      </Row>
    </Container>
      </div>
    );
  }

  getCommonPost() {
    fetch(process.env.PUBLIC_URL+'/privacypolicy.html')
    .then((resp)=>{ return resp.text() })
    .then((text)=>{
      this.setState({content: text });
      if (window.location.href.includes('#cookies')) {
        document.getElementById('cookies').scrollIntoView();
      }
    });
  }

  componentDidMount() {
    this.getCommonPost();

  }

  componentWillUnmount() {

  }

}


export default CommonPost;
