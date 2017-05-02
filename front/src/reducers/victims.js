import { List } from 'immutable';
import { makeRecord } from '../utils';
export default function (state, action) {
  switch (action.type) {
  // case('REPLACE_VICTIMS'): return state.set('items', List(action.items.map(item => makeRecord(item))));
  default: return state;
  }
}
