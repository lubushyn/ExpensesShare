/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 10:53 PM
 */

'use strict';

/* Services */
angular.module('expenseShareServices', ['ngResource'])
  .factory('Event', function ($resource, $rootScope) {
    var Event = $resource($rootScope.config.basePath + 'event/:eventId', {}, {
      query: {method: 'GET', cache: true, params: {}, isArray: true},
      get: {method: 'GET', cache: false, params: {eventId: '', limit: ''}, isArray: false,
        url:$rootScope.config.basePath + 'event/:eventId/:limit'},
      patch: {method: 'PATCH', params: {eventId: ''}},
      addParticipant: {method: 'PATCH', params: {eventId: ''}, url:$rootScope.config.basePath + 'event/:eventId/user'}
    });

    Event.prototype.getParticipantById = function (id) {
      //TODO rewrite into map
      for (var index in this.participants) {
        if (this.participants.hasOwnProperty(index)) {
          var participant = this.participants[index];
          if (participant.id === id) {
            return participant;
          }
        }
      }
    };

    return Event;
  })
  .factory('User', function ($resource, $rootScope, $http) {
    return  $resource($rootScope.config.basePath + 'user/', {}, {
      me: {
        url: $rootScope.config.basePath + 'user/me',
        method: 'GET',
        cache: true,
        params: {},
        transformResponse: $http.defaults.transformResponse.concat([
          function (data) {
            data.id = data._id.$oid;
            return data;
          }
        ])
      },
      add: {
        method: 'POST',
        params:{},
        isArray:false
      }
    });
  })
  .factory('Report', function ($resource, $rootScope) {
    return $resource($rootScope.config.basePath + 'report/:eventId', {}, {
      get: {method: 'GET', cache: true, params: {eventId: ''}, isArray: true},
      getByParticipantId: {
        method: 'GET',
        cache: true,
        params: {eventId: '', participantId: ''},
        url: $rootScope.config.basePath + 'report/:eventId/:participantId',
        isArray: true
      }
    });
  });




