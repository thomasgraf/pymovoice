define('artikel',["require", "exports"], function (require, exports) {
    "use strict";
    var Artikel = (function () {
        function Artikel() {
            this.done = false;
            this.detailname = 'Name';
            this.eancode = 'EAN';
            this.stockquantity = 0;
        }
        return Artikel;
    }());
    exports.Artikel = Artikel;
});

define('web-api',["require", "exports", 'aurelia-fetch-client'], function (require, exports, aurelia_fetch_client_1) {
    "use strict";
    var client = new aurelia_fetch_client_1.HttpClient();
    var WebAPI = (function () {
        function WebAPI() {
        }
        WebAPI.prototype.getExternalArticle = function (article) {
            return new Promise(function (resolve) {
                client.fetch('/api/v1/external_article/' + article.eancode + '.json')
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                    resolve(data);
                });
            });
        };
        return WebAPI;
    }());
    exports.WebAPI = WebAPI;
});

var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
define('app',["require", "exports", './artikel', 'aurelia-event-aggregator', 'aurelia-framework', './web-api'], function (require, exports, artikel_1, aurelia_event_aggregator_1, aurelia_framework_1, web_api_1) {
    "use strict";
    var App = (function () {
        function App(api, ea) {
            this.api = api;
            this.ea = ea;
            this.message = 'Hello World!';
            this.current_article = new artikel_1.Artikel();
        }
        App.prototype.searchArticle = function () {
            var _this = this;
            this.api.getExternalArticle(this.current_article).then(function (article) {
                _this.current_article = article;
            });
        };
        App = __decorate([
            aurelia_framework_1.inject(web_api_1.WebAPI, aurelia_event_aggregator_1.EventAggregator), 
            __metadata('design:paramtypes', [web_api_1.WebAPI, aurelia_event_aggregator_1.EventAggregator])
        ], App);
        return App;
    }());
    exports.App = App;
});

define('environment',["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    exports.default = {
        debug: true,
        testing: true
    };
});

define('main',["require", "exports", './environment'], function (require, exports, environment_1) {
    "use strict";
    Promise.config({
        warnings: {
            wForgottenReturn: false
        }
    });
    function configure(aurelia) {
        aurelia.use
            .standardConfiguration()
            .feature('resources');
        if (environment_1.default.debug) {
            aurelia.use.developmentLogging();
        }
        if (environment_1.default.testing) {
            aurelia.use.plugin('aurelia-testing');
        }
        aurelia.start().then(function () { return aurelia.setRoot(); });
    }
    exports.configure = configure;
});

define('resources/index',["require", "exports"], function (require, exports) {
    "use strict";
    function configure(config) {
    }
    exports.configure = configure;
});

define('text!app.html', ['module'], function(module) { module.exports = "<template>\n     <require from=\"bootstrap/css/bootstrap.css\"></require>\n  <h1>${message}</h1>\n\n  <form submit.trigger=\"searchArticle()\">\n    <input type=\"text\" value.bind=\"current_article.eancode\">\n    <button type=\"submit\">search article</button>\n  </form>\n\n\n  <form submit.trigger=\"addArticle()\">\n    <input type=\"text\" value.bind=\"current_article.eancode\">\n    <input type=\"text\" value.bind=\"current_article.detailname\">\n    <input type=\"text\" value.bind=\"current_article.stockquantity\">\n    <button type=\"submit\">add article</button>\n  </form>\n\n</template>\n"; });
//# sourceMappingURL=app-bundle.js.map