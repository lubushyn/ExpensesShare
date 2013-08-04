/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 10:53 PM
 */

'use strict';

/* Services */
angular.module('expenseShareServices', ['ngResource'])
  .factory('Event', function ($resource, $rootScope) {
    var Event =  $resource($rootScope.config.basePath + 'event/:eventId', {}, {
      query: {method: 'GET', cache: true, params: {}, isArray: true},
      get: {method: 'GET', cache: false, params: {eventId:''}, isArray: false},
      patch: {method: 'PATCH', params: {eventId:''}}
    });

    Event.prototype.getParticipantById = function (id){
      //TODO rewrite into map
      for (var index in this.participants){
        if (this.participants.hasOwnProperty(index)){
          var participant = this.participants[index];
          if (participant.id === id){
            return participant;
          }
        }
      }
    };

    return Event;
  })
  .factory('User', function ($resource, $rootScope, $http) {
    return  $resource($rootScope.config.basePath + 'user/me', {}, {
      me: {
        method: 'GET',
        cache: true,
        params: {},
        transformResponse: $http.defaults.transformResponse.concat([
          function (data) {
            data.id = data._id.$oid;
            return data;
          }
        ])
      }
    });
  });




