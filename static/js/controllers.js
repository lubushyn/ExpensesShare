/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/7/13
 * Time: 8:30 PM
 */
/* exported EventsCtrl, PaymentAddCtrl, EventCtrl, ReportsCtrl, ReportCtrl, UserCtrl, PaymentListCtrl */

'use strict';

/* Controllers */
function EventsCtrl($scope, Event) {
  $scope.events = Event.query();
}

function UserCtrl($rootScope, $scope, $routeParams, User, Event) {
  //TODO research how to implement it in proper way - lol, use controller, Luke!
  $rootScope.eventId = $routeParams.eventId;

  $scope.newUser = {};

  $scope.addUser = function () {
    if (!$scope.newUser.name) {
      alert('User must have name. Sorry about that');
      return;
    }

    User.add({},
      $scope.newUser,
      function (data) {
        var newId = data.$oid;
        //flush all
        console.log('New id: ' + newId);

        Event.addParticipant(
          {eventId: $routeParams.eventId},
          {"id": newId},
          function () {
            $scope.newUser = {};
            alert('User added! Nothing special');
          },
          function (data) {
            alert('Error occurred: ' + data.status);
          });

      }, function (data) {
        alert('Error occurred: ' + data.status);
      });
  };
}

function PaymentListCtrl($rootScope, $scope, $routeParams, Event) {
  //TODO research how to implement it in proper way - lol, use controller, Luke!
  $rootScope.eventId = $routeParams.eventId;
  $scope.event = Event.get({eventId: $routeParams.eventId});
}

function PaymentAddCtrl($rootScope, $scope, $routeParams, Event) {
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

function EventCtrl($rootScope, $scope, $routeParams, Event, User, $location) {
  $rootScope.eventId = $routeParams.eventId;
  $scope.event = Event.get({eventId: $routeParams.eventId, limit: 15});
//  $scope.me = User.me();
  $scope.allPayments = function () {
    $location.path('/payment/list/' + $routeParams.eventId);
  };
}

function ReportsCtrl($scope, Event) {
  $scope.events = Event.query();
}

function ReportCtrl($scope, $routeParams, Event, Report) {
  var dEvent = new $.Deferred();

  $scope.reports = [];
  $scope.event = Event.get({eventId: $routeParams.eventId}, function () {
    dEvent.resolve();
  });

  $scope.defaultChart = {
    "title": {
      "text": "Dummy title"
    },
    "subtitle": {
      "text": "Dummy subtitle"
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
    xAxis: {
      type: 'category'
    },
    "series": [
      {
        "name": "Dummy series",
        "data": []
      }
    ]
  };

  dEvent.done(function () {
    //general report
    Report.get({eventId: $routeParams.eventId}, function (data) {
      var _data = [],
        total = 0;
      data.forEach(function (item) {
        //TODO gavnocode.ru (facepalm)
        _data.push([item._id.match(/[-\d]+/)[0], item.total]);
        total += item.total;
      });
//      console.log(_data);

      $scope.basicAreaChart = $.extend({}, $scope.defaultChart, {});
      $scope.basicAreaChart.title.text = $scope.event.name + ' ['+total+'$]';
      $scope.basicAreaChart.subtitle.text = "Participants: " +
        $scope.event.participants.map(function (data) {
          return data.name;
        }).reduce(function (result, data) {
            return result += data + ", ";
          });
      $scope.basicAreaChart.series = [
        {
          "name": "Expenses",
          "data": _data
        }
      ];
    });

    //report per participant
    $scope.event.participants.forEach(function (participant) {
      Report.getByParticipantId({eventId: $routeParams.eventId, participantId: participant.id}, function (data) {
        console.log(data);
        var _data = [],
          total = 0;
        data.forEach(function (item) {
          //TODO gavnocode.ru (facepalm)
          _data.push([item._id.match(/[-\d]+/)[0], item.total]);
          total += item.total;
        });
        var newChart = $.extend({}, $scope.defaultChart, {});
        newChart.title.text = $scope.event.name + ' ['+total.toFixed(2)+'$]';
        newChart.subtitle.text = "Participant: " + participant.name;
        newChart.series = [
          {
            "name": "Expenses",
            "data": _data
          }
        ];
        $scope.reports.push(newChart);
      });
    });

  });
}