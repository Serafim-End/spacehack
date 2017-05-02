import { get, errorProcessor } from '../utils';
const getReducerName = path => path.split('/')[1];
const processError = errorProcessor('pages');
const REDUCER_NAMES = [
  'victims',
  'events',
  'user',
];
const NOPE = { type: 'NOPE' };

export function getPageData ({path, params}) {
  return dispatch => {
    const reducerName = getReducerName(path);

    if (!reducerName || !REDUCER_NAMES.includes(reducerName)) {
      dispatch(NOPE);
      return;
    }

    get(`/${reducerName}`)
    .then(({items}) => dispatch({
      type: `REPLACE_${reducerName.toUpperCase()}`,
      items
    }))
    .catch(processError);

    dispatch({ type: `PENDING_REPLACE_${reducerName.toUpperCase()}` });
  };
}
