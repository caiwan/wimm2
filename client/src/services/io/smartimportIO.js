import { BaseIONode } from './_baseIO';

export class SmartImport extends BaseIONode {

  fetchAll() {
    return fetch(`${this.root}/smartimport/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
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

  saveItem(item, storedItem) {
    return fetch(`${this.root}/smartimport/${item.id}/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: this.headers,
      ...this.io.toJson(storedItem)
    })
      .then(v => v.json());
  }

  deleteItem(item) {
    return fetch(`${this.root}/smartimport/${item.id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
      headers: this.headers,
    })
  }

}
