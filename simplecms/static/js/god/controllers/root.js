app
  .controller('rootCtrl', function($scope) {
    $scope.categoryDict = {
      normal: '普通文章',
      recipe: '菜谱',
      recipe_list: '菜单',
      event: '话题',
      source: '通过源码发布的文章',
      notification: '商家通知'
    };
  });
