/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 10:53 PM
 */

'use strict';

/* Services */
angular.module('expenseShareServices', ['ngResource'])
  .factory('Event', function ($resource, $rootScope) {
    return $resource($rootScope.config.basePath + '/event/:eventId', {}, {
      query: {method: 'GET', cache: true, params: {}, isArray: true},
      get: {method: 'GET', cache: true, params: {eventId:''}, isArray: false}
    });
  })
  .factory('Payment', function ($resource, $rootScope) {
    return $resource($rootScope.config.basePath + '/payment');
  });