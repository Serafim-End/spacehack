import React from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import { Provider } from 'react-redux';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { Map, List, Record } from 'immutable';
import { backDomain, makeRecord } from './utils';

import Store from './store';
import App from './app';
import './index.css';

/* eslint-disable */
const store = Store(Map({
  victims: Map({items: List(require('../data/victims.sample.json').map(item => makeRecord(item)))}),
  events: Map({items: List([])}),
  user: makeRecord({uid: localStorage['uid'] || '', filters: makeRecord({readiness: 50, face: 50, similarity: 50})}),
}));
/* eslint-enable */

const Root = ({store}) => {
  return <Provider {...{store}}>
    <Router>
      <Route path="/" component={App} />
    </Router>
  </Provider>;
};

Root.propTypes = {
  store: PropTypes.object.isRequired,
};

ReactDOM.render(
  <Root {...{store}}/>,
  document.getElementById('root')
);
