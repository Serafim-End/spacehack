import { List } from 'immutable';
export default function (state, action) {
  switch (action.type) {
  case('REPLACE_EVENTS'): return state.set('items', List(action.items));
  default: return state;
  }
}
