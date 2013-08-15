/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:30 PM
 */
/* exported EventsCtrl, PaymentCtrl, EventCtrl, ReportsCtrl, ReportCtrl */

'use strict';

/* Controllers */
function EventsCtrl($scope, Event) {
  $scope.events = Event.query();
}

function PaymentCtrl($rootScope, $scope, $routeParams, Event) {
  //TODO research how to implement it in proper way - lol, use controller, Luke!
  $rootScope.eventId = $routeParams.eventId;

  var currentDate = new Date();
  var _defaultPayment = {
    participants: [],
    payer: null,
    total: null,
    date: new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate(), 0, 0, 0, 0)
  };

  $scope.event = Event.get({eventId: $routeParams.eventId});

  $scope.participants = {};
  $scope.newPayment = $.extend({}, {}, _defaultPayment);

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

    //total should be float
    $scope.newPayment.total = parseFloat($scope.newPayment.total);

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
        //flush all
        $scope.newPayment = $.extend({}, {}, _defaultPayment);
        $scope.participants = {};

        //TODO rewrite
        $scope.event = Event.get({eventId: $routeParams.eventId});
      }, function (data) {
        alert('Error occurred: ' + data.status);
      });
  };

  $scope.$watch('newPayment.total', function () {
    var floatValue = parseFloat($scope.newPayment.total);
    //TODO rewrite with regex - just ignore non number or dot
    if (($scope.newPayment.total <= 0 || isNaN(floatValue)) && $scope.newPayment.total !== '') {
      $scope.newPayment.total = '';
    }
  });
}

function EventCtrl($rootScope, $scope, $routeParams, Event, User) {
  $rootScope.eventId = $routeParams.eventId;
  $scope.event = Event.get({eventId: $routeParams.eventId});
//  $scope.me = User.me();
}

function ReportsCtrl($scope, Event) {
  $scope.events = Event.query();
}

function ReportCtrl($scope, $routeParams, Event, Report) {
  var dEvent = new $.Deferred(),
    dReport = new $.Deferred();
  $scope.event = Event.get({eventId: $routeParams.eventId}, function () {
    dEvent.resolve();
  });
  $scope.report = Report.get({eventId: $routeParams.eventId}, function () {
    dReport.resolve();
  });

  $.when.apply(null, [dEvent, dReport]).then(function () {
    var _data = [];
    $scope.report.forEach(function(item){
      _data.push([item._id, item.total]);
    });
    console.log(_data);

    $scope.basicAreaChart = {
      "title": {
        "text": $scope.event.name
      },
      "subtitle": {
        "text": "Participants: " +
          $scope.event.participants.map(function (data) {
            return data.name;
          }).reduce(function (result, data) {
            return result += data + ", ";
          })
      },

      "tooltip": {},
      "plotOptions": {
        "area": {
          "pointStart": 0,
          "marker": {
            "enabled": false,
            "symbol": "circle",
            "radius": 2,
            "states": {
              "hover": {
                "enabled": true
              }
            }
          }
        }
      },
      "series": [
        {
          "name": "Expenses",
          "data": _data
        }
      ]
    };
  }, 1000);

}