(function(angular) {
  /* global _ */

  angular
    .module('god', ['ngRoute', 'ngMaterial', 'ng.ueditor'])
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider
        .when('/login', {
          controller: 'loginCtrl',
          templateUrl: '/static/js/god/template/login.html'
        })
        .when('/posts', {
          controller: 'postsCtrl',
          templateUrl: '/static/js/god/template/posts.html'
        })
        .when('/posts/new', {
          controller: 'postCtrl',
          templateUrl: '/static/js/god/template/post.html'
        })
        .when('/posts/:id', {
          controller: 'postCtrl',
          templateUrl: '/static/js/god/template/post.html'
        })
        .when('/magazine', {
          controller: 'magazineCtrl',
          templateUrl: '/static/js/god/template/magazine.html'
        })
        .otherwise({
          redirectTo: '/posts'
        });
    }])
    .service('getPosts', function($http) {
      return function() {
        return $http.get('/api/posts');
      };
    })
    .service('getPost', function($http) {
      return function(id) {
        return $http.get('/api/posts/' + id);
      };
    })
    .service('createPost', function($http) {
      return function(post) {
        return $http.post('/api/posts/new', post);
      };
    })
    .service('editPost', function($http) {
      return function(id, post) {
        return $http.post('/api/posts/' + id + '/update', post);
      };
    })
    .service('delPost', function($http) {
      return function(id) {
        return $http.post('/api/posts/' + id + '/delete');
      };
    })
    .service('getMagazine', function($http) {
      return function(id) {
        return $http.get('/api/magazines/' + id);
      };
    })
    .service('editMagazine', function($http) {
      return function(id, magazine) {
        return $http.put('/api/magazines/' + id, magazine);
      };
    })
    .service('login', function($http, $q) {
      return function(user) {
        return $q.all([
          $http.post('/api/login', user),
          // AV.User.logIn(user.username, user.password)
        ]);
      };
    })
    .service('catchErr', function($http, $location) {
      return function(err) {
        try {
          switch (err.data.err) {
            case 1:
              alert(err.data.msg);
              break;
            case 2:
              $location.path('/login');
              break;
            default:
              console.error(err);
              alert(err.data.msg);
          }
        } catch (e) {
          console.error(e);
          alert('出错了……');
        }
      };
    })
    .service('toast', ['$mdToast', function($mdToast) {
      return function(text) {
        $mdToast.show(
          $mdToast.simple()
          .content(text)
          .position('bottom left')
          .hideDelay(3000)
        );
      };
    }])
    .controller('rootCtrl', function($location) {
      // if (!AV.User.current()) {
      //   $location.path('/login');
      // }
    })
    .controller('postsCtrl', function($scope, $timeout, getPosts, catchErr) {
      getPosts()
        .then(function(xhr) {
          $scope.posts = xhr.data.content;
        }, catchErr);
    })
    .controller('loginCtrl', function($scope, $location, login, toast) {
      $scope.user = {
        username: '',
        password: ''
      };
      $scope.login = function() {
        login($scope.user)
          .then(function() {
            $location.path('/');
            toast('登录成功！');
          })
          .catch(function(err) {
            alert(err.data.message);
          });
      };
    })
    .controller('postCtrl', function($scope, $location, $routeParams, $timeout, $mdDialog, getPost, createPost, editPost, delPost, catchErr, toast) {
      var postId = $routeParams.id;
      var isCreatingNew = !angular.isString(postId);

      $scope.isCreatingNew = isCreatingNew;
      $scope.postId = postId;

      $scope.config = {
        UEDITOR_HOME_URL: '/static/lib/ueditor/',
        topOffset: 0,
        autoFloatEnabled: false,
        autoHeightEnabled: false,
        autotypeset: {
          removeEmptyline: true
        },
        blackList: {},
        whiteList: {
          style: 1,
          script: 1
        },
        serverUrl: null,
        enableAutoSave: false,
        // iframeCssUrl: '/static/css/posts.css',
        wordCount: false, //是否开启字数统计
        maximumWords: 99999, //允许的最大字符数
        initialFrameHeight: 500,
        zIndex: 1,
        filterTxtRules: (function() {
          function transP(node) {
            node.tagName = 'p';
            node.setStyle();
          }

          function transDiv(node) {
            node.tagName = 'div';
            node.setStyle();
          }
          return {
            'div': transDiv,
            'caption': transP,
            'th': transP,
            'tr': transP,
            'h1': transP,
            'h2': transP,
            'h3': transP,
            'h4': transP,
            'h5': transP,
            'h6': transP,
            'td': function(node) {
              //没有内容的td直接删掉
              var txt = !!node.innerText();
              if (txt) {
                node.parentNode.insertAfter(UE.uNode.createText(' &nbsp; &nbsp;'), node);
              }
              node.parentNode.removeChild(node, node.innerText());
            }
          };
        })(),
        toolbars: [
          [
            'fullscreen',
            'source',
            '|',
            'undo',
            'redo',
            '|',
            'bold',
            'italic',
            'underline',
            'strikethrough',
            'removeformat',
            'formatmatch',
            'autotypeset',
            'blockquote',
            'pasteplain',
            '|',
            'forecolor',
            'backcolor',
            'insertorderedlist',
            'insertunorderedlist',
            'cleardoc',
            '|',
            'justifyleft',
            'justifycenter',
            'justifyright',
            'justifyjustify',
            '|',
            'link',
            'unlink',
            '|',
            'imagenone',
            'imageleft',
            'imageright',
            'imagecenter',
            '|',
            'simpleupload',
            'insertimage',
            'emotion',
            'background',
            '|',
            'preview',
            '|',
            'customstyle',
            'paragraph',
            'fontfamily',
            'fontsize'
          ]
        ]
      };

      $scope.createPost = function() {
        if ($scope.loading) {
          return false;
        }
        $scope.loading = true;
        createPost($scope.post)
          .then(function(res) {
            toast('保存成功！');
            $location.path('/posts/' + res.data.post.id);
          })
          .catch(catchErr)
          .finally(function() {
            $scope.loading = false;
          });
      };

      $scope.editPost = function() {
        if ($scope.loading) {
          return false;
        }
        $scope.loading = true;
        editPost(postId, $scope.post)
          .then(function() {
            toast('保存成功！');
          })
          .catch(catchErr)
          .finally(function() {
            $scope.loading = false;
          });
      };
      $scope.delPost = function(ev) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
          .parent(angular.element(document.body))
          .title('确定要删除吗？')
          .content('删除后无法恢复。')
          .ariaLabel('Lucky day')
          .ok('确定删除')
          .cancel('不删除了')
          .targetEvent(ev);

        $mdDialog.show(confirm)
          .then(function() {
            delPost($scope.postId)
              .then(function() {
                toast('已删除！');
                $location.path('/posts');
              });
          });
      };

      $scope.submit = isCreatingNew ? $scope.createPost : $scope.editPost;

      if (isCreatingNew) {
        $scope.post = {
          author: '下厨房'
        };
      } else {
        getPost(postId)
          .then(function(xhr) {
            $scope.post = xhr.data.content;
          });
      }
    })
    .controller('magazineCtrl', function($scope, $mdToast, getMagazine, editMagazine, catchErr, toast) {
      var magazineId = '55d4132100b09b5389b6d441'; //目前只手动建了这一个

      getMagazine(magazineId)
        .then(function(xhr) {
          $scope.magazine = xhr.data;
          $scope.magazine.title = '美食生活杂志';
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
})(window.angular);
