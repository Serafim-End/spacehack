import { List } from 'immutable';
export default function (state, action) {
  switch (action.type) {
  case('SET_UID'): return state.set('uid', action.uid);
  case('TUNE_FILTER'): return state.updateIn(['filters', action.name], () => action.value);
  default: return state;
  }
}
