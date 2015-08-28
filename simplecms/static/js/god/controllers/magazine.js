app
  .controller('magazineCtrl', [

    '$scope', '$mdToast', '$q',

    'createMagazine', 'getMagazine', 'updateMagazinePost', 'createMagazinePost', 'deleteMagazinePost', 'getPosts', 'catchErr', 'toast',

    function(
      $scope, $mdToast, $q,

      createMagazine, getMagazine, updateMagazinePost, createMagazinePost, deleteMagazinePost, getPosts, catchErr, toast
    ) {
      var magazineId = '1'; //目前只手动建了这一个

      $q.all(
        getMagazine(magazineId)
          .then(function(xhr) {
            $scope.magazine = xhr.data.content;
          }),

        getPosts()
          .then(function(xhr) {
            $scope.allPosts = xhr.data.content;
          })
      )
        .then(function(xhr) {
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
        var delPostFromScope = function() {
          _.pull($scope.magazine.posts, post);
        };

        if (post.id && confirm('确定要删除吗？')) {
          toast('正在删除……');
          deleteMagazinePost($scope.magazine, post)
            .then(_.partial(toast, '删除成功！'))
            .then(delPostFromScope);
        } else {
          delPostFromScope();
        }
      };
      $scope.publishPost = function(post) {
        var promise = (post.id ?
          updateMagazinePost :
          createMagazinePost
        )($scope.magazine, post);

        toast('正在发布……');

        promise
          .then(_.partial(toast, '发布成功！'))
          .catch(_.partial(toast, '发布失败……'));
      };
      $scope.save = function() {
        toast('正在发布……');

        _.map($scope.magazine.posts, $scope.closePost);

        editMagazine(magazineId, $scope.magazine)
          .then(function() {
            toast('发布成功！');
          })
          .catch(function() {
            toast('发布失败……');
          });
      };
    }
  ]);
