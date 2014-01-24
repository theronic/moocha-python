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
	$http({method: 'GET', url:'/api/search/categories/'}).success((data) ->
		$scope.categories = data.categories
		$scope.input.category = data.categories[0]
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
])