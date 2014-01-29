notify = angular.module('notify', ['ngRoute', 'controllers'])

notify.config(['$routeProvider', ($routeProvider) ->
	$routeProvider.when('/', {
		templateUrl: 'partials/index.html',
		controller: 'HomePageCtrl',
	}).when('/admin', {
		templateUrl: 'partials/admin/index.html',
		controller: 'AdminCtrl',
	}).when('/admin/sent-emails/:id', {
		templateUrl: 'partials/admin/sent-emails/list.html',
		controller: 'AdminCtrl',
	}).when('/admin/advertisements/', {
		templateUrl: 'partials/admin/advertisements/list.html',
		controller: 'AdvertisementCtrl',
	}).otherwise({
		redirectTo: '/',
	})
])

controllers = angular.module('controllers', [])

controllers.controller('HomePageCtrl', ['$scope', '$http', ($scope, $http) ->
	$scope.input = {
		category: '',
		query: '',
	}
	# Fetch the categories.
	$http({method: 'GET', url:'/api/categories/'}).success((data) ->
		$scope.categories = data.result.categories
		$scope.input.category = data.result.categories[0]
	)

	$scope.search = ->
		# Fetch the search results.
		$http.get('/api/search', {
			params: {
				'query': $scope.input.query,
				'category': $scope.input.category,
			}}).success((data) ->
				$scope.results = data.results
			)
		console.log($scope.input)

	$scope.create_email_rule = ->
		$http.post('/api/email_rules/', $scope.input).success (data) ->
			console.log data
])

controllers.controller('AdminCtrl', ['$scope', '$http', ($scope, $http) ->
	console.log('Welcome to the admin interface.')
	$http({method: 'GET', url:'/api/advertisements/'}).success((data) ->
		$scope.advertisement_count = data.meta.count
	)
	$http({method: 'GET', url:'/api/email_rules/'}).success((data) ->
		$scope.email_rule_count = data.meta.count
	)
	$http({method: 'GET', url:'/api/sent_emails/'}).success((data) ->
		$scope.sent_email_count= data.meta.count
	)
])

controllers.controller('AdvertisementCtrl', ['$scope', '$http', ($scope, $http) ->
	$http({method: 'GET', url:'/api/advertisements/'}).success((data) ->
		$scope.advertisements = data.result.advertisements
		$scope.advertisement_count = data.meta.count
		console.log(data)
	)
])
