import "whatwg-fetch";
import config from "./config";
import { v4 as uuidv4 } from 'uuid';

const fetch = window.fetch;

export default (url, options, traced = false) => {
  if (options === undefined) {
    options = {
      method: "GET",
      credentials: "same-origin",
      headers: {},
    };
  }
  url = config.urlRoot + url;

  if (options.headers === undefined) {
    options.headers = {};
  }
  options.credentials = "same-origin";
  options.headers["Accept"] = "application/json";
  options.headers["Content-Type"] = "application/json";
  options.headers["CSRF-Token"] = config.csrfNonce;
  if(traced) {
    options.headers["X-Trace-ID"] = uuidv4();
  }
  return fetch(url, options);
};
