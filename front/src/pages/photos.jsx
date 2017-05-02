import React, { Component } from 'react';
import { connect } from 'react-redux';
import { TextArea } from 'semantic-ui-react';
  import 'semantic-ui-css/semantic.min.css';
import { addPhotos } from '../actions/user';

class Photos extends Component {
  render () {
    return <div className="page__wrap">
      <Form onSubmit={this.onSubmit}>
        <TextArea autoHeight onChange={this.onChange} value={this.state.photos.join('\n')}/>
    </div>;
  }
}
const ms2p = (state) => ({
  items: state.get('photos').get('items').filter(item => item), // todo
});
const md2a = ({onSubmit: addPhotos});
export default connect(ms2p, md2a)(Photos);
