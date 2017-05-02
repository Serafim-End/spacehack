import { createStore, applyMiddleware, compose } from 'redux';
import thunk from 'redux-thunk';

import rootReducer from  './reducers';

let enhancers = [applyMiddleware(thunk)];
if (window.__REDUX_DEVTOOLS_EXTENSION__) {
  enhancers.push(window.__REDUX_DEVTOOLS_EXTENSION__());
}

export default(initialState) => {
  return createStore(rootReducer, initialState, compose(...enhancers));
};
