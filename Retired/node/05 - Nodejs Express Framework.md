![[Pasted image 20230428235026.png]]
![[Pasted image 20230428235104.png]]

- Potentially NoSQL login: `/api/session/authenticate`

![[Pasted image 20230428235841.png]]
![[Pasted image 20230429000037.png]]
Is error because Tom does not exist? or that the query is bad?

Uploads section:
![[Pasted image 20230429002246.png]]
Visiting redirects back to the main page

It seems as though invalid login names return an error message, where potentially valid username return only `success` boolean. This is verified by testing the names available on the front page, and when trying names such as `lemur` or `joeshmoe` they return `error`.

Nothing comes up for this type of authentication. Rescan on `port 3000`:
![[Pasted image 20230429004022.png]]

Now looking closer at the beginning results, `Hadoop` is not a web page server, but rather a sort of data `load balancer`, if you will. The results from the scan do no really match-up with what we see on the page, so this should have immmediately raised my suspicions that `there's something not right with the results`. No idea why adding Nmap script-scanning  gave a false positive but it's something to keep in mind for the future. [thanks to 0xdf for pointing out this discrepency. I would have spent hours stuck on this]

![[Pasted image 20230429004735.png]]
This appears to match up better.

![[Pasted image 20230429005402.png]]
![[Pasted image 20230429005542.png]]

## App.js
```js
var controllers = angular.module('controllers', []);
var app = angular.module('myplace', [ 'ngRoute', 'controllers' ]);

app.config(function ($routeProvider, $locationProvider) {
  $routeProvider.
    when('/', {
      templateUrl: '/partials/home.html',
      controller: 'HomeCtrl'
    }).
    when('/profiles/:username', {
      templateUrl: '/partials/profile.html',
      controller: 'ProfileCtrl'
    }).
    when('/login', {
      templateUrl: '/partials/login.html',
      controller: 'LoginCtrl'
    }).
    when('/admin', {
      templateUrl: '/partials/admin.html',
      controller: 'AdminCtrl'
    }).
    otherwise({
      redirectTo: '/'
    });

    $locationProvider.html5Mode(true);
});

```

## Admin.js

```js
var controllers = angular.module('controllers');

controllers.controller('AdminCtrl', function ($scope, $http, $location, $window) {
  $scope.backup = function () {
    $window.open('/api/admin/backup', '_self');
  }

  $http.get('/api/session')
    .then(function (res) {
      if (res.data.authenticated) {
        $scope.user = res.data.user;
      }
      else {
        $location.path('/login');
      }
    });
});
```

If response is 'authenticated' then we are within user scope, otherwise, redirect to `/login`
![[Pasted image 20230429005956.png]]

## Profile.js
```js
var controllers = angular.module('controllers');

controllers.controller('ProfileCtrl', function ($scope, $http, $routeParams) {
  $http.get('/api/users/' + $routeParams.username)
    .then(function (res) {
      $scope.user = res.data;
    }, function (res) {
      $scope.hasError = true;

      if (res.status == 404) {
        $scope.errorMessage = 'This user does not exist';
      }
      else {
        $scope.errorMessage = 'An unexpected error occurred';
      }
    });
});

```

 visiting `/api/users/latest:`
![[Pasted image 20230429010120.png]]

```json
_id : "59a7368398aa325cc03ee51d"
username : "tom"
password : "f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240"
is_admin : false
[spongebob]

_id : "59a7368e98aa325cc03ee51e"
username : "mark"
password : "de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73"
is_admin : false
[snowflake]

_id : "59aa9781cced6f1d1490fce9"
username : "rastating"
password : "5065db2df0d4ee53562c650c29bacf55b97e231e3fe88570abc9edd8b78ac2f0"
is_admin : false
[Not found.]
```

![[Pasted image 20230429011124.png]]
![[Pasted image 20230429011157.png]]
`Only admin users have access to the control panel. Check back soon...`

Neither tom nor mark have SSH access and I do not have rastating's password yet. Now that i'm authenticated i receive a cookie:
![[Pasted image 20230429012019.png]]
Stuck again, I looked at `0xdf's writeup` and found that there is a 4th user that was not displayed within the browser's dev-tools:
![[Pasted image 20230429012821.png]]

```json
 {  
   "_id": "59a7365b98aa325cc03ee51c",  
   "username": "myP14ceAdm1nAcc0uNT",  
   "password": "dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af",  
   "is_admin": true  
 },
```

When searching through directories, make sure to hit as many endpoints as possible when sensitive information is leaked in this way. You never know what you may find...

`myP14ceAdm1nAcc0uNT:manchester`
![[Pasted image 20230429013213.png]]


