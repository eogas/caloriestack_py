
ngApp.controller('FoodCtrl', function($scope, $resource) {

	var Stack = $resource('/stack/:id/:year/:month/:day', {
		stackId: '@id',
		year: '@year',
		month: '@month',
		day: '@day'
	});
	var Meal = $resource('/meal/:id', { id: '@id' });
	var FoodItem = $resource('/fooditem/:id', { id: '@id' }, {
		update: { method: 'PUT' }
	});

	$scope.MealStateEnum = {
		View: 0, Add: 1
	};

	$scope.ItemStateEnum = {
		View: 0, Edit: 1
	};

	$scope.init = function(stackId, year, month, day) {
		$scope.stackId = stackId;
		$scope.currentDate = moment([year, month - 1, day]);

		// fetch all meals
		Stack.get({
			id: stackId,
			year: year,
			month: month,
			day: day
		}, function(data) {
			var meals = data.meals.map(function(meal) {
				meal.items = meal.items.map(function(item) {
					return new FoodItem($.extend(item, {
						state: $scope.ItemStateEnum.View
					}));
				});

				return $.extend(meal, {
					state: $scope.MealStateEnum.View
				});
			});

			$scope.stack = data;
			$scope.meals = meals; // TODO: refactor this out
		});

		$('#datepicker').datetimepicker({
			pickTime: false,
			maxDate: moment(),
			defaultDate: $scope.currentDate
		}).on('dp.change', function(e) {
			document.location = ['',
				$scope.stackId,
				e.date.year(),
				e.date.month() + 1,
				e.date.date()
			].join('/');
		});
	};

	$scope.original = {};

	$scope.itemSelect = function(item) {
		// cancel edit of other items
		$scope.meals.forEach(function(meal) {
			meal.items.forEach(function(foodItem) {
				if (foodItem !== item && foodItem.state == $scope.ItemStateEnum.Edit) {
					$scope.cancelEdit(foodItem);
				}
			});
		});

		angular.copy(item, $scope.original);
		item.state = $scope.ItemStateEnum.Edit;
	};

	$scope.cancelEdit = function(item, event) {
		angular.copy($scope.original, item);
		item.state = $scope.ItemStateEnum.View;

		// This stops the click from passing through to the list item and
		// immediately triggering another edit
		if (event) {
			event.stopPropagation();
			event.preventDefault();
		}
	};

	$scope.saveEdit = function(item, event) {
		item.$update(function() {
			item.state = $scope.ItemStateEnum.View;
		});

		// This stops the click from passing through to the list item and
		// immediately triggering another edit
		if (event) {
			event.stopPropagation();
			event.preventDefault();
		}
	};

	$scope.deleteItem = function(item, meal, index) {
		item.$remove(function() {
			meal.items.splice(index, 1);
		});
	};

	$scope.addItem = function(meal) {
		meal.state = $scope.MealStateEnum.Add;
	};

	$scope.saveAdd = function(meal, item) {
		item.state = $scope.ItemStateEnum.View;
		meal.state = $scope.MealStateEnum.View;

		var newItem = new FoodItem(item);
		newItem.mealId = meal.id;
		newItem.$save(function(cbItem) {
			$.extend(cbItem, {
				state: $scope.ItemStateEnum.View
			});
			meal.items.push(cbItem);
		});
	};

	$scope.cancelAdd = function(meal, item) {
		item = {};
		meal.state = $scope.MealStateEnum.View;
	};

	$scope.mealCals = function(meal) {
		var cals = 0;

		meal.items.forEach(function(item) {
			cals += item.cals;
		});

		if ($.isNumeric(cals)) {
			meal.totalCals = cals;
		}

		return meal.totalCals;
	};

	$scope.dayCals = function() {
		var cals = 0;

		if (!$scope.meals) {
			return 0;
		}

		$scope.meals.forEach(function(meal) {
			cals += meal.totalCals;
		});

		return cals;
	};

	// watch for edit form creation so we can set focus
	$scope.$watch(function() {
		return $('[name="editForm"]')[0];
	}, function(newVal, oldVal) {
		newVal && $(newVal).find('input')[0].focus();
	});

	// watch for add form creation so we can set focus
	// TODO: may need to limit to one add form at a time
	$scope.$watch(function() {
		return $('[name="addForm"]')[0];
	}, function(newVal, oldVal) {
		newVal && $(newVal).find('input')[0].focus();
	});
});
