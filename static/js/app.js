/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:28 PM
 */

'use strict';
/* global EventsCtrl:true, EventCtrl:true, PaymentCtrl:true */
/* App Module */

angular.module('expenseShare', ['expenseShareServices', 'expenseShareDirectives'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
      when('/events', {templateUrl: '../static/js/partials/events.html', controller: EventsCtrl}).
      when('/payment/add/:eventId', {templateUrl: '../static/js/partials/add-payment.html', controller: PaymentCtrl}).
      when('/event/:eventId', {templateUrl: '../static/js/partials/event.html', controller: EventCtrl}).
      when('/upchk', {templateUrl: '../static/js/partials/upchk.html'}).
      otherwise({redirectTo: '/events'});
  }])
  .run(function ($rootScope, $location) {
    $rootScope.config =
    {
      'projectName': 'Expenses Share',
      'basePath': '',
      'dateFormat': 'dd-mm-yyyy',
      'dateFormatAngular': 'dd-MM-yyyy'
    };

    $rootScope.location = $location;
    $rootScope.$on('$locationChangeSuccess', function() {
      $location.isEvent = false;
      $location.isAddPayment = false;

      if (!!$location.path().match(/^\/event\//)){
        $location.isEvent = true;
      } else if (!!$location.path().match(/^\/payment\/add\//)) {
        $location.isAddPayment = true;
      }
    });

  });