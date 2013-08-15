/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:28 PM
 */

'use strict';
/* global EventsCtrl:true, EventCtrl:true, PaymentAddCtrl:true, ReportsCtrl:true, ReportCtrl, UserCtrl:true,
  PaymentListCtrl:true */
/* App Module */

angular.module('expenseShare', ['expenseShareServices', 'expenseShareDirectives', 'chartsExample.directives'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider.
      when('/events', {templateUrl: '../static/js/partials/events.html', controller: EventsCtrl}).
      when('/payment/add/:eventId', {templateUrl: '../static/js/partials/add-payment.html',
        controller: PaymentAddCtrl}).
      when('/payment/list/:eventId', {templateUrl: '../static/js/partials/list-payment.html',
        controller: PaymentListCtrl}).
      when('/event/:eventId/addUser', {templateUrl: '../static/js/partials/add-user.html', controller: UserCtrl}).
      when('/event/:eventId', {templateUrl: '../static/js/partials/event.html', controller: EventCtrl}).
      when('/reports', {templateUrl: '../static/js/partials/reports.html', controller: ReportsCtrl}).
      when('/report/:eventId', {templateUrl: '../static/js/partials/report.html', controller: ReportCtrl}).
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

    //TODO hellfire, use controller or I kill you
    $rootScope.location = $location;
    $rootScope.$on('$locationChangeSuccess', function() {
      $location.isEvent = false;
      $location.isUpdateEvent = false;

      if (!!$location.path().match(/^\/payment\/(add|list)\//) || !!$location.path().match(/^\/event\/\w+\/addUser/)) {
        $location.isUpdateEvent = true;
      } else if (!!$location.path().match(/^\/event\//)){
        $location.isEvent = true;
      }
    });

  });