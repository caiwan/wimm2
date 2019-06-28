import { BaseIONode } from './_baseIO';

const AUTOCOMPLETE_LIMIT = 10;

export class Stats extends BaseIONode {
  totalSum ({
    dateFrom,
    dateTo,
    interval
  }) {
    return fetch(`${this.root}/total_sum/?from=${dateFrom}&to=${dateTo}&interval=${interval}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  tagSumOverTime ({
    dateFrom,
    dateTo,
    interval,
    tags,
    baseTag,
    noBase
  }) {
    const params = new URLSearchParams();

    params.append('from', dateFrom);
    params.append('to', dateTo);
    params.append('interval', interval);
    params.append('base_tag', baseTag);
    params.append('no_base', noBase);

    for (let tag of tags) {
      params.append('tags', tag);
    }

    return fetch(`${this.root}/tag_sum_over_time/?${params}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  tagSum ({
    dateFrom,
    dateTo,
    tagCount,
    negativeFirst,
    tags = []
  }) {
    const params = new URLSearchParams();

    params.append('from', dateFrom);
    params.append('to', dateTo);
    params.append('tagCount', tagCount);
    params.append('negativeFirst', Number(negativeFirst));

    for (let tag of tags) {
      params.append('tags', tag);
    }

    return fetch(`${this.root}/tag_sum/?${params}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }
}

export class Items extends BaseIONode {
  fetchMonth ({
    year,
    month
  }) {
    return fetch(`${this.root}/items/?year=${year}&month=${month}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json())
      .then(data => {
        data.forEach(date => {
          date.items.forEach(item => {
            item.date = date.date;
          });
        });

        return data;
      });
  }

  fetchRange ({
    dateFrom,
    dateTo
  }) {
    return fetch(`${this.root}/items/?from=${dateFrom}&to=${dateTo}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  add (item) {
    if (item) {
      return fetch(`${this.root}/items/`, {
        method: 'POST',
        credentials: 'same-origin',
        ...this.io.toJson(item)
      })
        .then(v => v.json())
        .then(data => {
          // data.item = data;
          return { 'item': data };
        });
    } else {
      return Promise.resolve();
    }
  }

  addFromFile (file) {
    const data = new FormData();
    data.append('file', file);

    return fetch(`${this.root}/items/upload/`, {
      method: 'POST',
      credentials: 'same-origin',
      headers: this.headers,
      body: data
    })
      .then(v => v.json());
  }

  remove (items) {
    if (items.length) {
      return fetch(`${this.root}/items/`, {
        method: 'DELETE',
        credentials: 'same-origin',
        ...this.io.toJson({
          'items': items
        })
      })
        .then(v => v.json());
    } else {
      return Promise.resolve();
    }
  }

  edit (item) {
    return fetch(`${this.root}/items/${item.id}/`, {
      method: 'PATCH',
      credentials: 'same-origin',
      ...this.io.toJson(item)
    })
      .then(v => v.json());
  }
}

export class Tags extends BaseIONode {
  fetchAll () {
    return fetch(`${this.root}/autocomplete/`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }

  autocomplete (term) {
    return fetch(`${this.root}/autocomplete/?q=${term}&l=${AUTOCOMPLETE_LIMIT}`, {
      credentials: 'same-origin'
    })
      .then(v => v.json());
  }
}
