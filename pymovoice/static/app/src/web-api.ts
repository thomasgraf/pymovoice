/**
 * Created by tgraf on 06.11.16.
 */

import {HttpClient} from 'aurelia-fetch-client';

let client = new HttpClient();

export class WebAPI {
  getExternalArticle(article){
    return new Promise(resolve => {
      client.fetch('/api/v1/external_article/'+article.eancode+'.json')
        .then(response => response.json())
        .then(data => {
          resolve(data);
        });
    });
  }
}
