import { BaseIONode } from './_baseIO'

export class Categories extends BaseIONode {
  constructor(io) {
    super(io)
  }

  fetchAll() {
    return fetch(`${this.root}/categories/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  add(item) {
    return fetch(`${this.root}/categories/`, {
      method: 'POST',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    })
      .then(v => v.json());
  }

  edit(item) {
    return fetch(`${this.root}/categories/${item.id}/`, {
      method: 'PUT',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    })
      .then(v => v.json());
  }

  remove(item) {
    return fetch(`${this.root}/categories/${item.id}/`, {
      method: 'DELETE',
      credentials: 'same-origin',
    })
  }

  /// 
  addFromFile(file) {
    const data = new FormData();
    data.append('file', file);

    return fetch(`${this.root}/categories/upload/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: this.headers,
      body: data
    })
      .then(v => v.json())
  }
}

