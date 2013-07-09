/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:30 PM
 */
/* exported EventsCtrl, EventCtrl */

'use strict';

/* Controllers */
function EventsCtrl($scope, Event) {
  $scope.events = Event.query();
}

function EventCtrl($scope, $routeParams, Event, Payment) {
  $scope.event = Event.get({eventId: $routeParams.eventId});

  $scope.participants = {};
  $scope.newPayment = {
    participants: [],
    payer: null,
    event_id: null,
    total: null
  };

  $scope.pay = function () {
    //TODO fix this shit
    $scope.newPayment.participants = [];
    for (var id in $scope.participants) {
      if ($scope.participants.hasOwnProperty(id)) {
        if ($scope.participants[id]) {
          $scope.newPayment.participants.push(id);
        }
      }
    }

    //set event id
    $scope.newPayment.event_id = $scope.event._id.$oid;

    if (!$scope.newPayment.participants.length) {
      alert('Select participants!!');
      return;
    }

    var payment = new Payment($scope.newPayment);
    //TODO replace alerts
    payment.$save(function () {
      alert('Success');
    }, function (data) {
      alert('Error occured: ' + data.status);
    });

    //flush total
    $scope.newPayment.total = '';
    //TODO rewrite
    $scope.event = Event.get({eventId: $routeParams.eventId});
  };

}