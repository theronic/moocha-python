notify = angular.module('notify', ['ngRoute', 'controllers'])

notify.config(['$routeProvider', ($routeProvider) ->
	$routeProvider.when('/', {
		templateUrl: 'partials/index.html',
		controller: 'HomePageCtrl',
	})
	.otherwise({
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
	$http({method: 'GET', url:'/api/get_categories'}).success((data) ->
		$scope.categories = (cat for cat of data.categories)
		console.log $scope.categories
	)
	$scope.submit = ->
		# Fetch the search results.
		$http.get('/api/search', {
			params: {
				'query': $scope.input.query,
				'category': $scope.input.category,
			}}).success((data) ->
				$scope.results = data.results
			)
		console.log($scope.input)

	$scope.submit_email = ->
		# Fetch the search results.
		$http.get('/api/send_search_results', {
			params: {
				'query': $scope.input.query,
				'category': $scope.input.category,
				'email_address': $scope.input.email_address,
			}}).success((data) ->
				$scope.results = data.results
			)
		console.log($scope.input)
])