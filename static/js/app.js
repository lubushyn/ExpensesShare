/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:28 PM
 */

'use strict';
/* global EventsCtrl:true, EventCtrl:true */
/* App Module */

angular.module('expenseShare', ['expenseShareServices', 'expenseShareDirectives'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
      when('/events', {templateUrl: '../static/js/partials/events.html', controller: EventsCtrl}).
      when('/event/:eventId', {templateUrl: '../static/js/partials/event.html', controller: EventCtrl}).
      when('/upchk', {templateUrl: '../static/js/partials/upchk.html'}).
      otherwise({redirectTo: '/events'});
  }])
  .run(function ($rootScope) {
    $rootScope.config =
    {
      'projectName': 'Expenses Share',
      'basePath': '',
      'dateFormat': 'dd-mm-yyyy',
      'dateFormatAngular': 'dd-MM-yyyy'
    };
  });