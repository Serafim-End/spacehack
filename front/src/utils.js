import { Record } from 'immutable';

export function getPageName () {
  return this.context.router.route.location.pathname.replace(/^\/|\d/g, '').replace(/\/$/, '').replace(/\//g, '-').replace(/\/$/, '') || 'index';
}

export function leftpad (width, str, char = '0') {
  const str_ = str.toString();
  const padLen = width - str_.length;
  return char.repeat(padLen > 0 ? padLen : 0) + str_;
}

/* eslint-disable */
export const backDomain = atob(require('../.back').split(',')[1]).trim();
/* eslint-enable */

export function get (path, opts) {
  return fetch(backDomain + '/admin' + path, opts).then(data => data.json());
}

export function post (path, opts) {
  return get(path, {...opts, method: 'POST'});
}

export function errorProcessor (reducer) {
  /* eslint-disable */
  return e => console.log(reducer + ' error', e);
  /* eslint-enable */
}

export function makeRecord (obj) {
  return Record(obj)(obj);
}
