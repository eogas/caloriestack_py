
ngApp.controller('HomeCtrl', function($scope, $resource) {

	var Stack = $resource('/stack/:id', { stackId: '@id' });

	$scope.createStack = function() {
		var stack = new Stack();

		stack.$save(function(newStack) {
			window.location.href = '/' + newStack.stackId;
		});
	};
});
