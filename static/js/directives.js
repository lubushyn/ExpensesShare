/**
 * Created by Artem Azarov (bel-azar@ya.ru).
 * Date: 7/11/13
 * Time: 8:29 AM
 */

angular.module('expenseShareDirectives', [])
  .directive('datepicker', function () {
    return {
      restrict: 'A',
      require: '?ngModel',
      scope: {
        select: '&',
        datepicker:'@datepicker'
      },
      link: function (scope, element, attrs, ngModel) {
        attrs.$observe('datepicker', function (dateFormat) {
          if (!ngModel) {
            return;
          }

          var optionsObj = {};
          optionsObj.format = dateFormat || 'mm/dd/yy';
          var updateModel = function (dateTxt) {
            scope.$apply(function () {
              ngModel.$setViewValue(dateTxt);
            });
          };

          ngModel.$render = function () {
            element.datepicker('setValue', ngModel.$viewValue || '');
          };
          element.datepicker(optionsObj).on('changeDate', function(ev){
            var dateTxt = ev.date;
            updateModel(dateTxt);
            if (scope.select) {
              scope.$apply(function () {
                scope.select({date: dateTxt});
              });
            }
          });
        });
      }
    };
  })
  .directive('stopClick', function () {
    return function (scope, element) {
      $(element).click(function (event) {
        event.preventDefault();
      });
    }
  });
