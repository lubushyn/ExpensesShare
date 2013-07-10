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

function EventCtrl($scope, $routeParams, Event) {
  $scope.event = Event.get({eventId: $routeParams.eventId});

  $scope.participants = {};
  $scope.newPayment = {
    participants: [],
    payer: null,
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


    if (!$scope.newPayment.participants.length) {
      alert('Select participants!!');
      return;
    }

    console.log($scope.newPayment);


    //TODO replace alerts
    Event.patch({eventId: $routeParams.eventId},
      $scope.newPayment,
      function () {
        alert('Success');
        //flush total
        $scope.newPayment.total = '';
        $scope.newPayment.name = '';

        //TODO rewrite
        $scope.event = Event.get({eventId: $routeParams.eventId});
      }, function (data) {
        alert('Error occured: ' + data.status);
      });


  };

}