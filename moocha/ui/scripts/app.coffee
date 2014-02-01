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
		category: 'All Categories',
		query: '',
		location: 'South Africa',
	}
	# Fetch the categories.
	$http({method: 'GET', url:'/api/categories/'}).success((data) ->
		$scope.categories = data.result.categories
	)
	# Fetch the locations.
	$http({method: 'GET', url:'/api/locations/'}).success((data) ->
		$scope.locations = data.result.locations
	)


	$scope.search = ->
		console.log($scope.input)
		# Fetch the search results.
		$http.get('/api/search', {
			params: {
				'query': $scope.input.query,
				'category': $scope.input.category,
			}}).success((data) ->
				$scope.results = data.result.advertisements
			)	

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
