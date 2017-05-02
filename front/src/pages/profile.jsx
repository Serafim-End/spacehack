import React, { Component } from 'react';
import { connect } from 'react-redux';

class Profile extends Component {
  render () {
    return <div>profile</div>;
  }
}
const ms2p = (state, ownProps) => ({
  items: state.get('victims').get('items').get(ownProps.victimId), // todo
});
const md2a = ({});
export default connect(ms2p, md2a)(Profile);
