import { combineReducers } from 'redux-immutable';
import victims from './victims';
import events from './events';
import user from './user';

const rootReducer = combineReducers({
  victims,
  events,
  user,
});

export default rootReducer;
