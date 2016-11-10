import {Artikel} from './artikel'
import {EventAggregator} from 'aurelia-event-aggregator';
import {inject} from 'aurelia-framework';
import {WebAPI} from './web-api';

@inject(WebAPI, EventAggregator)
export class App {
  message = 'Hello World!';
  current_article = new Artikel();
  searchArticle() {
    this.api.getExternalArticle(this.current_article).then
    (article => {
      this.current_article = <Artikel>article;

    });


  }

  constructor(private api: WebAPI, private ea: EventAggregator) { }
  
}
