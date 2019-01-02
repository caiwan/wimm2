import {BaseIONode} from './_baseIO';

export class SmartImport extends BaseIONode {

  fetchAll(){
    return fetch(`${this.root}/smartimport/items`, {
      credentials: 'same-origin'
    })
    .then (v => v.json);
  }

  addFromFile(type, file) {
    const data = new FormData();
    data.append('file', file);
    data.append('type', type);

    return fetch(`${this.root}/smartimport/upload/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: this.headers,
        body: data
      })
      .then(v => v.json())
  }
}
