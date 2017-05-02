import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Form, Input, Button, Label } from 'semantic-ui-react';
  import 'semantic-ui-css/semantic.min.css';
import './index.css';
import { setUid } from '../actions/user.js';

class Index extends Component {
  onSubmit = e => {
    e.preventDefault();
    localStorage.setItem('uid', this.props.uid);
  }
  onChange = e => {
    const uid = e.target.value;
    this.props.onSetUid(uid);
    localStorage.setItem('uid', uid);
  }
  render () {
    return <div className="page__wrap">
      <Form onSubmit={this.onSubmit}>
        <Label>
          <span>Your VK UserID </span>
          <Input value={this.props.uid} onChange={this.onChange} placeholder="4545454545"/>
        </Label>
        <Link to="/search">
          <Button primary>Find victims</Button>
        </Link>
      </Form>
    <div className="minor-text">Insert your vk id or link to your vk profile</div>
    </div>;
  }
}
const ms2p = (state) => ({uid: state.get('user').get('uid')});
const md2a = ({onSetUid: setUid});
export default connect(ms2p, md2a)(Index);
