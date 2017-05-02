export function setUid (uid) {
  return dispatch => dispatch({type: 'SET_UID', uid});
}
export function tuneFilter (name) {
  return value => dispatch => dispatch({type: 'TUNE_FILTER', name, value});
}
export function addPhotos (photos, uid) {
  // return dispatch => post(`/user/photo?uid=${uid}`, photos)
  //   .then(() => getPageData('/search'))
}
