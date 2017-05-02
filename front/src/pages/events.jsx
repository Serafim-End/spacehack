import React, { Component } from 'react';
import { connect } from 'react-redux';

class Events extends Component {
  render () {
    return <div>profile</div>;
  }
}
const ms2p = (state) => ({
  items: state.get('events').get('items').filter(item => item), // todo
});
const md2a = ({});
export default connect(ms2p, md2a)(Events);
