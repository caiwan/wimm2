import {
  Items,
  Stats,
  Tags
} from './itemsIO';

import { Categories } from './categoriesIO';
import { SmartImport } from './smartimportIO';

class IO {
  constructor () {
    this.headers = null;
    this.root = '';

    this.tags = null;
    this.items = null;
    this.stats = null;
    this.smartImport = null;
    this.categories = null;

    this.initialized = fetch('./api/settings/', {
      credentials: 'same-origin'
    })
      .then(v => v.json())
      .then(data => {
        this.root = `${data.root}/api`;

        this.headers = new Headers({
          'X-CSRFToken': data.csrftoken
        });

        this.tags = new Tags(this);
        this.items = new Items(this);
        this.stats = new Stats(this);
        this.smartImport = new SmartImport(this);
        this.categories = new Categories(this);
      });
  }

  toJson (data) {
    return {
      body: new Blob([JSON.stringify(data)], {
        type: 'application/json'
      }),
      headers: this.headers
    };
  }
}

export default new IO();
