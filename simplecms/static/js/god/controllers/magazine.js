app
  .controller('magazineCtrl', function($scope, $mdToast, createMagazine, getMagazine, editMagazine, catchErr, toast) {
    var magazineId = '1'; //目前只手动建了这一个

    getMagazine(magazineId)
      .then(function(xhr) {
        $scope.magazine = xhr.data.content;
      })
      .catch(function(err) {
        return createMagazine({
          title: '美食生活杂志'
        });
      })
      .catch(catchErr);

    $scope.addPost = function() {
      _.map($scope.magazine.posts, $scope.closePost);
      $scope.magazine.posts.unshift({
        opened: true,
        category: '市集故事',
        categoryIcon: 'http://static.xiachufang.com/upload/5883f5a0-4651-11e5-a7fe-c81f66ebffc0.png'
      });
    };
    $scope.editPost = function(post) {
      _.map(_.reject($scope.magazine.posts, post), $scope.closePost);
      post.opened = true;
    };
    $scope.closePost = function(post) {
      delete post.opened;
    };
    $scope.delPost = function(post) {
      _.pull($scope.magazine.posts, post);
    };
    $scope.save = function() {
      _.map($scope.magazine.posts, $scope.closePost);
      editMagazine(magazineId, $scope.magazine)
        .then(function() {
          toast('保存成功！');
        });
    };
  });
