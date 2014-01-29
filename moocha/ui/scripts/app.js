// Generated by CoffeeScript 1.6.3
var controllers, notify;

notify = angular.module('notify', ['ngRoute', 'controllers']);

notify.config([
  '$routeProvider', function($routeProvider) {
    return $routeProvider.when('/', {
      templateUrl: 'partials/index.html',
      controller: 'HomePageCtrl'
    }).when('/admin', {
      templateUrl: 'partials/admin/index.html',
      controller: 'AdminCtrl'
    }).when('/admin/sent-emails/:id', {
      templateUrl: 'partials/admin/sent-emails/list.html',
      controller: 'AdminCtrl'
    }).when('/admin/advertisements/', {
      templateUrl: 'partials/admin/advertisements/list.html',
      controller: 'AdvertisementCtrl'
    }).otherwise({
      redirectTo: '/'
    });
  }
]);

controllers = angular.module('controllers', []);

controllers.controller('HomePageCtrl', [
  '$scope', '$http', function($scope, $http) {
    $scope.input = {
      category: '',
      query: ''
    };
    $http({
      method: 'GET',
      url: '/api/categories/'
    }).success(function(data) {
      $scope.categories = data.result.categories;
      return $scope.input.category = data.result.categories[0];
    });
    $scope.search = function() {
      $http.get('/api/search', {
        params: {
          'query': $scope.input.query,
          'category': $scope.input.category
        }
      }).success(function(data) {
        return $scope.results = data.results;
      });
      return console.log($scope.input);
    };
    return $scope.create_email_rule = function() {
      return $http.post('/api/email_rules/', $scope.input).success(function(data) {
        return console.log(data);
      });
    };
  }
]);

controllers.controller('AdminCtrl', [
  '$scope', '$http', function($scope, $http) {
    console.log('Welcome to the admin interface.');
    $http({
      method: 'GET',
      url: '/api/advertisements/'
    }).success(function(data) {
      return $scope.advertisement_count = data.meta.count;
    });
    $http({
      method: 'GET',
      url: '/api/email_rules/'
    }).success(function(data) {
      return $scope.email_rule_count = data.meta.count;
    });
    return $http({
      method: 'GET',
      url: '/api/sent_emails/'
    }).success(function(data) {
      return $scope.sent_email_count = data.meta.count;
    });
  }
]);

controllers.controller('AdvertisementCtrl', [
  '$scope', '$http', function($scope, $http) {
    return $http({
      method: 'GET',
      url: '/api/advertisements/'
    }).success(function(data) {
      $scope.advertisements = data.result.advertisements;
      $scope.advertisement_count = data.meta.count;
      return console.log(data);
    });
  }
]);
